#!/usr/bin/python3

import socket
import logging, Log

from ChatManager import ChatManager


if __name__ == '__main__':
    Log.loginit()
    logging.info("Logging started, host: " + socket.gethostname())
    
    cm = ChatManager()
    cm.run()
