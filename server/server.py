from settings_server import *
from _thread import *
import socket

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
HOST = socket.gethostname()

# get my ip address
SERVER_IP = socket.gethostbyname(HOST)
PORT = 9999

try:
    socket_server.bind((SERVER_IP, PORT))
except socket.error as e:
    print(str(e))

socket_server.listen(2)
print(f"Waiting for a connection, Server Started in {HOST}")

#GLOBAL VARIABLES
currend_id = '1'


#THREADS OF CONNECTIONS
def threaded_client(connection):
    global currend_id
    msg_to_client = f"{1}:{FREE_COORDINATES}:{WALL_COORDINATES}:{CHEST_COORDINATES}"
    connection.send(str.encode(msg_to_client)) 
    currend_id = str(int(currend_id)+1)
    while True:
        try:
            data = connection.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                connection.sendall(str.encode('Goodbye'))
                break
            else:
                print('Received: ' + reply)
                connection.sendall(str.encode(reply))
        except:
            break

#MAIN LOOP
while True:
    connection, address = socket_server.accept()
    print(f"Connected to: {address}")
    start_new_thread(threaded_client, (connection,))
