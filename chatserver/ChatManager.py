import socket
from threading import Thread
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
                print("hello")
                connection.send(bytes([1]) + "HELLO".encode('utf-8'))
            elif command == 2:
                print("login")
            elif command == 3:
                print("logout")
            elif command == 5:
                print("user message")
            elif command == 6:
                print("exit")

            print(address)

            connection.close()

    def accept_new_connection(self):
        while True:
            connection, address = self._server_socket.accept()
            print("new connection")
            handle_connection_thread = Thread(target=self.handle_new_connection, args=(connection,))
            handle_connection_thread.start()
            handle_connection_thread.join()
            print("connection handle done")

    def handle_new_connection(self, connection):
        # TODO
        received = connection.recv(1024)
        print(received)

    def run(self):
        accept_connection_thread = Thread(target=self.accept_new_connection)
        accept_connection_thread.start()
