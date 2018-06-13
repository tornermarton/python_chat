from PySide2 import QtCore, QtGui
from PySide2.QtCore import Qt, QDateTime
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLineEdit


class JoinDialog(QDialog):
    def __init__(self, parent=None):
        super(JoinDialog, self).__init__(parent)

        # formatting
        self.setWindowTitle("Join room")

        # validator
        regexp = QtCore.QRegExp('[A-Za-z0-9_]+')
        validator = QtGui.QRegExpValidator(regexp)

        # widgets
        self.room_nameInput = QLineEdit()
        self.room_nameInput.setValidator(validator)

        self.passwordInput = QLineEdit()
        self.passwordInput.setValidator(validator)
        self.passwordInput.setEchoMode(QLineEdit.Password)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        self.buttons.button(QDialogButtonBox.Ok).setText('Join')
        self.buttons.setCenterButtons(True)

        # signals
        self.room_nameInput.textChanged.connect(self.check_input)
        self.room_nameInput.textChanged.emit(self.room_nameInput.text())

        self.passwordInput.textChanged.connect(self.check_input)
        self.passwordInput.textChanged.emit(self.passwordInput.text())

        # layout
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.room_nameInput)
        self.mainLayout.addWidget(self.passwordInput)
        self.mainLayout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # self.buttons.setEnabled(False)
        self.room_nameInput.setFocus()

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
    def get_room_nameInput(self):
        return self.room_nameInput.text()

    # get current data from the dialog
    def getPasswordInput(self):
        return self.passwordInput.text()

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def run(parent=None):
        dialog = JoinDialog(parent)
        result = dialog.exec_()
        room_name = dialog.get_room_nameInput()
        password = dialog.getPasswordInput()
        return room_name, password, result == QDialog.Accepted
