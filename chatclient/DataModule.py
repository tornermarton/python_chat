#!/usr/bin/python3
from typing import List

from Protocol import *


class DataModule:
    """DataModule stores all the connection (address, port) and user data (username, chat room info, etc.).
        Later the chat history will also be stored here."""

# public

    def __init__(self):
        self.__username = 'a_basic_noob'
        self.__current_room_name = ''
        self.__messages = List[Protocol.Message]

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, value: str):
        self.__username = value

    @property
    def current_room_name(self) -> str:
        return self.__current_room_name

    @current_room_name.setter
    def current_room_name(self, value: str):
        self.__current_room_name = value

    def has_message(self) -> bool:
        return len(self.__messages) != 0

    def add_message(self, message: Protocol.Message):
        self.__messages.append(message)
