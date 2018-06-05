#!/usr/bin/python3

import socket
import re
from functools import reduce

from Protocol import Protocol
from threading import Thread


class NetworkModule:
    """"The module which communicates with the server over TCP socket connection."""

# private

    def __listen(self):
        if not self.__connected:
            raise RuntimeError('Trying to listen without correctly established connection!')

        while self.__connected:
            received = self.__socket.recv(Protocol.max_message_size)
            messages = received.split(bytes([Protocol.Flags.TERMINATOR]))

            for i in range(0, len(messages)-1):
                flag = messages[i][0]
                body = ''
                if len(messages[i]) > 1:
                    body = messages[i][1:]
                self.__process_message(Protocol.Message(flag, body))

    def __process_message(self, message):
        print(message.get_message())

# public

    def __init__(self):
        self.__thread = Thread(target=self.__listen)
        self.__thread.name = 'NetworkModule listener'
        self.__socket = socket.socket()
        self.__connected = False

    def connect(self, host, port):
        # connect to the server
        self.__socket.connect((host, port))
        self.__connected = True

        # start listening for messages
        self.__thread.start()

        # send first message (hello)
        self.send(Protocol.hello_message())

    def disconnect(self):
        self.__connected = False
        self.__thread.join()
        self.__socket.close()

    def send(self, message):
        self.__socket.send(message)
