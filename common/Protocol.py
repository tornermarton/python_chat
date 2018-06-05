#!/usr/bin/python3

from enum import IntEnum


class Protocol:
    """The protocol for the network communication."""

    class Flags(IntEnum):
        """Flags (bits) used by the protocol."""

        HELLO = 1
        LOGIN = 2
        LOGOUT = 3
        SERVER = 4
        USER = 5
        EXIT = 6
        TERMINATOR = 127

# static

    max_message_size = 1024
    max_message_body_size = max_message_size - 2

    @staticmethod
    def hello_message():
        return Protocol.Message(Protocol.Flags.HELLO, '').get_message()

    @staticmethod
    def login_message(body):
        return Protocol.Message(Protocol.Flags.LOGIN, body).get_message()

    @staticmethod
    def logout_message():
        return Protocol.Message(Protocol.Flags.LOGOUT, '').get_message()

    @staticmethod
    def server_message(body):
        return Protocol.Message(Protocol.Flags.SERVER, body).get_message()

    @staticmethod
    def user_message(body):
        return Protocol.Message(Protocol.Flags.USER, body).get_message()

    @staticmethod
    def exit_message():
        return Protocol.Message(Protocol.Flags.EXIT, '').get_message()

    class Message:
        """Protocol messages"""

        def __init__(self, flag, body):
            if len(body) > Protocol.max_message_body_size:
                raise ValueError('Message body size can be a maximum of 1022 bytes!')

            if type(flag) is Protocol.Flags:        # is a real flag
                self.__flag = flag
            else:                                   # is int
                self.__flag = Protocol.Flags(flag)

            if type(body) is bytes:                 # is a byte array (bytes)
                self.__body = body
            else:                                   # is a string (str)
                self.__body = body.encode()

        def __str__(self):
            return self.__body.decode()

        def get_flag(self):
            return self.__flag

        def get_message(self):
            return bytes([self.__flag]) + self.__body + bytes([Protocol.Flags.TERMINATOR])
