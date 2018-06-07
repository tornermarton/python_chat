import socket, logging, time, select
from threading import Thread
from Pool import Pool
from Protocol import Protocol


class ChatManager:
    """
    Managing the communication between the server and the peers
    """
    
    def __init__(self):
        self.__pools = {"general": Pool("general")}
        
        self.__server_socket = socket.socket()
        self.__server_socket.bind((socket.gethostname(), 12345))
        self.__server_socket.listen(5)
        
        self.__timeout = 10 * 60
    
    def run(self):
        """
        Starts accepting connections

        :return: None
        """
        
        accept_new_connection_thread = Thread(target = self.__accept_new_connection)
        accept_new_connection_thread.name = "Accept new connection thread"
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
            
            handle_new_connection_thread = Thread(target = self.__message_handler, args = [connection])
            handle_new_connection_thread.name = "Message handler on " + str(address)
            handle_new_connection_thread.start()
    
    @staticmethod
    def __message_handler(connection: socket.socket) -> None:
        """
        
        
        
        :param connection: The peer can be accessed on this connection
        :return: None
        """
    
        hello_done = False
        received: bytes = "".encode("utf-8")
        while True:
            try:
            
                part: bytes
                terminator_index = received.find(bytes([Protocol.Flags.TERMINATOR]))
                while terminator_index == -1:
                    part = connection.recv(Protocol.max_message_size)
                    received += part
                
                    terminator_index = received.find(bytes([Protocol.Flags.TERMINATOR]))
                
                    if len(part) == 0:
                        logging.warning("Connection unexpectedly closed")
                        break
            
            
                if len(part) == 0:
                    if terminator_index == -1:
                        break
            
            
                logging.debug("Message received: " + str(received))
        
            except socket.timeout:
                logging.warning("Connection timeout")
                connection.sendall(Protocol.server_message("Connection timeout"))
                connection.close()
                break
            except ConnectionResetError:
                logging.warning("Connection closed by client without EXIT")
                break
            command = received[0]
            message_body = received[1:terminator_index]
            received = received[terminator_index+1:]
        
            if not hello_done:
                if command == Protocol.Flags.HELLO:
                    logging.info("HELLO message received")
                    connection.sendall(Protocol.hello_message())
                    hello_done = True
                else:
                    logging.warning("No HELLO received, closing connection")
                    connection.close()
                    break
            else:
                if command == Protocol.Flags.HELLO:
                    logging.warning("HELLO message received again")
                    connection.sendall(Protocol.hello_message())
            
                if command == Protocol.Flags.LOGIN:
                    username = message_body.split(bytes([Protocol.Flags.SEPARATOR]))[0].decode()
                    poolname = message_body.split(bytes([Protocol.Flags.SEPARATOR]))[1].decode()
                    logging.info("LOGIN from \"" + username + "\" for joining \"" + poolname + "\"")
            
            
                elif command == Protocol.Flags.LOGOUT:
                    logging.info("LOGOUT message received")
            
                elif command == Protocol.Flags.USER:
                    logging.info("USER message received")
            
                elif command == Protocol.Flags.PING:
                    logging.info("PING message received")
                    connection.sendall(Protocol.pong_message())
            
                elif command == Protocol.Flags.PONG:
                    logging.info("PONG message received")
            
                elif command == Protocol.Flags.EXIT:
                    logging.info("EXIT message received, connection closed")
                    connection.sendall(Protocol.server_message("See you later"))
                    connection.close()
                    break
            
                elif command == Protocol.Flags.SERVER:
                    logging.warning("Server received SERVER message, connection closed")
                    connection.sendall(Protocol.server_message("Did u just try to send a server message to the server? XD"))
                    connection.close()
                    break
                    
                else:
                    logging.warning("Invalid message received")

