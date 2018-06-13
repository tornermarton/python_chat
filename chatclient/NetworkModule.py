#!/usr/bin/python3

import socket
import logging
from threading import Thread
from typing import List

from PySide2 import QtCore

from Protocol import Protocol


class NetworkModule(QtCore.QObject):
    """"The module which communicates with the server over TCP socket connection."""

# public

    onConnectionEstablished = QtCore.Signal()
    onConnectionTerminated = QtCore.Signal()

    onMessageReceived = QtCore.Signal(Protocol.Message)

    def __init__(self):
        super(NetworkModule, self).__init__()

        self.__host: str = ''
        self.__port: int = 0

        self.__thread: Thread = Thread(target=self.__listen)
        self.__thread.name = 'TCP listener'
        self.__socket: socket = socket.socket()
        self.__connected: bool = False

    def connectToHost(self, host: str, port: int) -> None:
        self.__host = host
        self.__port = port

        # connect to the server
        self.__socket.connect((host, port))
        self.__connected = True

        # start listening for messages
        self.__thread.start()

        # send first message (hello)
        self.send(Protocol.hello_message())

    def disconnectFromHost(self) -> None:
        self.send(Protocol.exit_message())

        self.__connected = False
        self.__thread.join()
        self.__socket.close()

        self.onConnectionTerminated.emit()

    def send(self, message: bytes) -> None:
        self.__socket.send(message)

# private

    def __listen(self) -> None:
        if not self.__connected:
            raise RuntimeError('Trying to listen without correctly established connection!')

        while self.__connected:
            received: bytes = self.__socket.recv(Protocol.max_message_size)

            if len(received) == 0:
                logging.error('Connection closed unexpectedly by ' + self.__host + ':' + str(self.__port))

            messages: List[bytes] = received.split(bytes([Protocol.Flags.TERMINATOR]))

            for i in range(0, len(messages)-1):
                flag: Protocol.Flags = messages[i][0]
                body: str = ''
                if len(messages[i]) > 1:
                    body = messages[i][1:]
                self.__process_message(Protocol.Message(flag, body))

    def __process_message(self, message: Protocol.Message) -> None:
        flag = message.get_flag()

        if flag in (Protocol.Flags.SERVER, Protocol.Flags.USER):
            self.onMessageReceived.emit(message)
        elif flag == Protocol.Flags.HELLO:
            self.onConnectionEstablished.emit()
        elif flag == Protocol.Flags.PING:
            self.send(Protocol.pong_message())

