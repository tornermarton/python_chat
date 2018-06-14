from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QTextCursor

from JoinDialog import JoinDialog
from LoginDialog import LoginDialog


class WindowModule(QtWidgets.QMainWindow):

    onExit = QtCore.Signal()
    onMessageSend = QtCore.Signal(str)
    onLogin = QtCore.Signal(str, str)
    onJoin = QtCore.Signal(str, str)

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

    def display_user_message(self, username: str, message: str) -> None:
        self.__display_message(username, message)

    def display_self_message(self, message: str) -> None:
        self.__display_message('You', message, 'blue')

    def display_special_message(self, message: str) -> None:
        self.__display_message('Server', message, 'green', 'bold')

    def display_error_message(self, message: str) -> None:
        self.__display_message('Error', message, 'red', 'bold')

    def show_login_dialog(self):
        username, password, ok = LoginDialog.run()
        if ok:
            self.onLogin.emit(username, password)

    def show_join_dialog(self):
        room_name, password, ok = JoinDialog.run()
        if ok:
            self.onJoin.emit(room_name, password)

    def add_title_text(self, text: str):
        self.setWindowTitle('PyChat - ' + text)

    def clear_input(self) -> None:
        self.__chatInput.setText('')

    def closeEvent(self, event) -> None:
        self.onExit.emit()
        exit()

    # private

    def __display_message(self, username: str, message: str, color: str = 'black', font_weight: str = 'normal') -> None:
        self.__chatHistory.append(
            '<p><span style="color:' + color + '; font-weight:bold;">' + username + ': </span>' +
            '<span style="color:' + color + '; font-weight:' + font_weight + ';">' + message + '</span></p>')

        # auto scroll
        c = self.__chatHistory.textCursor()
        c.movePosition(QTextCursor.End)
        self.__chatHistory.setTextCursor(c)
        self.__chatHistory.ensureCursorVisible()
