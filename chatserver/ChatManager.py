import socket, logging, time
from threading import Thread
from Pool import Pool
from Flags import Flags


class ChatManager:
    def __init__(self):
        self.__pools = [Pool("general")]
        self.__server_socket = socket.socket()
        self.__server_socket.bind((socket.gethostname(), 12345))
        self.__server_socket.listen(5)
    
    def manager_loop(self):
        while True:
            connection, address = self.__server_socket.accept()
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
    
    def run(self):
        accept_new_connection_thread = Thread(target = self.__accept_new_connection)
        accept_new_connection_thread.name = "Accept new conn"
        accept_new_connection_thread.start()
    
    def __accept_new_connection(self):
        while True:
            connection, address = self.__server_socket.accept()
            logging.info("New connection: " + str(address))
            handle_new_connection_thread = Thread(target = self.__handle_new_connection, args = [connection])
            handle_new_connection_thread.name = "Conn handler for " + str(address)
            handle_new_connection_thread.start()
            handle_new_connection_thread.join()
    
    # TODO
    def __handle_new_connection(self, connection):
        if self.__wait_for_hello(connection):
            self.__wait_for_login(connection)
    
    def __wait_for_hello(self, connection):
        received = connection.recv(1024)
        command = received[0]
        terminator = received[-1:]
        if terminator != bytes([Flags.TERMINATOR]):
            logging.warning("terminator byte not received")
        if command == 1:
            logging.info("Hello received")
            connection.send(bytes([Flags.HELLO]) + "HELLO".encode('utf-8') + bytes([Flags.TERMINATOR]))
            return True
        else:
            logging.error("No hello received, closing connection")
            connection.close()
            return False
    
    
    def __wait_for_login(self, connection):
        received = connection.recv(1024)
        command = received[0]
        message = received[1:]
        terminator = received[-1:]
        if terminator != bytes([Flags.TERMINATOR]):
            logging.warning("terminator byte not received")
        if command == 1:
            logging.info("Hello received")
            connection.send(bytes([Flags.HELLO]) + "HELLO".encode('utf-8') + bytes([Flags.TERMINATOR]))
            return True
        else:
            logging.error("No hello received, closing connection")
            connection.close()
            return False
