from settings_server import *
from _thread import *
import socket
import time

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
print(f"Waiting for a connection, Server Started in {HOST} ip: {SERVER_IP}")

#GLOBAL VARIABLES
currend_id = '1'
time_to_start = False


#THREADS OF CONNECTIONS
def threaded_client(connection):
    global currend_id, time_to_start
    my_id = currend_id
    control = True
    msg_to_client = f"{my_id}:{FREE_COORDINATES}:{WALL_COORDINATES}:{CHEST_COORDINATES}"
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
                #Magic
                #get data of client
                position = reply.split(":")[1]
                message = reply.split(":")[2]
                print(f"Player {my_id} is in {position} and says {message}")
                #Want start game?
                if message == "start" or (time_to_start and control) :
                    #send data to client
                    #T-15
                    connection.sendall(str.encode(reply))
                    time_to_start = True
                    for i in range(15,0,-1):
                        time.sleep(1)
                        print(f"Time to start: {i}")
                        message = i
                        reply = f"{my_id}:{position}:{message}"
                        data = connection.recv(2048)
                        connection.sendall(str.encode(reply))
                    time_to_start = False
                    control = False
                else:
                    connection.sendall(str.encode(reply))
        except:
            break
    print(f'Lost connection of player: {my_id}')
    connection.close()
#MAIN LOOP
while True:
    connection, address = socket_server.accept()
    print(f"Connected from: {address}")
    start_new_thread(threaded_client, (connection,))
