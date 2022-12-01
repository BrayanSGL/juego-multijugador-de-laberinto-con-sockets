import socket
from _thread import *
import sys

# Create a socket object TCP
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = socket.gethostname()

#get my ip address
ip = socket.gethostbyname(host)
print(ip, type(ip))

server = 'localhost'
port = 9999

server_ip = socket.gethostbyname(server)
print('Server started in ' + host)

try:
    serversocket.bind((server, port))
except socket.error as e:
    print(str(e))

serversocket.listen(2)
print("Waiting for a connection, Server Started")

def threaded_client(connection):
    connection.send(str.encode('Welcome to the server'))
    while True:
        data = connection.recv(2048)
        reply = 'Server output: ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()

while True:
    clientsocket, address = serversocket.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    start_new_thread(threaded_client, (clientsocket,))
