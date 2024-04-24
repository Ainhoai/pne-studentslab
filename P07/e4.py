import http.client
import json
from http import HTTPStatus
from seq import Seq #trabajo con la clase seq.

GENES = {
    "FRAT1": "ENSG00000165879",
    "ADA": "ENSG00000196839",
    "FXN": "ENSG00000165060",
    "RNU6_269P": "ENSG00000212379",
    "MIR633": "ENSG00000207552",
    "TTTY4C": "ENSG00000228296",
    "RBMY2YP": "ENSG00000227633",
    "FGFR3": "ENSG00000068078",
    "KDR": "ENSG00000128052",
    "ANK2": "ENSG00000145362"
}

print()
gene = input("Write the gene name: ") #introducimos el nombre de un gen. Este ejercicio hace exactamente lo mismo que el 3, pero yo le estoy pidiendo un gen.
if gene in GENES: #compruebo si es valido el gen que le estoy pidiendo.
    SERVER = 'rest.ensembl.org'
    RESOURCE = f'/sequence/id/{GENES[gene]}' #identificador.
    PARAMS = '?content-type=application/json'
    URL = SERVER + RESOURCE + PARAMS

    print()
    print(f"SERVER: {SERVER}")
    print(f"URL: {URL}")

    conn = http.client.HTTPConnection(SERVER)

    try:
        conn.request("GET", RESOURCE + PARAMS)
    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()

    response = conn.getresponse()
    print(f"Response received!: {response.status} {response.reason}\n")
    if response.status == HTTPStatus.OK:
        data_str = response.read().decode("utf-8")
        data = json.loads(data_str)
        print(f"Gene: {gene}")
        print(f"Description: {data['desc']}")
        bases = data['seq'] #coger las bases de la sequencia y crearnos una sequencia nuestra de la clase seq.
        s = Seq(bases)
        print(s.info()) #funcion de la clase seq.