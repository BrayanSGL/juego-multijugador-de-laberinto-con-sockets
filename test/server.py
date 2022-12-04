import socket
from _thread import *
import sys

# Create a socket object TCP
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = socket.gethostname()

# get my ip address
ip = socket.gethostbyname(host)
print(ip, type(ip))

server = '192.168.1.64'
port = 9999

server_ip = socket.gethostbyname(server)
print('Server started in ' + host)

try:
    serversocket.bind((server, port))
except socket.error as e:
    print(str(e))

serversocket.listen(2)
print("Waiting for a connection, Server Started")


start_clock = False

status = '0,0:0,0'  # id, status: x, y
current_id = '0'

def threaded_client(connection):
    global start_clock, status, current_id
    connection.send(str.encode(current_id))
    current_id = str(int(current_id)+1)

    while True:
        try:
            data = connection.recv(2048)
            reply = data.decode('utf-8')
            if reply == 'q':
                print('Disconnected')
                break
            

            #####
            
            # elif reply == 'i' or start_clock:
            #     start_clock = True
            #     print('game started')
            #     connection.sendall(str.encode('S'))
            
            ####
            if not data:
                connection.sendall(str.encode('Goodbye'))
                break
            else:
                print('Received: ' + reply)
                connection.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    connection.close()

    #     data = connection.recv(2048)
    #     reply = 'Server output: ' + data.decode('utf-8')
    #     if not data:
    #         break
    #     connection.sendall(str.encode(reply))
    # connection.close()
while True:
    clientsocket, address = serversocket.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    start_new_thread(threaded_client, (clientsocket,))
