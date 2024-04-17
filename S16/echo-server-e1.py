import http.server
import socketserver
import termcolor
import os
from pathlib import Path
from urllib.parse import urlparse, parse_qs   #para tratar le peticion del cliente de forma mas sencilla. El parse es un submodulo dentro de urllib; para tratar url.
# del modulo me importo dos funciones que son urlparse, parse_qs.
import jinja2 as j   #generar una pagina web de forma dinamica. El as es para poder usar j en vex de jinja2.


def read_html_file(filename):
    file_path = os.path.join(HTML_FOLDER, filename) #construye la ruta al fichero
    contents = Path(file_path).read_text() #lee el contenido de path
    contents = j.Template(contents) #j es alias de jinja 2, con una clase que es una plantilla y le paso el contenido que es un str con el contenido de html el de result-echo...
    return contents  #ya no es un str, es un objeto de tipo plantilla con el codigo html.


PORT = 8080
HTML_FOLDER = "html"

socketserver.TCPServer.allow_reuse_address = True


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        url_path = urlparse(self.path) #lleva el recurso que solicite el cliente
        resource = url_path.path
        print(f"Path: {resource}")
        arguments = parse_qs(url_path.query) #consulta, me devuelve un resultado almacenado en argumento. Me convierte el mensaje en un diccionario con {msg: [msg]}, y me genera una lista.
        print(f"Arguments: {arguments}")
        if resource == "/":
            file_path = os.path.join(HTML_FOLDER, "form-e1.html")
            contents = Path(file_path).read_text()
            self.send_response(200)
        elif resource == "/echo":
            try:
                msg_param = arguments['msg'][0]  #arguements["msg"] devuelve una lista con el mensaje; ahora sobre esta lista cojo la posicion 0.
                print(msg_param)
                contents = read_html_file("result-echo-server-e1.html").render(context={"todisplay": msg_param})
                            #la funcion de arriba la uso aqui. Objeto de tipo plantilla que contiene el html; render es refrescar, actualizar, es un metodo de la clase template de jinja 2. Contiene lo mismo que el html, que es un diccionario que contiene una clave.

                # contents = f"""       #esto seria la primera version pero no va a ser la mejor opcion.
                #     <!DOCTYPE html>
                #     <html lang="en">
                #         <head>
                #             <meta charset="utf-8">
                #             <title>Result</title>
                #         </head>
                #         <body>
                #             <h1>Received message:</h1>
                #             <p>{msg_param}</p> #esto no es estatico, es variable pq dependiendo del mensaje que tu envies te responde con el mensaje que tu has enviado; no es el mismo siempre.
                #             <a href="/">Main page</a>
                #         </body>
                #     </html>"""

                self.send_response(200)
            except (KeyError, IndexError):
                file_path = os.path.join(HTML_FOLDER, "format-e1.html")
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


with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("Serving at PORT...", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Stopped by the user")
        httpd.server_close()