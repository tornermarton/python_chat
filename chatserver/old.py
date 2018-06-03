
'''
import socket

socket = socket.socket()
socket.bind(("", 12345))
socket.listen(5)

while True:
    conn, addr = socket.accept()
    print('Got connection from', addr)

    print(conn.recv(1024)[0])
    message = 'HELLO'
    conn.send(bytes([1]) + message.encode('utf-8'))
    conn.close()
'''