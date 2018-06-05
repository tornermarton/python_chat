import socket, time
import logging, Log

from ChatManager import ChatManager
from threading import Thread


def phantom():
    time.sleep(1)
    conn = socket.socket()
    conn.connect((socket.gethostname(), 12345))
    conn.send(bytes([1]) + "HELLO".encode('utf-8') + bytes([127]))
    print(conn.recv(1024))


if __name__ == '__main__':
    Log.loginit()
    logging.info("Logging started, host: " + socket.gethostname())
    
    cm = ChatManager()
    t = Thread(target = cm.run)
    t.start()
    t.join()
