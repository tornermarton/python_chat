#!/usr/bin/python3
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

        self.__connected: bool = False
        self.__room_joined: bool = False
        self.__room_name: str = ''

    # public

    @QtCore.Slot(Protocol.Message)
    def receive_message(self, message: Protocol.Message) -> None:
        self.__window_module.displayMessage(message)

    @QtCore.Slot(str)
    def send_message(self, message: str) -> bool:
        self.__network_module.send(Protocol.user_message(message))
        self.__window_module.displayMessage(Protocol.Message(Protocol.Flags.USER, message))
        self.__window_module.clearInput()

    def join_room(self, name: str, password: str) -> None:
        if self.__room_joined:
            self.__network_module.send(Protocol.leave_message())

    @QtCore.Slot()
    def exit(self) -> None:
        self.__network_module.disconnectFromHost()
