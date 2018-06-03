import socket
from chatserver.Pool import Pool


class ChatManager:
    def __init__(self):
        self._pools = [Pool("general")]
        self._server_socket = socket.socket()
        self._server_socket.bind((socket.gethostname(), 12345))
        self._server_socket.listen(5)


    def manager_loop(self):
        while True:
            connection, address = self._server_socket.accept()
            print(type(connection))
            print('Got connection from', address)

            print(connection.recv(1024))
            message = 'HELLO'
            connection.send(bytes([1]) + message.encode('utf-8'))
            connection.close()

