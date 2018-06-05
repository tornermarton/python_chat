import logging
import socket, time

from ChatManager import ChatManager
from threading import Thread


def phantom():
    time.sleep(1)
    conn = socket.socket()
    conn.connect((socket.gethostname(), 12345))
    conn.send(bytes([1]) + "HELLO".encode('utf-8') + bytes([127]))
    print(conn.recv(1024))


if __name__ == '__main__':
    loginfo = "%(levelname)-10s"
    logtime = "%(asctime)s "
    logthread = "%(threadName)-50s"
    logmsg = "%(message)s"
    
    logging.basicConfig(level=logging.INFO,
    # logging.basicConfig(filename = 'serverlog.log', level = logging.INFO, filemode = 'w',
                        format = loginfo + logtime + logthread + logmsg)
    
    logging.info("Logging started, host: " + socket.gethostname())
    
    cm = ChatManager()
    t = Thread(target = cm.run)
    t.start()
    t.join()
