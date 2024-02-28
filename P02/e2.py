from client0 import Client

PRACTICE = 2
EXERCISE = 2

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "212.128.255.98"
PORT = 8081

c = Client(IP, PORT)
print(c)
