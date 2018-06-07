import socket
from Pool import Pool

class Peer:
    """
    Peer class for storing the socket and name of peer
    """

    def __init__(self, name, connection, pool):
        self.__connection = connection
        self.__name = name
        self.__pool = pool

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def send_message(self, message):
        self.__connection.sendall(bytes([5]) + message.encode('utf-8'))
