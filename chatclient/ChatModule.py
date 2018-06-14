#!/usr/bin/python3
from typing import List

from PySide2 import QtCore

from Protocol import Protocol

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
        self.__window_module.onLogin.connect(self.login)
        self.__window_module.onJoin.connect(self.join_room)
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
        if len(messages) > 0:
            for i in range(0, len(messages) - 1):
                flag: Protocol.Flags = messages[i][0]
                body: str = ''
                if len(messages[i]) > 1:
                    body = messages[i][1:]
                self.__process_message(Protocol.Message(flag, body))

    @QtCore.Slot(str)
    def send_message(self, message: str) -> None:
        if len(message.strip()) == 0:
            return

        if not self.__connected:
            self.__window_module.display_error_message('You must be connected to the server to send messages!')
        if not self.__logged_in:
            self.__window_module.display_error_message('You must be logged in to send messages!')
        if not self.__room_joined:
            self.__window_module.display_error_message('You must be joined to a room to send messages!')

        if not self.__connected or not self.__logged_in or not self.__room_joined:
            return

        self.__network_module.send(Protocol.user_message(self.__room_name, self.__username, message.strip()))
        self.__window_module.display_self_message(message)
        self.__window_module.clear_input()

    def connect_to_server(self, address: str, port: int) -> None:
        if self.__connected:
            self.disconnect()

        self.__network_module.connect_to_host(address, port)
        self.__network_module.send(Protocol.hello_message())    # first message
        self.__connected = True

    def disconnect_from_server(self) -> None:
        if self.__connected:
            self.__network_module.send(Protocol.exit_message())  # last message
            self.__network_module.disconnect_from_host()
            self.__connected = False

    @QtCore.Slot(str, str)
    def login(self, username: str, password: str) -> None:
        if self.__logged_in:
            self.logout()

        self.__network_module.send(Protocol.login_message(username, password))
        self.__logged_in = True
        self.__username = username

        self.__window_module.add_title_text(self.__username)

    def logout(self) -> None:
        if self.__room_joined:
            self.leave_room()
        if self.__logged_in:
            self.__network_module.send(Protocol.logout_message())
            self.__logged_in = False
            self.__username = ''

    @QtCore.Slot(str, str)
    def join_room(self, room_name: str, password: str) -> None:
        if self.__room_joined:
            self.leave_room()

        self.__network_module.send(Protocol.join_message(room_name, password))
        self.__room_joined = True
        self.__room_name = room_name

        self.__window_module.add_title_text(self.__username + '@' + self.__room_name)
        self.__window_module.display_special_message('You joined the room \'' + room_name + '\' successfully!')

    def leave_room(self) -> None:
        if self.__room_joined:
            self.__network_module.send(Protocol.leave_message())
            self.__room_joined = False
            self.__room_name = ''

        self.__window_module.display_special_message('You left the room!')

    @QtCore.Slot()
    def exit(self) -> None:
        self.leave_room()
        self.logout()
        self.disconnect_from_server()

    # private

    def __process_message(self, message: Protocol.Message) -> None:
        flag = message.get_flag()

        if flag is Protocol.Flags.SERVER:
            server_flag: Protocol.ServerFlags = Protocol.ServerFlags(message.get_message()[1])
            server_message = ''

            if len(str(message)) > 1:
                server_message: str = str(message)[1:]

            if server_flag is Protocol.ServerFlags.NORMAL:
                self.__window_module.display_special_message(server_message)

        elif flag is Protocol.Flags.USER:
            parts: List[bytes] = message.get_body_split()
            if len(parts) == 3:
                self.__window_module.display_user_message(parts[1].decode(), parts[2].decode())

        elif flag is Protocol.Flags.PING:
            self.__network_module.send(Protocol.pong_message())
