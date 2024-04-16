import http.server
import socketserver


PORT = 8080

socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.requestline)


        if self.path == "/":
            contents = "Welcome to my server"
            self.send_response(200)
        else:
            self.send_response(404)
            contents = "Resource not available"

        contents_bytes = contents.encode()
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', str(len(contents_bytes)))
        self.end_headers()

        self.wfile.write(contents_bytes)

        return


with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
    print("Serving at PORT...", PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Stopped by the user")
        httpd.server_close()