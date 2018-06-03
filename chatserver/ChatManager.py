import socket
from Pool import Pool


class ChatManager:
    def __init__(self):
        self._pools = [Pool("general")]
        self._server_socket = socket.socket()
        self._server_socket.bind((socket.gethostname(), 12345))
        self._server_socket.listen(5)

    def manager_loop(self):
        while True:
            connection, address = self._server_socket.accept()
            received = connection.recv(1024)
            command = received[0]
            message = received[1:]
            if command == 1:
                connection.send(bytes([1]) + "HELLO".encode('utf-8'))

            connection.close()
