import socket, logging, time
from threading import Thread
from Pool import Pool
from Protocol import Protocol

class ChatManager:
    def __init__(self):
        self.__pools = [Pool("general")]
        self.__server_socket = socket.socket()
        self.__server_socket.bind((socket.gethostname(), 12345))
        self.__server_socket.listen(5)
    
    
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
    
        hello_done = False
        while True:
            received = connection.recv(1024)
            command = received[0]
            terminator = received[-1:]
            
            if terminator != bytes([Protocol.Flags.TERMINATOR]):
                logging.warning("terminator byte not received")
                
            if not hello_done:
                if command == Protocol.Flags.HELLO:
                    logging.info("HELLO message received")
                    connection.send(Protocol.hello_message())
                    hello_done = True
                else:
                    logging.error("No HELLO received, closing connection")
                    connection.close()
                    break
            
            else:
                if command == Protocol.Flags.LOGIN:
                    logging.info("LOGIN message received")
                elif command == Protocol.Flags.LOGOUT:
                    logging.info("LOGOUT message received")
                elif command == Protocol.Flags.USER:
                    logging.info("USER message received")
                elif command == Protocol.Flags.EXIT:
                    logging.info("EXIT message received")
                elif command == Protocol.Flags.SERVER:
                    logging.error("Server received SERVER message")
            
'''
        if self.__wait_for_hello(connection):
            self.__wait_for_login(connection)
    
    def __wait_for_hello(self, connection):
        received = connection.recv(1024)
        command = received[0]
        terminator = received[-1:]
        if terminator != bytes([Protocol.Flags.TERMINATOR]):
            logging.warning("terminator byte not received")
        if command == 1:
            logging.info("Hello received")
            connection.send(Protocol.hello_message())
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
        if terminator != bytes([Protocol.Flags.TERMINATOR]):
            logging.warning("terminator byte not received")
        if command == 1:
            logging.info("Hello received")
            return True
        else:
            logging.error("No hello received, closing connection")
            connection.close()
            return False
'''