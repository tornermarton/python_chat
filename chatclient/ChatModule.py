#!/usr/bin/python3
from Protocol import Protocol

# must be in this form to catch circular import
import WindowModule
import NetworkModule


class ChatModule:
    def __init__(self):
        self.__network_module: NetworkModule = None
        self.__window_module: WindowModule = None

    @property
    def network_module(self) -> NetworkModule:
        return self.__network_module

    @network_module.setter
    def network_module(self, value: NetworkModule):
        self.__network_module = value

    @property
    def window_module(self) -> WindowModule:
        return self.__window_module

    @window_module.setter
    def window_module(self, value: window_module):
        self.__window_module = value

# public

    class ChatMessage:
        def __init__(self):
            pass

    def receive_message(self, message: Protocol.Message) -> None:
        self.__window_module.displayMessage(message)

    def send_message(self, message: str) -> bool:
        self.__network_module.send(Protocol.user_message(message))
        self.__window_module.displayMessage(Protocol.Message(Protocol.Flags.USER, message))
        return True

    def exit(self) -> None:
        self.__network_module.disconnect()
