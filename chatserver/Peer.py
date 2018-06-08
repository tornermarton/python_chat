from socket import socket
from Pool import Pool
from Protocol import Protocol


class Peer:
    """
    Peer class for storing the socket and name of peer
    """
    
    def __init__(self, connection: socket):
        self.__connection = connection
        self.__name = ""
        self.__pool = None
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value: str):
        self.__name = value
    
    @property
    def __pool(self):
        return self.__pool
    
    @__pool.setter
    def __pool(self, value):
        self.__pool = value
    
    def send_message(self, message: str):
        self.__connection.sendall(bytes([Protocol.Flags.USER]) + message.encode('utf-8') + bytes([Protocol.Flags.TERMINATOR]))
