import socket

SERVER_PORT = 8081
SERVER_IP = ""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((SERVER_IP, SERVER_PORT))

# Send data. No strings can be sent, only bytes
# It necessary to encode the string into bytes
s.send(str.encode("HELLO FROM THE CLIENT!!!"))

# Close the socket
s.close()