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
}

RESOURCE_NOT_AVAILABLE_ERROR = "Resource not available"
ENSEMBL_COMMUNICATION_ERROR = "Error in communication with the Ensembl server."


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
            'number_of_species': len(species),
            'limit': limit,
            'name_species': name_species
        }
        contents = read_html_template("species.html").render(context=context)
        code = HTTPStatus.OK
    else:
        contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
        code = HTTPStatus.SERVICE_UNAVAILABLE  # Comment
    return code, contents


def karyotype(endpoint, parameters):
    request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
    species = parameters["species"][0]
    url = f"{request['resource']}{species}?{request['params']}"
    error, data = server_request(ENSEMBL_SERVER, url)
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
            "species": species,
            "chromo": chromo,
            "length": c_length
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
            data = data[0]
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
    endpoint = f"/overlap/region/human/{chromo}:{start}-{end}"
    params = "content-type=application/json;feature=gene;feature=transcript;feature=cds;feature=exon"
    url = f"{endpoint}?{params}"
    error, data = server_request(ENSEMBL_SERVER, url)
    if not error:
        print(data)
        data = data[0]
        chromo = data["seq_region_name"]
        start = data["start"]
        end = data["end"]
        gene_list = []
        for c in range(start, end + 1):
            if "assembly_name" in data:
                name = data["assembly_name"]
                gene_list.append(name)
        context = {
            "chromo": chromo,
            "start": start,
            "end": end,
            "gene_list": gene_list[0]
        }
        contents = read_html_template("gene_list.html").render(context=context)
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


