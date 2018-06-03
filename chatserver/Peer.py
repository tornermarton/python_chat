import socket


class Peer:
    """
    Peer class for storing the socket and name of peer
    """

    def __init__(self, name, connection):
        self._connection = connection
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
