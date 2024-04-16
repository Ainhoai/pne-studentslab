import http.server
import socketserver
import termcolor
from pathlib import Path

PORT = 8080
HTML_FOLDER = "html"

socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        contents = Path(f'{HTML_FOLDER}/form-1.html').read_text()

        self.send_response(200)

        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', f"{len(str.encode(contents))}")
        self.end_headers()

        self.wfile.write(str.encode(contents))

        return


with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
    print("Serving at PORT", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()

