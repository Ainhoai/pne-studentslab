from player0 import Player

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8081
c = Player(SERVER_IP, SERVER_PORT)
player_number = int(input(f"Please enter a valid number between 0-100:"))
