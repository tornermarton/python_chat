from PySide2 import QtCore, QtGui
from PySide2.QtCore import Qt, QDateTime
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLineEdit


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        # formatting
        self.setWindowTitle("Login")

        # validator
        regexp = QtCore.QRegExp('[A-Za-z0-9_]+')
        validator = QtGui.QRegExpValidator(regexp)

        # widgets
        self.usernameInput = QLineEdit()
        self.usernameInput.setValidator(validator)

        self.passwordInput = QLineEdit()
        self.passwordInput.setValidator(validator)
        self.passwordInput.setEchoMode(QLineEdit.Password)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        self.buttons.button(QDialogButtonBox.Ok).setText('Login')
        self.buttons.button(QDialogButtonBox.Cancel).setText('Quit')
        self.buttons.setCenterButtons(True)

        # signals
        self.usernameInput.textChanged.connect(self.check_input)
        self.usernameInput.textChanged.emit(self.usernameInput.text())

        self.passwordInput.textChanged.connect(self.check_input)
        self.passwordInput.textChanged.emit(self.passwordInput.text())

        # layout
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.usernameInput)
        self.mainLayout.addWidget(self.passwordInput)
        self.mainLayout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # self.buttons.setEnabled(False)
        self.usernameInput.setFocus()

    def check_input(self, *args, **kwargs):
        sender = self.sender()
        validator = sender.validator()
        state = validator.validate(sender.text(), 0)[0]

        if state == QtGui.QValidator.Acceptable:
            color = '#ffffff'
        elif state == QtGui.QValidator.Intermediate:
            color = '#ffffff'
        else:
            color = '#f6989d' # red
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)

    # get current data from the dialog
    def getUsernameInput(self):
        return self.usernameInput.text()

    # get current data from the dialog
    def getPasswordInput(self):
        return self.passwordInput.text()

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def run(parent=None):
        dialog = LoginDialog(parent)
        result = dialog.exec_()
        username = dialog.getUsernameInput()
        password = dialog.getPasswordInput()
        return username, password, result == QDialog.Accepted
