class Pool:
    def __init__(self, name):
        self.__name = name
        self.__peers = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def add_peer(self, peer):
        self.__peers.append(peer)

    def remove_peer(self, peer):
        self.__peers.remove(peer)

    def send_message(self, message):
        for peer in self.__peers:
            peer.send_message(message)
