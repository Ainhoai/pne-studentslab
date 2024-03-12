from client0 import Client

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080

c = Client(SERVER_IP, SERVER_PORT)
response = c.talk("PING")
print(response)
response = c.talk("GET 2")
print(response)
response = c.talk("INFO AACCGTA")
print(response)
response = c.talk("COMP AACCGTA")
print(response)
print(c.talk("REV AACCGTA"))
print(response)
response = c.talk("GENE U5")
print(response)