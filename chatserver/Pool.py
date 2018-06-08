from typing import List
import Peer


class Pool:
    
    def __init__(self, name):
        self.__name = name
        self.__peers: List[Peer.Peer] = []
    
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
            peer.send(message.encode("utf-8"))
