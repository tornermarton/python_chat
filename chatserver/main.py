import socket
import logging, Log

from ChatManager import ChatManager
from threading import Thread


if __name__ == '__main__':
    Log.loginit()
    logging.info("Logging started, host: " + socket.gethostname())
    
    cm = ChatManager()
    t = Thread(target = cm.run)
    t.start()
    t.join()
