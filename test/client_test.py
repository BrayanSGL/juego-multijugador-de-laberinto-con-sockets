import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 9999))
id = s.recv(1024).decode("utf-8")
print(id)