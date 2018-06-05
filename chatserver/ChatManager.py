import socket, logging, time, select
from threading import Thread
from Pool import Pool
from Protocol import Protocol


class ChatManager:
    """
    Managing the communication between the server and the peers
    """
    
    def __init__(self):
        self.__pools = [Pool("general")]
        self.__server_socket = socket.socket()
        self.__server_socket.bind((socket.gethostname(), 12345))
        self.__server_socket.listen(5)
        self.__timeout = 300
    
    
    def run(self):
        """
        Starts accepting connections

        :return: None
        """
        
        accept_new_connection_thread = Thread(target = self.__accept_new_connection)
        accept_new_connection_thread.name = "Accept new conn"
        accept_new_connection_thread.start()
    
    def __accept_new_connection(self):
        """
        Only accepts the incoming connection, then starts a thread for receiving data

        :return: None
        """
        
        while True:
            connection, address = self.__server_socket.accept()
            connection.settimeout(self.__timeout)
            logging.info("New connection: " + str(address))
            handle_new_connection_thread = Thread(target = self.__handle_new_connection, args = [connection])
            handle_new_connection_thread.name = "Conn handler for " + str(address)
            handle_new_connection_thread.start()
    
    def __handle_new_connection(self, connection: socket.socket):
        """
        Receives data from peer on the connection
        
        :param connection: The peer can send data on this connection
        :return: None
        """
        
        hello_done = False
        while True:
            
            valid, command, message = self.__receive_message(connection)
            
            if not valid:
                break
            
            if not hello_done:
                if command == Protocol.Flags.HELLO:
                    logging.info("HELLO message received")
                    connection.send(Protocol.hello_message())
                    hello_done = True
                else:
                    logging.warning("No HELLO received, closing connection")
                    connection.close()
                    break
            
            else:
                if command == Protocol.Flags.HELLO:
                    logging.warning("HELLO message received again")
                    connection.send(Protocol.hello_message())
                
                # TODO
                if command == Protocol.Flags.LOGIN:
                    logging.info("LOGIN message received")
                
                elif command == Protocol.Flags.LOGOUT:
                    logging.info("LOGOUT message received")
                
                elif command == Protocol.Flags.USER:
                    logging.info("USER message received")
                
                elif command == Protocol.Flags.EXIT:
                    logging.info("EXIT message received, connection closed")
                    connection.send(Protocol.server_message("See you later"))
                    connection.close()
                    break
                
                elif command == Protocol.Flags.SERVER:
                    logging.warning("Server received SERVER message, connection closed")
                    connection.send(Protocol.server_message("Did u just try to send a server message to the server? XD"))
                    connection.close()
    
    @staticmethod
    def __receive_message(connection: socket.socket):
        
        try:
            received = connection.recv(Protocol.max_message_size)
        
        except socket.timeout:
            logging.warning("Connection timeout")
            connection.send(Protocol.server_message("Connection timeout"))
            connection.close()
            return False
        
        except ConnectionResetError:
            logging.warning("Connection closed by client")
            return False
        
        if len(received) == 0:
            logging.warning("Connection unexpectedly closed or no byte received")
            connection.send(Protocol.server_message("Whatever happened, you probably cannot receive this message :("))
            connection.close()
            return False
        
        command = received[0]
        message = received[1:-1]
        terminator = received[-1:]
        
        if terminator != bytes([Protocol.Flags.TERMINATOR]):
            logging.warning("Terminator byte not received")
        
        return True, command, message
