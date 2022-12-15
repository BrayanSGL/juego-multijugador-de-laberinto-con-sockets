from settings_server import *
from _thread import *
import socket
import time

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

BUFFER_SIZE = 2048
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

# GLOBAL VARIABLES
currend_id = '1'
time_to_start = False
message = ''
id_winner = ''

# THREADS OF CONNECTIONS
def threaded_client(connection):
    global currend_id, time_to_start, message, id_winner
    id_client = currend_id
    msg_to_client = f"{id_client}:{FREE_COORDINATES}:{WALL_COORDINATES}:{CHEST_COORDINATES}"
    connection.send(str.encode(msg_to_client))
    currend_id = str(int(currend_id)+1)
    while True:
        try:
            data = connection.recv(BUFFER_SIZE)
            reply = data.decode('utf-8')
            if not data:
                connection.sendall(str.encode('Goodbye'))
                break
            else:
                # Magic
                # get data of client
                position_client = reply.split(":")[1]
                message_client = reply.split(":")[2]
                print(
                    f"Player {id_client} is in {position_client} and says {message_client}")
                # Want start game?
                if message_client == "start" or time_to_start or message == 'start':
                    # send data to client
                    # T-15
                    message = 'start'
                    reply = f"{id_client}:{position_client}:{message}"
                    connection.sendall(str.encode(reply))
                    time_to_start = True
                    for i in range(15, 0, -1):
                        time.sleep(1)
                        print(f"Time to start: {i}")
                        message = i
                        reply = f"{id_client}:{position_client}:{message}"
                        data = connection.recv(BUFFER_SIZE)
                        print(reply, 'reply')
                        connection.sendall(str.encode(reply))
                    time_to_start = False
                if message_client == "win" or (message.split(':')[0] == 'won' and id_winner == ''):
                    id_winner = id_client
                    message = f'won:{id_winner}'
                    reply = f"{id_client}:{position_client}:{message}"
                    print(reply)
                    connection.sendall(str.encode(reply))
                else:
                    connection.sendall(str.encode(reply))
        except:
            break
    print(f'Lost connection of player: {id_client}')
    connection.close()


# MAIN LOOP
while True:
    connection, address = socket_server.accept()
    print(f"Connected from: {address}")
    start_new_thread(threaded_client, (connection,))
