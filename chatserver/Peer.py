#!/usr/bin/python3

from socket import socket
from Protocol import Protocol
import logging
import Pool


class Peer:
    """
    Peer class for storing the socket and name of peer
    """
    
    
    def __init__(self, connection: socket):
        self.__connection: socket = connection
        self.__username: str = None
        self.__logged_in: bool = False
        self.__hello_done: bool = False
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
        
    @property
    def logged_in(self):
        return self.__logged_in
    
    @logged_in.setter
    def logged_in(self, value):
        self.__logged_in = value
        
    @property
    def hello_done(self):
        return self.__hello_done
    
    @hello_done.setter
    def hello_done(self, value):
        self.__hello_done = value
        
    
    def send(self, bytes_message: bytes):
        self.__connection.sendall(bytes_message)
    
    def receive(self) -> bytes:
        
        """
        
        Receives a message on its connection
        
        :return:
        """
        
        try:
            return self.__connection.recv(Protocol.max_message_size)
        except ConnectionAbortedError:
            raise
        
    def terminate(self):
        """
        
        The peer closes the connection
        
        :return:
        """
        
        self.__connection.close()
        
        if self.__pool is not None:
            self.__pool.remove_peer(self)

    def leave_pool(self):
    
        """

        The peer leaves the pool

        :return:
        """
    
        if self.__pool is not None:
            self.__pool.remove_peer(self)
        self.__pool = None
