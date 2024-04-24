import http.client
import json
from http import HTTPStatus #clase dentro del modulo HTTP que contiene varias constantes.

SERVER = 'rest.ensembl.org'
RESOURCE = '/info/ping'
PARAMS = '?content-type=application/json' #parametros de la peticion. Esto es lo que va en la http en el navegador.
URL = SERVER + RESOURCE + PARAMS #tots los ingredientes de la url.

print() #linea en blanco.
print(f"SERVER: {SERVER}")
print(f"URL: {URL}")

conn = http.client.HTTPConnection(SERVER) #crea conexion con el servidor. Utiliza el puerto por defecto de http (80).

try:
    conn.request("GET", RESOURCE + PARAMS)
except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()

response = conn.getresponse() #esto es r1 en S18
print(f"Response received!: {response.status} {response.reason}\n")
if response.status == HTTPStatus.OK: #para saber si la peticion ha ido como debia.
    data_str = response.read().decode("utf-8") #tod el final es para tratar con json.
    data = json.loads(data_str) #me hago una idea de como tengo el diccionario
    ping = data['ping']
    if ping == 1:
        print("PING OK! The database is running!")
    else:
        print("...")