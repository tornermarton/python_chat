import socket


class Pool:
    def __init__(self, name):
        self._name = name
        self._peers = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def add_peer(self, peer):
        self._peers.append(peer)

    def remove_peer(self, peer):
        self._peers.remove(peer)

    def send_message(self, message):
        for peer in self._peers:
            peer.send_message(message)