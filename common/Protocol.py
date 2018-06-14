#!/usr/bin/python3

from enum import IntEnum
from typing import List


class Protocol:
    """The protocol for the network communication."""
    
    class Flags(IntEnum):
        """Basic flags (bits) used by the protocol."""
        
        # Flag name = byte # meaning (message body)
        HELLO = 1
        LOGIN = 2  # user login (username + SEPARATOR + hashed password)
        LOGOUT = 3  # user logout
        JOIN = 4  # join chatroom (chatroom name + SEPARATOR + chatroom hashed password)
        LEAVE = 5  # leave chatroom (chatroom name)
        SERVER = 6
        USER = 7  # poolname + SEPARATOR + message body
        PING = 8
        PONG = 9
        EXIT = 10  # close connection
        SALT = 11
        
        SEPARATOR = 29
        TERMINATOR = 127

    class ServerFlags(IntEnum):
        """Flags to distinguish server messages, must be behind server message flag"""
        NORMAL = 1

        ACK = 6
        NAK = 21
    
    # static
    
    max_message_size: int = 1024
    max_message_body_size: int = max_message_size - 2
    
    @staticmethod
    def hello_message() -> bytes:
        return Protocol.Message(Protocol.Flags.HELLO, '').get_message()
    
    @staticmethod
    def login_message(username: str, password: str) -> bytes:
        return Protocol.Message(Protocol.Flags.LOGIN,
                                    username.encode() + bytes([Protocol.Flags.SEPARATOR]) + password.encode()
                                ).get_message()
    
    @staticmethod
    def logout_message() -> bytes:
        return Protocol.Message(Protocol.Flags.LOGOUT, '').get_message()

    @staticmethod
    def join_message(room_name: str, password: str) -> bytes:
        return Protocol.Message(Protocol.Flags.JOIN,
                                    room_name.encode() + bytes([Protocol.Flags.SEPARATOR]) + password.encode()
                                ).get_message()

    @staticmethod
    def leave_message() -> bytes:
        return Protocol.Message(Protocol.Flags.LEAVE, '').get_message()

    @staticmethod
    def server_message(server_flag: ServerFlags, body: str) -> bytes:
        return Protocol.Message(Protocol.Flags.SERVER, bytes([server_flag]) + body.encode()).get_message()
    
    @staticmethod
    def user_message(room_name: str, username: str, body: str) -> bytes:
        return Protocol.Message(Protocol.Flags.USER,
                                    room_name.encode() + bytes([Protocol.Flags.SEPARATOR])
                                    + username.encode() + bytes([Protocol.Flags.SEPARATOR])
                                    + body.encode()
                                ).get_message()
    
    @staticmethod
    def ping_message() -> bytes:
        return Protocol.Message(Protocol.Flags.PING, '').get_message()
    
    @staticmethod
    def pong_message() -> bytes:
        return Protocol.Message(Protocol.Flags.PONG, '').get_message()
    
    @staticmethod
    def exit_message() -> bytes:
        return Protocol.Message(Protocol.Flags.EXIT, '').get_message()

    @staticmethod
    def split_message_body(body: bytes) -> List[bytes]:
        parts: List[bytes] = body.split(bytes([Protocol.Flags.SEPARATOR]))

        return parts[:-1]
    
    class Message:
        """Protocol messages"""
        
        # public
        
        def __init__(self, flag, body):
            if len(body) > Protocol.max_message_body_size:
                raise ValueError('Message body size can be a maximum of 1022 bytes!')
            
            if type(flag) is Protocol.Flags:  # is a real flag
                self.__flag = flag
            else:  # is int
                self.__flag = Protocol.Flags(flag)
            
            if type(body) is bytes:  # is a byte array (bytes)
                self.__body = body
            else:  # is a string (str)
                self.__body = body.encode()
        
        def __str__(self):
            return self.__body.decode()
        
        def get_flag(self):
            return self.__flag
        
        def get_message(self) -> bytes:
            return bytes([self.__flag]) + self.__body + bytes([Protocol.Flags.TERMINATOR])

        def get_body_split(self) -> List[bytes]:
            return Protocol.split_message_body(self.__body)
