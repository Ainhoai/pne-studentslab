import socket
import os
from Seq1 import Seq


IP = "127.0.0.1"
PORT = 8080
SEQUENCES = ["ADA", "FRAT1", "FXN", "RNU6_269P", "U5"]


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #para por si esta un port ocupado o habia sido ocupado antes que no de problema; es opcional.
try:
    server_socket.bind((IP, PORT))
    server_socket.listen()

    print("SEQ Server configure.")

    while True:  #aceptando all el rato conexiones de clientes.
        print(f"Waiting for clients ({IP}:{PORT})...")
        (client_socket, client_address) = server_socket.accept()

        request_bytes = client_socket.recv(2048) #cadena de caracteres con la peticion del cliente.
        request = request_bytes.decode("utf-8")

        response = None
        slices = request.split(" ")
        command = slices[0] #lista con la posicion 0 los comandos (PING; INFO; GET; etc) y en la uno la lista (AAGTTAG; etc). Aqui puedo poner .uppercase y asi cogeria el comando en minuscula tambien.
        print(command)

        if command == "PING":
            response = "Ok!\n"

        elif command == "GET":
            n = int(slices[1]) #para luego poder indexarla en genes.
            genes = SEQUENCES[n]
            s = Seq()
            filename = os.path.join("..", "sequences", genes + ".txt")  #esto lo pongo solo pq estoy usando las sequencias de una carpeta que estan predefinidas. Podria hacerlo con una lista de sequencias creada directamente en este codigo.
            s.read_fasta(filename)
            response = str(s)
        elif command == "INFO":
            bases = slices[1] #me guardo la sequencia. Posicion 0 es el comando "INFO".
            s = Seq(bases)
            response = s.info()

        elif command == "COMP":
            pass

        print(response)
        response_bytes = response.encode("utf-8")
        client_socket.send(response_bytes)
        client_socket.close()

except socket.error:
    print(f"Problems using port {PORT}. Do you have permission?")
except KeyboardInterrupt:
    print("Server stopped by the admin")
    server_socket.close()

