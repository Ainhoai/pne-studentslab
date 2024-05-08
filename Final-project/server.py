import http.server
from http import HTTPStatus
import socketserver
import termcolor
from pathlib import Path
import http.client
from urllib.parse import urlparse, parse_qs
import jinja2
import os
import json


PORT = 8080
HTML_FOLDER = "html"
ENSEMBL_SERVER = "rest.ensembl.org"
RESOURCE_TO_ENSEMBL_REQUEST = {
    '/listSpecies': {'resource': "/info/species", 'params': "content-type=application/json"},
    "/karyotype": {"resource": "/info/assembly/", 'params': "content-type=application/json"},
    "/chromosomeLength": {"resource": "/info/assembly/", 'params': "content-type=application/json"}
}
RESOURCE_NOT_AVAILABLE_ERROR = "Resource not available"
ENSEMBL_COMMUNICATION_ERROR = "Error in communication with the Ensembl server"


def read_html_template(file_name):
    file_path = os.path.join(HTML_FOLDER, file_name)
    contents = Path(file_path).read_text()
    contents = jinja2.Template(contents)
    return contents


def server_request(server, url):
    error = False
    data = None
    try:
        connection = http.client.HTTPSConnection(server)
        connection.request("GET", url)
        response = connection.getresponse()
        if response.status == HTTPStatus.OK:
            json_str = response.read().decode()
            data = json.loads(json_str)
        else:
            error = True
    except Exception:
        error = True
    return error, data


def handle_error(endpoint, message):
    context = {
        'endpoint': endpoint,
        'message': message
    }
    return read_html_template("error.html").render(context=context)


def list_species(endpoint, parameters):
    request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
    url = f"{request['resource']}?{request['params']}"
    error, data = server_request(ENSEMBL_SERVER, url)
    if not error:
        limit = None
        if 'limit' in parameters:
            limit = int(parameters['limit'][0])
        species = data['species']
        name_species = []
        for specie in species[:limit]:
            name_species.append(specie['display_name'])
        context = {
            'limit': limit,
            'name_species': name_species
        }
        contents = read_html_template("species.html").render(context=context)
        code = HTTPStatus.OK
    else:
        contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
        code = HTTPStatus.SERVICE_UNAVAILABLE
    return code, contents


def karyotype(endpoint, parameters):
    request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
    species = parameters["species"][0]
    url = f"{request['resource']}{species}?{request['params']}"
    print(data)
    if not error:
        context = {
            "species": species,
            "karyotype": data["karyotype"]

        }
        contents = read_html_template("karyotype.html").render(context=context)
        code = HTTPStatus.OK
    else:
        contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
        code = HTTPStatus.SERVICE_UNAVAILABLE
    return code, contents


def chromosome_length(endpoint, parameters):
    request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
    species = parameters["species"][0]
    chromo = parameters["chromo"][0]
    url = f"{request['resource']}{species}?{request['params']}"
    error, data = server_request(ENSEMBL_SERVER, url)
    print(data)
    if not error:
        chromosomes = data["top_level_region"]
        c_length = None
        for c in chromosomes:
            if c["name"] == chromo:
                c_length = c["length"]
                break
        context = {
            "chromo": chromo,
            "length": c_length
        }
        contents = read_html_template("chromosome_length.html").render(context=context)
        code = HTTPStatus.OK
    else:
        contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
        code = HTTPStatus.SERVICE_UNAVAILABLE
    return code, contents


socketserver.TCPServer.allow_reuse_address = True


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        parsed_url = urlparse(self.path)
        endpoint = parsed_url.path
        print(f"Endpoint: {endpoint}")
        parameters = parse_qs(parsed_url.query)
        print(f"Parameters: {parameters}")

        code = HTTPStatus.OK
        content_type = "text/html"
        contents = ""
        if endpoint == "/":
            file_path = os.path.join(HTML_FOLDER, "index.html")
            contents = Path(file_path).read_text()
        elif endpoint == "/listSpecies":
            code, contents = list_species(endpoint, parameters)
        elif endpoint == "/karyotype":
            code, contents = karyotype(endpoint, parameters)
        elif endpoint == "/chromosomeLength":
            code, contents = chromosome_length(endpoint, parameters)
        else:
            contents = handle_error(endpoint, RESOURCE_NOT_AVAILABLE_ERROR)
            code = HTTPStatus.NOT_FOUND

        self.send_response(code)
        contents_bytes = contents.encode()
        self.send_header('Content-Type', content_type)
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


