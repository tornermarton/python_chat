#!/usr/bin/python3

import mysql.connector
from datetime import *
import logging
import Log


class SQLModule:
    conn = mysql.connector.connect(host = "127.0.0.1", user = "pychat", password = "pychat", database = "pychat")
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
            return -1
        
        if SQLModule.cursor.rowcount == 1:
            return info[0][0]
        else:
            return -1
    
    @staticmethod
    def insert_wrapper(query: str, data):  # data is a tuple
        
        try:
            
            SQLModule.cursor.execute(query, data)
            SQLModule.conn.commit()
            if SQLModule.cursor.rowcount == 1:
                logging.info(data + " inserted into database")
            else:
                logging.warning(data + " is already in the database")  # nem kell sztem
        
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
            query = "SELECT peer_id FROM Peers WHERE username = %s"
            return SQLModule.get_wrapper(query, username)
        
        @staticmethod
        def get_hashed_pwd(username: str):
            query = "SELECT hashed_pwd FROM Peers WHERE username = %s"
            return SQLModule.get_wrapper(query, username)
        
        @staticmethod
        def get_last_online(username: str):
            query = "SELECT last_online FROM Peers WHERE username = %s"
            return SQLModule.get_wrapper(query, username)
        
        @staticmethod
        def add_peer(username: str, hashed_pwd: str):
    
            query = "INSERT IGNORE INTO Peers (username, hashed_pwd, last_online) VALUES (%s, %s, %s)"
            SQLModule.insert_wrapper(query, (username, hashed_pwd, SQLModule.now()))
            
    
    
    class PoolsSQLModule:
        
        @staticmethod
        def get_id(username: str):
            query = "SELECT pool_id FROM Pools WHERE pool_name = %s"
            return SQLModule.get_wrapper(query, username)
        
        @staticmethod
        def get_hashed_pwd(username: str):
            query = "SELECT hashed_pwd FROM Pools WHERE pool_name = %s"
            return SQLModule.get_wrapper(query, username)
        
        @staticmethod
        def get_last_message(username: str):
            query = "SELECT last_message FROM Pools WHERE pool_name = %s"
            return SQLModule.get_wrapper(query, username)

        @staticmethod
        def add_pool(pool_name: str, hashed_pwd: str):
            query = "INSERT IGNORE INTO Pools (pool_name, hashed_pwd, last_message) VALUES (%s, %s, %s)"
            SQLModule.insert_wrapper(query, (pool_name, hashed_pwd, SQLModule.now()))


Log.loginit()
a = SQLModule()
SQLModule.PeersSQLModule.add_peer("asd12asd31", "asd213")
