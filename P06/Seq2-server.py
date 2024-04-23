import http.server
from http import HTTPStatus   #contiene constantes con los valores de los codigos http
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import jinja2
import os
from Seq1 import Seq

PORT = 8080
HTML_FOLDER = "html"
SEQUENCES = ["CATGA", "TTACG", "AAAAA", "CGCGC", "TATAT"]
GENES = ["ADA", "FRAT1", "FXN", "RNU6_269P", "U5"]
OPERATIONS = ["info", "comp", "rev"]

def read_html_template(file_name):
    file_path = os.path.join(HTML_FOLDER, file_name) #recive el nombre de un fichero de dentri de la carpeta httml.
    contents = Path(file_path).read_text() #lee el fichero. Aqui es de tipo string.
    contents = jinja2.Template(contents) #me creo un objeto sobre el string, de la clase template con la variable contents. Sirve para crearme una plantilla dinamica.
    return contents #aqui ya es un objeto de tipo template.


def handle_get(arguments):  #para poner el codigo mas ordenado.
    try:
        sequence_number = int(arguments['sequence_number'][0])
        file_path = os.path.join(HTML_FOLDER, "get.html")
        contents = Path(file_path).read_text()
        contents = jinja2.Template(contents)
        context = {'number': sequence_number, 'sequence': SEQUENCES[sequence_number]}
        contents = contents.render(context=context)
        code = HTTPStatus.OK
    except (KeyError, IndexError, ValueError):
        file_path = os.path.join(HTML_FOLDER, "error.html")
        contents = Path(file_path).read_text()
        code = HTTPStatus.NOT_FOUND
    return contents, code


socketserver.TCPServer.allow_reuse_address = True


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler): #de donde tiene que heredar.
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green') #informacion

        parsed_url = urlparse(self.path) #trocea la ruta que recivo cuando el cliente hace una peticion.
        resource = parsed_url.path  # path
        print(f"Resource: {resource}")
        arguments = parse_qs(parsed_url.query) #devuelve un diccionario con los parametros que llegan en la peticion. Clave = [valor]
        print(f"Arguments: {arguments}")

        if resource == "/" or resource == "/index.html":
            contents = read_html_template("index.html")
            context = {'n_sequences': len(SEQUENCES), 'genes': GENES} #me estoy creando el diccionario. Conexion con el html.
            contents = contents.render(context=context) # contexto actualizate. Y es un string.
            self.send_response(200)
        elif resource == "/ping":
            file_path = os.path.join(HTML_FOLDER, "ping.html")
            contents = Path(file_path).read_text()
            self.send_response(200)
        elif resource == "/get":
            contents, code = handle_get(arguments)
            self.send_response(code)
        elif resource == "/gene":
            try:
                gene_name = arguments['gene_name'][0]
                file_path = os.path.join(HTML_FOLDER, "gene.html")
                contents = Path(file_path).read_text()
                contents = jinja2.Template(contents)
                file_name = os.path.join("..", "sequences", gene_name + ".txt")
                s = Seq()
                s.read_fasta(file_name)
                context = {'gene_name': gene_name, 'sequence': str(s)}
                contents = contents.render(context=context)
                self.send_response(200)
            except (KeyError, IndexError, FileNotFoundError):
                file_path = os.path.join(HTML_FOLDER, "error.html")
                contents = Path(file_path).read_text()
                self.send_response(404)
        elif resource == "/operation":
            try:
                bases = arguments['bases'][0]
                op = arguments['op'][0]  # lower()
                file_path = os.path.join(HTML_FOLDER, "operation.html")
                contents = Path(file_path).read_text()
                contents = jinja2.Template(contents)
                s = Seq(bases)
                if op in OPERATIONS:
                    if op == "info":
                        result = s.info().replace("\n", "<br><br>")
                    elif op == "comp":
                        result = s.complement()
                    else:  # elif op == "rev":
                        result = s.reverse()
                    context = {'sequence': str(s), 'op': op, 'result': result}
                    contents = contents.render(context=context)
                    self.send_response(200)
                else:
                    file_path = os.path.join(HTML_FOLDER, "error.html")
                    contents = Path(file_path).read_text()
                    self.send_response(404)
            except (KeyError, IndexError):
                file_path = os.path.join(HTML_FOLDER, "error.html")
                contents = Path(file_path).read_text()
                self.send_response(404)
        else:
            file_path = os.path.join(HTML_FOLDER, "error.html")
            contents = Path(file_path).read_text()
            self.send_response(404)

        contents_bytes = contents.encode()
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(contents_bytes)))
        self.end_headers()

        self.wfile.write(contents_bytes)


with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd: #programa principal
    print("Serving at PORT...", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Stopped by the user")
        httpd.server_close()
