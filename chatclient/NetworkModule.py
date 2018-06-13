#!/usr/bin/python3

import socket, logging
from threading import Thread

from PySide2 import QtCore

from Protocol import Protocol


class NetworkModule(QtCore.QObject):
    """"The module which communicates with the server over TCP socket connection."""

# public

    onMessageReceived = QtCore.Signal(bytes)

    def __init__(self):
        super(NetworkModule, self).__init__()

        self.__host: str = ''
        self.__port: int = 0

        self.__thread: Thread = Thread(target=self.__listen)
        self.__thread.name = 'TCP listener'
        self.__socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connected: bool = False

    def connect_to_host(self, host: str, port: int) -> None:
        self.__host = host
        self.__port = port

        # connect to the server
        self.__socket.connect((host, port))
        self.__connected = True

        logging.info('Connection established to host: ' + self.__host + ':' + str(self.__port) + '!')

        # start listening for messages
        self.__thread.start()

    def disconnect_from_host(self) -> None:
        self.__connected = False
        self.__socket.close()
        self.__thread.join()

        logging.info('Connection closed!')

    def send(self, message: bytes) -> None:
        self.__socket.send(message)


# private

    def __listen(self) -> None:
        if not self.__connected:
            raise RuntimeError('Trying to listen without correctly established connection!')

        logging.info('Listening started on: '+self.__host+':'+str(self.__port)+'!')

        while self.__connected:
            try:
                data: bytes = self.__socket.recv(Protocol.max_message_size)

                if len(data) == 0:
                    continue

                self.onMessageReceived.emit(data)
            except:
                continue

        logging.info('Listening stopped on: '+self.__host+':'+str(self.__port)+'!')
