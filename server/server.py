import socket
from server_setup import *
from _thread import *
import sys
import time

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Constantes
BUFFER_SIZE = 2048  # Tamaño del buffer
HOST = socket.gethostname()  # Obtiene el nombre de la máquina
SERVER_IP = socket.gethostbyname(HOST)  # Obtiene la IP de la máquina
PORT = 6751  # Puerto de conexión

# Conexión
try:
    socket_server.bind((SERVER_IP, PORT))
except socket.error as e:
    print(str(e))

socket_server.listen(2)  # Escucha a 2 clientes
print(f"Esperando conexión, servidor iniciado en {HOST} con IP {SERVER_IP}")

# Variables globales
current_id = 1
time_countdown = False
id_winner = 0
message = ""


def threaded_client(conn):
    global current_id, id_winner, time_countdown
    id_client = current_id
    position_player = "0,0"
    current_id += 1
    config_client = f"{id_client}:{FREE_COORDINATES}:{WALL_COORDINATES}:{CHEST_COORDINATES}"
    conn.send(str.encode(config_client))
    while True:
        try:
            data = conn.recv(BUFFER_SIZE)  # Recibe los
            reply = data.decode("utf-8")
            position_player = reply.split(":")[1]
            msg_client = reply.split(":")[2]
            # Decodifica los datos
            reply = f"{id_client}:{position_player}:{msg_client}"

            if not data:
                print("Desconexión")
                break
            else:
                position_player = reply.split(":")[1]
                msg_client = reply.split(":")[2]
                print(f"{id_client}:{position_player}:{msg_client}")
                # Si el mensaje del cliente es "start" o el mensaje del servidor es "start" para la cuenta regresiva
                if msg_client == "start" or time_countdown:
                    time_countdown = True
                    msg_client = "start"
                    print(f"El jugador {id_client} ha iniciado el juego")
                    # Enviar el tiempo de 15 hacia atras
                    reply = f"{id_client}:{position_player}:{msg_client}"
                    conn.sendall(str.encode(reply))  # Envía los datos
                    for i in range(15, 0, -1):
                        msg_client = f"{i}"
                        print(f"{i} segundos restantes")
                        reply = f"{id_client}:{position_player}:{msg_client}"
                        conn.recv(BUFFER_SIZE)
                        conn.sendall(str.encode(reply))  # Envía los datos
                        time.sleep(1)
                    time_countdown = False
                # Si el cliente envia "chest"
                elif msg_client == "chest":
                    id_winner = id_client
                    msg_client = "winner"
                    print(f"El jugador {id_client} ha encontrado un cofre")
                    reply = f"{id_client}:{id_winner}:{msg_client}"
                    conn.sendall(str.encode(reply))
                    id_winner = 0
                elif id_winner != 0:
                    msg_client = "winner"
                    reply = f"{id_client}:{id_winner}:{msg_client}"
                    conn.sendall(str.encode(reply))
                    id_winner = 0
                else:
                    conn.sendall(str.encode(reply))  # Envía los datos
        except:
            break
    print(f"Conexión terminada con el jugador {id_client}")
    current_id -= 1
    conn.close()


# Loop principal
while True:
    client, address = socket_server.accept()  # Acepta la conexión
    print(f"Conexión aceptada de {address[0]}:{address[1]}")
    start_new_thread(threaded_client, (client,))
