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
        self.__chat_module.connect_to_server(socket.gethostname(), 12345)

        self.__window_module.show_login_dialog()
        # self.__window_module.show_join_dialog()
        self.__chat_module.join_room('general', 'general')

        self.__window_module.show()
