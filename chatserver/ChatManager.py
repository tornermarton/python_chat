#!/usr/bin/python3

import socket, logging, time, ssl
from threading import Thread
from Protocol import Protocol
from Peer import Peer
from Pool import Pool
from SQLModule import SQLModule
from bcrypt import hashpw


class ChatManager:
    """
    Managing the communication between the server and the peers
    """
    
    def __init__(self):
        self.__pools = {}
        
        self.__server_socket = socket.socket()
        self.__server_socket.bind((socket.gethostname(), 12345))
        self.__server_socket.listen(5)
        
        # self.__context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        # self.__context.load_cert_chain(certfile = "cert.pem")  # 1. key, 2. cert, 3. intermediates
        # self.__context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # optional
        # self.__context.set_ciphers('EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH')
        
        # kliens pl:
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile = "cert.pem")
        # context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        # connectionToServer = context.wrap_socket(sock, server_hostname = "pychat")
        # connectionToServer.connect(("192.168.1.19", 12345))
        
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
        Accepts the incoming connection, creates Peer for the connection, then starts a thread for receiving data

        :return: None
        """
        while True:
            sock, address = self.__server_socket.accept()
            
            # connection = self.__context.wrap_socket(sock, server_side = True)
            connection = sock
            
            connection.settimeout(self.__timeout)
            
            logging.info("New connection: " + str(address))
            
            handle_new_peer_thread = Thread(target = self.__message_handler, args = [connection])
            handle_new_peer_thread.name = "Message handler on " + str(address)
            handle_new_peer_thread.start()
    
    def __message_handler(self, connection: socket) -> None:
        peer = Peer(connection)
        received: bytes = "".encode("utf-8")
        while True:
            try:
                
                command, message_body, received, invalid = self.__receive(peer, received)
                
                if invalid:
                    break
                
                if not peer.hello_done:
                    self.__receive_hello(peer, command)
                    if peer.hello_done:
                        continue
                
                if not peer.logged_in:
                    self.__receive_login(peer, command, message_body)
                    if peer.logged_in:
                        continue
                
                if self.__process_message(peer, command, message_body):
                    peer.terminate()
                    break
            
            except socket.timeout:
                logging.warning("Connection timeout")
                peer.send(Protocol.server_message(Protocol.ServerFlags.NORMAL, "Connection timeout"))
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
        
        logging.debug("End of thread")
    
    @staticmethod
    def __receive(peer: Peer, received: bytes) -> (bytes, bytes, bytes, bool):
        terminator_index = received.find(bytes([Protocol.Flags.TERMINATOR]))
        while terminator_index == -1:
            part: bytes = peer.receive()
            received += part
            
            terminator_index = received.find(bytes([Protocol.Flags.TERMINATOR]))
            
            if len(part) == 0:
                logging.warning("Connection unexpectedly closed")
                peer.terminate()
                return None, None, None, True
        
        logging.debug("Message received: " + str(received))
        
        command = received[0]
        body = received[1:terminator_index]
        received = received[terminator_index + 1:]
        
        return command, body, received, False
    
    @staticmethod
    def __receive_hello(peer: Peer, command: bytes):
        """
        
        Tries to receives HELLO, if the message is not HELLO, terminates the peer
        
        :param peer:
        :param command:
        :return:
        """
        if command == Protocol.Flags.HELLO:
            logging.info("HELLO message received")
            peer.send(Protocol.hello_message())
            peer.send(Protocol.server_message(Protocol.ServerFlags.ACK, "Welcome to the server"))
            peer.hello_done = True
        else:
            logging.warning("No HELLO received, closing connection")
            peer.terminate()
            peer.hello_done = False
    
    @staticmethod
    def __receive_login(peer: Peer, command: bytes, message: bytes):
        if command == Protocol.Flags.LOGIN:
            username = message.split(bytes([Protocol.Flags.SEPARATOR]))[0].decode()
            passwd = message.split(bytes([Protocol.Flags.SEPARATOR]))[1].decode()
            hashed = str(hashpw(passwd.encode("utf-8"), b"$2a$12$" + b"SZ4R4Z3G3SZ4DJ4LS0RT..")).split("..")[1][:-1]
            logging.info("LOGIN from \"" + username + "\"")
            
            peer_id = SQLModule.PeersSQLModule.get_id(username)
            if peer_id == -1 or hashed == SQLModule.PeersSQLModule.get_hashed_pwd(username):
                if peer_id == -1:
                    SQLModule.PeersSQLModule.add_peer(username, hashed)
                    logging.info("Account created for \"" + username + "\"")
                    peer.send(Protocol.server_message(Protocol.ServerFlags.ACK, "Account created for \"" + username + "\""))
                peer.name = username
                peer.logged_in = True
                logging.info("\"" + username + "\" has logged in succesfully")
                peer.send(Protocol.server_message(Protocol.ServerFlags.ACK, "Successful login"))
            
            else:
                logging.warning("\"" + username + "\" failed to log in")
                peer.send(Protocol.server_message(Protocol.ServerFlags.NAK, "Wrong password for this user"))
                peer.logged_in = False
    
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
        
        elif command == Protocol.Flags.LOGIN:
            logging.warning("User \"" + peer.name + "\" is already logged in")
            peer.send(Protocol.server_message(Protocol.ServerFlags.ACK, "You are already logged in"))
        
        elif command == Protocol.Flags.PING:
            logging.info("PING message received")
            peer.send(Protocol.pong_message())
        
        elif command == Protocol.Flags.PONG:
            logging.info("PONG message received")
        
        elif command == Protocol.Flags.EXIT:
            logging.info("EXIT message received, connection closed")
            peer.send(Protocol.server_message(Protocol.ServerFlags.NORMAL, "See you later"))
            return True
        
        elif command == Protocol.Flags.LOGOUT:
            if not peer.logged_in:
                return False
            logging.info("LOGOUT message received from \"" + peer.name + "\"")
            peer.logged_in = False
            peer.name = None
        
        elif command == Protocol.Flags.JOIN:
            if not peer.logged_in:
                return False
            
            pool_name = message.split(bytes([Protocol.Flags.SEPARATOR]))[0].decode()
            passwd = message.split(bytes([Protocol.Flags.SEPARATOR]))[1].decode()
            hashed = str(hashpw(passwd.encode("utf-8"), b"$2a$12$" + b"SZ4R4Z3G3SZ4DJ4LS0RT..")).split("..")[1]

            logging.info("JOIN from \"" + peer.name + "\" for pool \"" + pool_name + "\"")
            
            pool_id = SQLModule.PoolsSQLModule.get_id(pool_name)
            if pool_id == -1 or hashed == SQLModule.PoolsSQLModule.get_hashed_pwd(pool_name):
                if pool_name in self.__pools:
                    logging.debug("Pool already exists")
                    self.__pools[pool_name].add_peer(peer)
                else:
                    logging.debug("Pool not exists, creating")
                    self.__pools[pool_name] = Pool(pool_name)
                    self.__pools[pool_name].add_peer(peer)
                    
                if pool_id == -1:
                    SQLModule.PoolsSQLModule.add_pool(pool_name, hashed)
                    logging.info("Pool created with name \"" + pool_name + "\"")
                    peer.send(Protocol.server_message(Protocol.ServerFlags.ACK, "Pool created with name \"" + pool_name + "\""))

                pool_id = SQLModule.PoolsSQLModule.get_id(pool_name)
                peer_id = SQLModule.PeersSQLModule.get_id(peer.name)
                SQLModule.SwitchTable.add_peer_pool(peer_id, pool_id)
                logging.info("\"" + peer.name + "\" has joined \"" + pool_name + "\" succesfully")
                peer.send(Protocol.server_message(Protocol.ServerFlags.ACK, "Successful join"))
    
                peer.pool = self.__pools[pool_name]
                peer.pool.send_message(Protocol.server_message(Protocol.ServerFlags.NORMAL, peer.name + " has joined the room"), peer)
            
            else:
                logging.warning("\"" + pool_name + "\" failed to log in")
                peer.send(Protocol.server_message(Protocol.ServerFlags.NAK, "Wrong password for this pool"))
        
        elif command == Protocol.Flags.LEAVE:
            if not peer.logged_in:
                return False
            # pool_name = message.split(bytes([Protocol.Flags.SEPARATOR]))[0].decode()
            pool_name = peer.pool.name
            logging.info("LEAVE from \"" + peer.name + "\" for pool \"" + pool_name + "\"")
            
            peer_id = SQLModule.PeersSQLModule.get_id(peer.name)
            pool_id = SQLModule.PoolsSQLModule.get_id(pool_name)
            
            if SQLModule.SwitchTable.remove_peer_pool(peer_id, pool_id):
                peer.send(Protocol.server_message(Protocol.ServerFlags.NORMAL, "You've left the group"))
            
            peer.leave_pool()
        
        elif command == Protocol.Flags.USER:
            if not peer.logged_in:
                peer.send(Protocol.server_message(Protocol.ServerFlags.NORMAL, "You gotta log in first"))
                return False
            if peer.pool is None:
                peer.send(Protocol.server_message(Protocol.ServerFlags.NORMAL, "You gotta join a room first"))
                return False
            
            logging.info("USER message received")
            
            peer.pool.send_message(message, peer)
        
        
        elif command == Protocol.Flags.SERVER:
            logging.warning("Server received SERVER message, connection closed")
            return True
        
        else:
            peer.send(Protocol.server_message(Protocol.ServerFlags.NORMAL, "Invalid message received"))
            logging.warning("Invalid message received")
        
        return False
