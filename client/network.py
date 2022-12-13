import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.71"
        self.port = 9999
        self.addr = (self.server, self.port)
        self.settings = self.connect()
        self.id = self.decode_settings()[0]
        self.free_coordinates = eval(self.decode_settings()[1])
        self.wall_coordinates = eval(self.decode_settings()[2])
        self.chest_coordinates = eval(self.decode_settings()[3])

    def connect(self) -> str:
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data) -> str:
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
            return str(e)

    def decode_settings(self) -> list:
        return self.settings.split(":")
