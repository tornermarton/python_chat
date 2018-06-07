import socket, time
connectionToServer = socket.socket()
connectionToServer.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

connectionToServer.connect(("192.168.1.19", 12345))
connectionToServer.sendall(bytes([1]) + "HELLOaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa".encode('utf-8') + bytes([127]))
print(connectionToServer.recv(1024))
connectionToServer.sendall(bytes([6]) + "Ping".encode('utf-8') + bytes([127]))
print(connectionToServer.recv(1024))
connectionToServer.sendall(bytes([6]) + "Ping".encode('utf-8') + bytes([127]))
print(connectionToServer.recv(1024))
connectionToServer.sendall(bytes([2]) + "username".encode('utf-8') + bytes([29]) + "poolname".encode('utf-8') + bytes([127]))
connectionToServer.sendall(bytes([8]) + "exit".encode('utf-8') + bytes([127]))
print(connectionToServer.recv(1024))

