# -- Example of a client that uses the HTTP.client library
# -- for requesting the main page from the server
import http.client

PORT = 8080
SERVER = 'localhost'

print(f"\nConnecting to server: {SERVER}:{PORT}\n")

# How to crate connection with the server.
conn = http.client.HTTPConnection(SERVER, PORT)

# -- Send the request message, using the GET method. We are
# -- requesting the main page (/)
try:
    conn.request("GET", "/") #haciendo la peticion al cliente.
except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()

# -- Read the response message from the server
r1 = conn.getresponse() #r1 es un objeto de la clase HTTPResponse.

# -- Print the status line
print(f"Response received!: {r1.status} {r1.reason}\n") #pinta el numero del codigo (200, 404) y luego el texto asociado a es codigo (OK o not found).

# -- Read the response's body
data1 = r1.read().decode("utf-8") #esto lee el self.wfile.write(contents_bytes) del servidor en bytes y los decodifica.

# -- Print the received data
print(f"CONTENT: {data1}")
