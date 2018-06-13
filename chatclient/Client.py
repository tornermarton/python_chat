#!/usr/bin/python3
import socket

from ChatModule import ChatModule
from NetworkModule import NetworkModule
from WindowModule import WindowModule


class Client:
    """Chat client."""

    def __init__(self):
        self.__network_module = NetworkModule()
        self.__window_module = WindowModule()
        self.__chat_module = ChatModule(self.__network_module, self.__window_module)

    def run(self):
        self.__network_module.connectToHost(socket.gethostname(), 12345)
        self.__window_module.show()
