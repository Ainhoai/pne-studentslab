import http.server
import socketserver
import termcolor
from pathlib import Path
import os #operative system

PORT = 8080
HTML_FOLDER = "html" #constante que determina donde tengo la carpeta con el cofigo HTML

socketserver.TCPServer.allow_reuse_address = True #reutilizar la direccion.


class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self): #solo sabe contestar al cliente con el formulario independientemente de lo que el cliente le mande.
        termcolor.cprint(self.requestline, "green")

        file_path = os.path.join(HTML_FOLDER, "form-1.html")
        contents = Path(file_path).read_text()

        self.send_response(200)

        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', f"{len(str.encode(contents))}")
        self.end_headers()

        self.wfile.write(str.encode(contents))  #enviar al cliente la respuesta.

        return


with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
    print("Serving at PORT", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()

