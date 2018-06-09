from socket import socket
from Protocol import Protocol
import Pool
import logging


class Peer:
    """
    Peer class for storing the socket and name of peer
    """
    
    
    def __init__(self, connection: socket):
        self.__connection = connection
        self.__username: str = ""
        self.__pool: Pool = None
    
    @property
    def name(self):
        return self.__username
    
    @name.setter
    def name(self, value: str):
        self.__username = value
    
    @property
    def pool(self) -> Pool:
        return self.__pool
    
    @pool.setter
    def pool(self, value: Pool):
        self.__pool = value
        
    def send(self, bytes_message: bytes):
        self.__connection.sendall(bytes_message)
    
    def receive(self) -> bytes:
        try:
            return self.__connection.recv(Protocol.max_message_size)
        except ConnectionAbortedError:
            raise
    
    def is_logged_in(self)->bool:
        return self.__pool is not None
    
    def terminate(self):
        
        self.__connection.close()
        
        if self.__pool is not None:
            self.__pool.remove_peer(self)
            
        logging.info("User \"" + self.__username + "\" terminated")
    
    def leave_pool(self):
        if self.__pool is not None:
            self.__pool.remove_peer(self)
        self.__pool = None