import socket, logging, time, select
from threading import Thread
from Pool import Pool
from Protocol import Protocol
from multiprocessing import Queue
from multiprocessing import Event


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
        
        self.__incoming_queue = Queue(100)  # max size is maybe necessary for Condition
        
    
    
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

            connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, Protocol.max_message_size) # ez nem biztos, hogy kell
            
            logging.info("New connection: " + str(address))
            
            stop_signal = Event()
            
            handle_new_connection_thread = Thread(target = self.__message_handler, args = [connection, stop_signal])
            handle_new_connection_thread.name = "Message handler on " + str(address)
            handle_new_connection_thread.start()
            
            receive_message_thread = Thread(target = self.__message_receiver, args = [connection, stop_signal])
            receive_message_thread.name = "Message receiver on " + str(address)
            receive_message_thread.start()
            
    
    def __message_receiver(self, connection: socket.socket, stop_signal: Event):
        """
        
        Producer: Receives the data and pushes it to the queue
        
        :param connection:
        :return:
        """

        while True:
            try:
                received = connection.recv(100*Protocol.max_message_size)
                if len(received) == 0:
                    stop_signal.set()
                    logging.warning("Connection unexpectedly closed or no byte received")
                    # connection.close()
                    break
    
                if not self.__incoming_queue.full():
                    self.__incoming_queue.put(received)
                else:
                    logging.error("Queue is full")
                
            except socket.timeout:
                stop_signal.set()
                time.sleep(1)
                logging.warning("Connection timeout")
                connection.sendall(Protocol.server_message("Connection timeout"))
                connection.close()
                break
                
            except ConnectionResetError:
                stop_signal.set()
                time.sleep(1)
                logging.warning("Connection closed by client")
                break
                
            except OSError:
                stop_signal.set()
                logging.debug("Killing message receiver thread")
                break
    
    def __message_handler(self, connection: socket.socket, stop_signal: Event):
        """
        Consumer: Handles data taken from the queue
        
        :param connection: The peer can be accessed on this connection
        :return: None
        """
        
        
        hello_done = False
        while True:
    
            if stop_signal.is_set():
                break
            
            
            if not self.__incoming_queue.empty():
                received = self.__incoming_queue.get()
            else:
                continue


            logging.debug("Message received: " + str(received))

            command = received[0]
            message = received[1:-1]
            terminator = received[-1:]

            if terminator != bytes([Protocol.Flags.TERMINATOR]):
                logging.warning("Terminator byte not received")

            # valid, command, message = self.__message_receiver(connection)
            message: bytes
            
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
                    username = message.split(bytes([Protocol.Flags.SEPARATOR]))[0].decode()
                    poolname = message.split(bytes([Protocol.Flags.SEPARATOR]))[1].decode()
                    logging.info("LOGIN from " + username + " for joining " + poolname)
                
                
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

        '''
    @staticmethod
    def old__receive_message(connection: socket.socket):
        """

        Receives the data and checks its validity

        :param connection:
        :return:
        """
        
        try:
            time.sleep(1)
            received = connection.recv(Protocol.max_message_size)
            # logging.info("Message received: " + str(received))
        
        except socket.timeout:
            logging.warning("Connection timeout")
            connection.sendall(Protocol.server_message("Connection timeout"))
            connection.close()
            return False, "", ""
        
        except ConnectionResetError:
            logging.warning("Connection closed by client")
            return False, "", ""
        
        if len(received) == 0:
            logging.warning("Connection unexpectedly closed or no byte received")
            connection.sendall(Protocol.server_message("Whatever happened, you probably cannot receive this message :("))
            connection.close()
            return False, "", ""
        
        command = received[0]
        message = received[1:-1]
        terminator = received[-1:]
        
        if terminator != bytes([Protocol.Flags.TERMINATOR]):
            logging.warning("Terminator byte not received")
        
        return True, command, message
'''