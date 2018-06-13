from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QTextCursor

from Protocol import Protocol


class WindowModule(QtWidgets.QMainWindow):

    onExit = QtCore.Signal()
    onMessageSend = QtCore.Signal(str)

    def __init__(self, width: int = 600, height: int = 400):
        super(WindowModule, self).__init__()

        self.resize(width, height)
        # self.setStyleSheet(open("res/css/main.css", "r").read())

        mainLayout = QtWidgets.QGridLayout()

        self.__chatHistory = QtWidgets.QTextEdit()
        self.__chatHistory.setProperty('styleClass', 'chatHistory')
        self.__chatHistory.setReadOnly(True)

        self.__chatInput = QtWidgets.QLineEdit()
        self.__chatInput.setPlaceholderText('Write your message here...')
        self.__chatInput.returnPressed.connect(lambda: self.onMessageSend.emit(self.__chatInput.text()))

        self.__sendButton = QtWidgets.QPushButton('Send')
        self.__sendButton.clicked.connect(lambda: self.onMessageSend.emit(self.__chatInput.text()))

        mainLayout.addWidget(self.__chatHistory, 0, 0, 1, 2)
        mainLayout.addWidget(self.__chatInput, 1, 0)
        mainLayout.addWidget(self.__sendButton, 1, 1)

        mainBox = QtWidgets.QGroupBox()
        mainBox.setLayout(mainLayout)
        self.setCentralWidget(mainBox)

        self.setWindowTitle('PyChat')

    def displayMessage(self, message: Protocol.Message):
        color = "black"
        font_weight = "normal"

        if message.get_flag() is Protocol.Flags.SERVER:
            color = "green"
            font_weight = "bold"

        self.__chatHistory.append('<p style="color:' + color + '; font-weight:' + font_weight + ';">' + str(message) + '</p>')

        # autoscroll
        c = self.__chatHistory.textCursor()
        c.movePosition(QTextCursor.End)
        self.__chatHistory.setTextCursor(c)
        self.__chatHistory.ensureCursorVisible()

    def clearInput(self):
        self.__chatInput.setText('')

    def closeEvent(self, event):
        self.onExit.emit()
        exit()
