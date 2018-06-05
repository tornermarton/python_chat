from enum import IntEnum


class Protocol:
    """The protocol for the network communication."""

    _max_message_size = 1024
    _max_message_body_size = _max_message_size - 2

    class Flags(IntEnum):
        """Flags (bits) used by the protocol."""

        HELLO = 1
        LOGIN = 2
        LOGOUT = 3
        SERVER = 4
        USER = 5
        EXIT = 6
        TERMINATOR = 127

    @staticmethod
    def hello_message():
        return Protocol.Message(Protocol.Flags.HELLO, '')

    @staticmethod
    def login_message(body):
        return Protocol.Message(Protocol.Flags.LOGIN, body)

    @staticmethod
    def logout_message():
        return Protocol.Message(Protocol.Flags.LOGOUT, '')

    @staticmethod
    def server_message(body):
        return Protocol.Message(Protocol.Flags.SERVER, body)

    @staticmethod
    def user_message(body):
        return Protocol.Message(Protocol.Flags.USER, body)

    @staticmethod
    def exit_message():
        return Protocol.Message(Protocol.Flags.EXIT, '')

    class Message:
        """Protocol messages"""

        def __init__(self, flag, body):
            if len(body) > Protocol._max_message_body_size:
                raise ValueError('Message body size can be a maximum of 1022 bytes!')

            if type(flag) is Protocol.Flags:        # is a real flag
                self._flag = flag
            else:                                   # is int
                self._flag = Protocol.Flags(flag)

            if type(body) is bytes:                 # is a byte array (bytes)
                self._body = body
            else:                                   # is a string (str)
                self._body = body.encode()

        def __str__(self):
            return self._body.decode()

        def get_flag(self):
            return self._flag

        def get_message(self):
            return bytes([self._flag]) + self._body + bytes([Protocol.Flags.TERMINATOR])
