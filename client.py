import socket

sock = socket.socket()

sock.connect(('127.0.0.1', 9999))
sock.send(b'12')

print(sock.recv(1024))