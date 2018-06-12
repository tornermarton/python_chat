#!/usr/bin/python3

import socket, logging, time, ssl
from threading import Thread
from Pool import Pool
from Protocol import Protocol
from Peer import Peer
from SQLModule import SQLModule


class ChatManager:
    """
    Managing the communication between the server and the peers
    """
    
    def __init__(self):
        self.__pools = {"general": Pool("general")}
        
        self.__server_socket = socket.socket()
        self.__server_socket.bind((socket.gethostname(), 12345))
        self.__server_socket.listen(5)
        
        # self.__context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        # self.__context.load_cert_chain(certfile = "cert.pem")  # 1. key, 2. cert, 3. intermediates
        # self.__context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # optional
        # self.__context.set_ciphers('EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH')
        
        self.__timeout = 10 * 60
        
        self.__sql_module = SQLModule()
    
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
        Accepts the incoming connection, creates Peer for the connection, then starts a thread for receiving data

        :return: None
        """
        while True:
            sock, address = self.__server_socket.accept()

            # connection = self.__context.wrap_socket(sock, server_side = True)
            connection = sock
            
            connection.settimeout(self.__timeout)
            
            logging.info("New connection: " + str(address))
            
            peer = Peer(connection)
            
            handle_new_peer_thread = Thread(target = self.__message_handler, args = [peer])
            handle_new_peer_thread.name = "Message handler on " + str(address)
            handle_new_peer_thread.start()
    
    def __message_handler(self, peer: Peer) -> None:
        """
        
        :param peer:
        :return:
        """
        
        hello_done = False
        received: bytes = "".encode("utf-8")
        while True:
            try:
                
                part: bytes
                terminator_index = received.find(bytes([Protocol.Flags.TERMINATOR]))
                while terminator_index == -1:
                    part = peer.receive()
                    received += part
                    
                    terminator_index = received.find(bytes([Protocol.Flags.TERMINATOR]))
                    
                    if len(part) == 0:
                        logging.warning("Connection unexpectedly closed")
                        peer.terminate()
                        break
                
                if len(part) == 0:
                    if terminator_index == -1:
                        break
                
                logging.debug("Message received: " + str(received))
                
                command = received[0]
                message_body = received[1:terminator_index]
                received = received[terminator_index + 1:]
                
                if not hello_done:
                    hello_done = self.__receive_hello(peer, command)
                    if not hello_done:
                        break
                
                elif self.__process_message(peer, command, message_body):
                    peer.terminate()
                    break
            
            except socket.timeout:
                logging.warning("Connection timeout")
                peer.send(Protocol.server_message("Connection timeout"))
                peer.terminate()
                break
            
            except ConnectionResetError:
                logging.warning("Connection is reset by the peer")
                peer.terminate()
                break
            
            except ConnectionAbortedError:
                logging.warning("Connection closed by client without EXIT")
                peer.terminate()
                break
    
    
    @staticmethod
    def __receive_hello(peer: Peer, command: bytes):
        """
        
        Tries to receives HELLO, if the message is not HELLO, terminates the peer
        
        :param peer:
        :param command:
        :return:    True, if HELLO message has been received
        """
        if command == Protocol.Flags.HELLO:
            logging.info("HELLO message received")
            peer.send(Protocol.hello_message())
            peer.send(Protocol.server_message("Welcome to the server"))
            return True
        else:
            logging.warning("No HELLO received, closing connection")
            peer.terminate()
            return False
    
    def __process_message(self, peer: Peer, command: bytes, message: bytes) -> bool:
        """
        
        Processes the received message
        
        :param peer:
        :param command:
        :param message:
        :return: True, if connection should be closed
        """
        
        if command == Protocol.Flags.HELLO:
            logging.warning("HELLO message received again")
            peer.send(Protocol.hello_message())
        
        if command == Protocol.Flags.LOGIN:
            username = message.split(bytes([Protocol.Flags.SEPARATOR]))[0].decode()
            poolname = message.split(bytes([Protocol.Flags.SEPARATOR]))[1].decode()
            
            logging.info("LOGIN from \"" + username + "\" for joining \"" + poolname + "\"")
            
            peer.name = username
            
            if poolname in self.__pools:
                logging.debug("Pool already exists")
                self.__pools[poolname].add_peer(peer)
            else:
                logging.debug("Pool not exists, creating")
                self.__pools[poolname] = Pool(poolname)
                self.__pools[poolname].add_peer(peer)
            
            peer.pool = self.__pools[poolname]
            peer.pool.send_message(Protocol.server_message(username + " has joined the room"), peer)
        
        
        elif command == Protocol.Flags.LOGOUT:
            logging.info("LOGOUT message received")
            peer.leave_pool()
        
        elif command == Protocol.Flags.USER:
            logging.info("USER message received")
            if not peer.is_logged_in():
                peer.send(Protocol.server_message("You gotta log in first"))
            else:
                peer.pool.send_message(message, peer)
        
        elif command == Protocol.Flags.PING:
            logging.info("PING message received")
            peer.send(Protocol.pong_message())
        
        elif command == Protocol.Flags.PONG:
            logging.info("PONG message received")
        
        elif command == Protocol.Flags.EXIT:
            logging.info("EXIT message received, connection closed")
            peer.send(Protocol.server_message("See you later"))
            return True
        elif command == Protocol.Flags.SERVER:
            logging.warning("Server received SERVER message, connection closed")
            peer.send(Protocol.server_message("Did u just try to send a server message to the server? XD"))
            return True
        
        else:
            peer.send(Protocol.server_message("Invalid message received"))
            logging.warning("Invalid message received")
