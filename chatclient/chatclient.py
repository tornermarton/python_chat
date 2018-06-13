#!/usr/bin/python           # This is client.py file

import sys
from PySide2 import QtWidgets

import Log
from Client import Client


def main():
    Log.loginit()
    app = QtWidgets.QApplication(sys.argv)
    c = Client()
    c.run()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
