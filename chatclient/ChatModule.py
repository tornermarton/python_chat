#!/usr/bin/python3
import logging
from typing import List

from PySide2 import QtCore

from Protocol import Protocol

# must be in this form to catch circular import
import WindowModule
import NetworkModule


class ChatModule(QtCore.QObject):
    def __init__(self, network_module: NetworkModule, window_module: WindowModule):
        super(ChatModule, self).__init__()

        # wire in Network module
        self.__network_module: NetworkModule = network_module
        self.__network_module.onMessageReceived.connect(self.receive_message)

        # wire in window module
        self.__window_module: WindowModule = window_module
        self.__window_module.onMessageSend.connect(self.send_message)
        self.__window_module.onExit.connect(self.exit)

        # set variables
        self.__connected: bool = False

        self.__logged_in: bool = False
        self.__username: str = ''

        self.__room_joined: bool = False
        self.__room_name: str = ''

    # public

    @QtCore.Slot(bytes)
    def receive_message(self, data: bytes) -> None:
        messages: List[bytes] = data.split(bytes([Protocol.Flags.TERMINATOR]))

        for i in range(0, len(messages) - 1):
            flag: Protocol.Flags = messages[i][0]
            body: str = ''
            if len(messages[i]) > 1:
                body = messages[i][1:]
            self.__process_message(Protocol.Message(flag, body))

    @QtCore.Slot(str)
    def send_message(self, message: str) -> None:
        self.__network_module.send(Protocol.user_message(self.__room_name, self.__username, message))
        self.__window_module.display_user_message(message)
        self.__window_module.clear_input()

    def connect_to_server(self, address: str, port: int) -> None:
        self.__network_module.connect_to_host(address, port)
        self.__network_module.send(Protocol.hello_message())    # first message

    def disconnect_from_server(self) -> None:
        self.__network_module.send(Protocol.exit_message())  # last message
        self.__network_module.disconnect_from_host()

    def login(self, username: str, password: str) -> None:
        self.__network_module.send(Protocol.login_message(username, password))
        self.__logged_in = True
        self.__username = username

    def logout(self) -> None:
        if self.__logged_in:
            self.__network_module.send(Protocol.logout_message())
            self.__logged_in = False
            self.__username = ''

    def join_room(self, room_name: str, password: str) -> None:
        if self.__room_joined:
            self.leave_room()

        self.__network_module.send(Protocol.join_message(room_name, password))
        self.__room_joined = True
        self.__room_name = room_name

    def leave_room(self) -> None:
        if self.__room_joined:
            self.__network_module.send(Protocol.leave_message())
            self.__room_joined = False
            self.__room_name = ''

    @QtCore.Slot()
    def exit(self) -> None:
        self.leave_room()
        self.logout()
        self.disconnect_from_server()

    # private

    def __process_message(self, message: Protocol.Message) -> None:
        flag = message.get_flag()

        if flag is Protocol.Flags.SERVER:
            self.__window_module.display_special_message(str(message))
        elif flag is Protocol.Flags.USER:
            self.__window_module.display_user_message(str(message))
        elif flag is Protocol.Flags.PING:
            self.__network_module.send(Protocol.pong_message())
