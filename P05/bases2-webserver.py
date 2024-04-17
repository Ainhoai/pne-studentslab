import http.server
import socketserver
import termcolor
from pathlib import Path
import os


PORT = 8080
socketserver.TCPServer.allow_reuse_address = True


class Myhandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, "green")

        resource = self.path
        resource_to_file = {"/": "index.html",
                            "/index.html": "index.html",
                            "/info/A.html": os.path.join("info", "A.html"),
                            "/info/C.html": os.path.join("info", "C.html"),
                            "/info/G.html": os.path.join("info", "G.html"),
                            "/info/T.html": os.path.join("info", "T.html")}

        file_name = resource_to_file.get(resource, resource[1:])
        file_path = os.path.join("html", file_name)

        try:
            body = Path(f"{file_path}").read_text()
            self.send_response(200)
        except FileNotFoundError:
            file_path = os.path.join("html", "error.html")
            body = Path(file_path).read_text()
            self.send_response(404)

        body_bytes = body.encode()
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(body_bytes)))
        self.end_headers()

        self.wfile.write(body_bytes)

        return


with socketserver.TCPServer(("", PORT), Myhandler) as httpd:
    print("Serving at PORT...", PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Stopped by the user")
        httpd.server_close()
print("DNA Bases Server configured!")
