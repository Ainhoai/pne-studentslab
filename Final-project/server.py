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
    "/chromosomeLength": {"resource": "/info/assembly/", 'params': "content-type=application/json"},
    "/geneSeq": {"resource": "/sequence/id/", "params": "content-type=application/json"},
    "/geneInfo": {"resource": "/overlap/id/", "params": "content-type=application/json;feature=gene"},
    "/geneCalc": {"resource": "/sequence/id/", "params": "content-type=application/json"},
}  # this is how we are going to request what we want to ensemble's page.

RESOURCE_NOT_AVAILABLE_ERROR = "Resource not available"  # both of these are just in case of error.
ENSEMBL_COMMUNICATION_ERROR = "Error in communication with the Ensembl server."


def read_html_template(file_name):  # this function is to read the content of each html template.
    file_path = os.path.join(HTML_FOLDER, file_name)
    contents = Path(file_path).read_text()
    contents = jinja2.Template(contents)
    return contents


def server_request(server, url):
    error = False
    data = None
    try:
        connection = http.client.HTTPSConnection(server)
        connection.request("GET", url)  # petition
        response = connection.getresponse()
        if response.status == HTTPStatus.OK:
            json_str = response.read().decode()
            data = json.loads(json_str)
        else:
            error = True
    except Exception:  # Comment
        error = True
    return error, data


def handle_error(endpoint, message):
    context = {
        'endpoint': endpoint,
        'message': message
    }
    return read_html_template("error.html").render(context=context) # in case of error.


def list_species(endpoint, parameters):
    request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]  # send our request to ensemble, depending on what we are asking for it will take one or another rute.
    url = f"{request['resource']}?{request['params']}"  # this will be the url that will appear on the web.
    error, data = server_request(ENSEMBL_SERVER, url) # this should be error: False; data: (list/ dictionary from ensemble web).
    if not error: # if every thing goes ok.
        limit = None  # if i set none, it will get all the components of the list.
        if 'limit' in parameters: # because we are introducing a limit this is the rute it takes. "limit" is in params.
            limit = int(parameters['limit'][0])  # In order to get the integer that the user is setting in the web.
        species = data['species']  # list<dict> # inside the list that we are getting from ensemble, there is a dictionary and we are choosing to get "species" from all the datat.
        name_species = []  # empty list. we are creating it.
        for specie in species[:limit]:  # we are going through the whole list until we get to the limit chosen.
            name_species.append(specie['display_name'])  # we are adding to name_species (an empty dictionary) the species display name of all the species within the limit.
        context = { # we are creating a context so that the response on the website changes depending on what gets to the server. Non static that conects with html.
            'number_of_species': len(species),  # number in the list that the species occupies.
            'limit': limit,
            'name_species': name_species
        }
        contents = read_html_template("species.html").render(context=context) # this is how it connects with html and changes.
        code = HTTPStatus.OK
    else:
        contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
        code = HTTPStatus.SERVICE_UNAVAILABLE  # Comment
    return code, contents


def karyotype(endpoint, parameters):
    request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]  # connection to endpoint which is the petition to ensemble.
    species = parameters["species"][0]  # again we are creating a species variable to access to the parameters wanted.
    url = f"{request['resource']}{species}?{request['params']}" # this url changes a little because of how ensemble wants the petition to be done.
    error, data = server_request(ENSEMBL_SERVER, url) # error should be false; data should be ensembles database.
    print(data)
    if not error:
        context = {
            "species": species,  # we just need species name and karyotype: we accede through data.
            "karyotype": data["karyotype"]

        }
        contents = read_html_template("karyotype.html").render(context=context)
        code = HTTPStatus.OK
    else:
        contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
        code = HTTPStatus.SERVICE_UNAVAILABLE
    return code, contents


def chromosome_length(endpoint, parameters):
    request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint] # connecting to chromosome_length the way that ensemble wants
    species = parameters["species"][0]
    chromo = parameters["chromo"][0]  # dentro del formulario, necesitamos dos datos siendo species y chromosome.
    url = f"{request['resource']}{species}?{request['params']}"
    error, data = server_request(ENSEMBL_SERVER, url)
    print(data)
    if not error:
        chromosomes = data["top_level_region"]  # me devuleve todos los cromosomas de la especie. Es mi lista.
        c_length = None
        for c in chromosomes:
            if c["name"] == chromo: # si el diccionario c tiene como valor asociado "name" es igaual al chromosoma.
                c_length = c["length"]
                break  # para salir del bucle de forma abrupta.
        context = {
            "chromo": chromo,
            "length": c_length  # Lo que está entre comillas es el nombre que tiene que ser igual en el HTML.
        }
        contents = read_html_template("chromosome_length.html").render(context=context)
        code = HTTPStatus.OK
    else:
        contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
        code = HTTPStatus.SERVICE_UNAVAILABLE
    return code, contents


def get_id(gene):
    resource = "/homology/symbol/human/" + gene
    params = 'content-type=application/json;format=condensed'
    url = f"{resource}?{params}"
    error, data = server_request(ENSEMBL_SERVER, url)
    gene_id = None
    if not error:
        gene_id = data['data'][0]['id']
    return gene_id


