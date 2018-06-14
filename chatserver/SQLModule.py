#!/usr/bin/python3

import mysql.connector
from datetime import *
import logging
import Log


class SQLModule:
    conn = mysql.connector.connect(pool_name = "asd", pool_size = 5, host = "ffabi.ddns.net", user = "pychat", password = "pychat", database = "pychat")
    cursor = conn.cursor()
    
    @staticmethod
    def get_wrapper(query: str, username: str):
        
        try:
            SQLModule.cursor.execute(query, (username,))
            info = SQLModule.cursor.fetchall()
        except mysql.connector.Error as e:
            SQLModule.conn.rollback()
            logging.error("SQL Error: " + str(e))
            pass
            return -2  # szebben kéne
        
        if SQLModule.cursor.rowcount == 1:
            return info[0][0]
        else:
            return -1
    
    @staticmethod
    def insert_wrapper(query: str, data):  # data is a tuple
        
        try:
            
            SQLModule.cursor.execute(query, data)
            SQLModule.conn.commit()
            
            logging.debug(str(SQLModule.cursor.rowcount) + " rows effected for data " + str(data))  # nem kell sztem
        
        except mysql.connector.Error as e:
            SQLModule.conn.rollback()
            logging.error("SQL Error: " + str(e))
            pass
        
    @staticmethod
    def now():
        return str(datetime.utcnow()).split(".")[0]
    
    
    class PeersSQLModule:
        
        @staticmethod
        def get_id(username: str):
            query = "SELECT peer_id FROM Peers WHERE username = %s;"
            return SQLModule.get_wrapper(query, username)
        
        @staticmethod
        def get_hashed_pwd(username: str):
            query = "SELECT hashed_pwd FROM Peers WHERE username = %s;"
            return SQLModule.get_wrapper(query, username)
        
        @staticmethod
        def get_last_online(username: str):
            query = "SELECT last_online FROM Peers WHERE username = %s;"
            return SQLModule.get_wrapper(query, username)
        
        @staticmethod
        def add_peer(username: str, hashed_pwd: str):
    
            query = "INSERT IGNORE INTO Peers (username, hashed_pwd, last_online) VALUES (%s, %s, %s);"
            SQLModule.insert_wrapper(query, (username, hashed_pwd, SQLModule.now()))
            
    
    
    class PoolsSQLModule:
        
        @staticmethod
        def get_id(username: str):
            query = "SELECT pool_id FROM Pools WHERE pool_name = %s;"
            return SQLModule.get_wrapper(query, username)
        
        @staticmethod
        def get_hashed_pwd(username: str):
            query = "SELECT hashed_pwd FROM Pools WHERE pool_name = %s;"
            return SQLModule.get_wrapper(query, username)
        
        @staticmethod
        def get_last_message(username: str):
            query = "SELECT last_message FROM Pools WHERE pool_name = %s;"
            return SQLModule.get_wrapper(query, username)

        @staticmethod
        def add_pool(pool_name: str, hashed_pwd: str):
            query = "INSERT IGNORE INTO Pools (pool_name, hashed_pwd, last_message) VALUES (%s, %s, %s);"
            SQLModule.insert_wrapper(query, (pool_name, hashed_pwd, SQLModule.now()))
            
    
    class SwitchTable:
        
        @staticmethod
        def add_peer_pool(peer_id: int, pool_id: int):
            query = "INSERT IGNORE INTO pools_peers_connector (Peers_peer_id, Pools_pool_id) VALUES (%s, %s);"
            SQLModule.insert_wrapper(query, (peer_id, pool_id, ))
            
        @staticmethod
        def remove_peer_pool(peer_id: int, pool_id: int):
            query = "DELETE FROM pools_peers_connector WHERE Peers_peer_id = %s AND Pools_pool_id = %s;"
            SQLModule.insert_wrapper(query, (peer_id, pool_id, ))
            return SQLModule.cursor.rowcount == 1



# Log.loginit()
# SQLModule.SwitchTable.remove_peer_pool(51, 1)
