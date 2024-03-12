
import socket
class Player:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __str__(self):
        return f"Connection to SERVER at {self.ip}, PORT: {self.port}"

    def ping(self):
        print("OK")

    def talk(self, msg):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        s.send(str.encode(msg))
        response = s.recv(2048).decode("utf-8")
        s.close()
        return response

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8081
c = Player(SERVER_IP, SERVER_PORT)
player_number = int(input(f"Please enter a valid number between 0-100:"))
