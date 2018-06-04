import socket
from Pool import Pool

class Peer:
    """
    Peer class for storing the socket and name of peer
    """

    def __init__(self, name, connection, pool):
        self._connection = connection
        self._name = name
        self._pool = pool

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def send_message(self, message):
        self._connection.send(bytes([5]) + message.encode('utf-8'))
