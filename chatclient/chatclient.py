#!/usr/bin/python           # This is client.py file

import socket

from NetworkModule import *


n = NetworkModule()
n.connect(socket.gethostname(), 12345)
