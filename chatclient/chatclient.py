#!/usr/bin/python           # This is client.py file

import socket

from DataModule import DataModule
from NetworkModule import NetworkModule


def main():
    d = DataModule
    n = NetworkModule(d)
    n.connect(socket.gethostname(), 12345)


if __name__ == "__main__":
    main()
