from typing import List
from Peer import Peer


class Pool:
    __peers: List[Peer]
    
    def __init__(self, name):
        self.__name = name
        self.__peers = []
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value: str):
        self.__name = value
    
    def add_peer(self, peer: Peer):
        self.__peers.append(peer)
    
    def remove_peer(self, peer: Peer):
        self.__peers.remove(peer)
    
    def send_message(self, message: str):
        for peer in self.__peers:
            peer.send_message(message)