def gene_seq(endpoint, parameters):
    gene = parameters['gene'][0]
    gene_id = get_id(gene)
    print(f"Gene: {gene} - Gene ID: {gene_id}")
    if gene_id is not None:
        request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
        url = f"{request['resource']}{gene_id}?{request['params']}"
        error, data = server_request(ENSEMBL_SERVER, url)
        if not error:
            print(data)
            bases = data['seq']
            context = {
                'gene': gene,
                'bases': bases
            }
            contents = read_html_template("gene_seq.html").render(context=context)
            code = HTTPStatus.OK
        else:
            contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
            code = HTTPStatus.SERVICE_UNAVAILABLE
    else:
        contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
        code = HTTPStatus.NOT_FOUND
    return code, contents


def gene_info(endpoint, parameters):
    gene = parameters["gene"][0]
    gene_id = get_id(gene)
    print(f"Gene: {gene} - Gene ID: {gene_id}")
    if gene_id is not None:
        request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
        url = f"{request['resource']}{gene_id}?{request['params']}"
        error, data = server_request(ENSEMBL_SERVER, url)
        if not error:
            print(data)
            data = data[0] # porque resulta que data es una lista con el diccionario dentro de esta lista. Tengo q acceder a la posicion 0 de la lista.
            start = data["start"]
            end = data["end"]
            length = end-start
            chromosome_name = data["assembly_name"]
            context = {
                "gene": gene,
                "start": start,
                "end": end,
                "length": length,
                "gene_id": gene_id,
                "chromosome_name": chromosome_name,
            }

            contents = read_html_template("gene_info.html").render(context=context)
            code = HTTPStatus.OK
        else:
            contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
            code = HTTPStatus.SERVICE_UNAVAILABLE
        return code, contents


def gene_calc(endpoint, parameters):
    gene = parameters['gene'][0]
    gene_id = get_id(gene)
    print(f"Gene: {gene} - Gene ID: {gene_id}")
    if gene_id is not None:
        request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
        url = f"{request['resource']}{gene_id}?{request['params']}"
        error, data = server_request(ENSEMBL_SERVER, url)
        if not error:
            print(data)
            sequence = data['seq']
            A = 0
            C = 0
            G = 0
            T = 0
            for b in sequence:
                if b == "A":
                    A += 1
                elif b == "C":
                    C += 1
                elif b == "G":
                    G += 1
                elif b == "T":
                    T += 1
            total_length = A + C + G + T
            base_A = round((A / total_length) * 100, 2)
            base_C = round((C / total_length) * 100, 2)
            base_G = round((G / total_length) * 100, 2)
            base_T = round((T / total_length) * 100, 2)

            context = {
                "gene": gene,
                "total_length": total_length,
                "A": base_A,
                "C": base_C,
                "G": base_G,
                "T": base_T
            }
            contents = read_html_template("gene_calc.html").render(context=context)
            code = HTTPStatus.OK
        else:
            contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
            code = HTTPStatus.SERVICE_UNAVAILABLE
        return code, contents


def gene_list(parameters):
    chromo = parameters["chromo"][0]
    start = int(parameters["start"][0])
    end = int(parameters["end"][0])
    resource = f"/overlap/region/human {chromo}: {start}-{end}"
    params = "content-type=application/json;feature=gene;feature=transcript;feature=cds;feature=exon"
    url = f"{resource}?{params}"
    error, data = server_request(ENSEMBL_SERVER, url)
    if not error:
        print(data)

        context = {
            "chromo": chromo,
            "start": start,
            "end": end,
        }
        contents = read_html_template("gene_calc.html").render(context=context)
        code = HTTPStatus.OK
    else:
        contents = handle_error(ENSEMBL_COMMUNICATION_ERROR)
        code = HTTPStatus.SERVICE_UNAVAILABLE
    return code, contents


socketserver.TCPServer.allow_reuse_address = True


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        parsed_url = urlparse(self.path)
        endpoint = parsed_url.path  # resource or path
        print(f"Endpoint: {endpoint}")
        parameters = parse_qs(parsed_url.query)  # arguments.
        print(f"Parameters: {parameters}")

        code = HTTPStatus.OK
        content_type = "text/html"
        contents = ""
        if endpoint == "/":
            file_path = os.path.join(HTML_FOLDER, "index.html")
            contents = Path(file_path).read_text()
        elif endpoint == "/listSpecies":
            code, contents = list_species(endpoint, parameters)
        elif endpoint == "/karyotype":  # fill them up. Create a function so that this code is more structured.
            code, contents = karyotype(endpoint, parameters)
        elif endpoint == "/chromosomeLength":
            code, contents = chromosome_length(endpoint, parameters)
        elif endpoint == "/geneSeq":
            code, contents = gene_seq(endpoint, parameters)
        elif endpoint == "/geneInfo":
            code, contents = gene_info(endpoint, parameters)
        elif endpoint == "/geneCalc":
            code, contents = gene_calc(endpoint, parameters)
        elif endpoint == "/geneList":
            code, contents = gene_list(parameters)
        else:
            contents = handle_error(endpoint, RESOURCE_NOT_AVAILABLE_ERROR)
            code = HTTPStatus.NOT_FOUND

        self.send_response(code)
        contents_bytes = contents.encode()
        self.send_header('Content-Type', content_type) # content_type is always text-html, in this practice.
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


