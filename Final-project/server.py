import http.server
from http import HTTPStatus
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs, quote
import jinja2
import requests

PORT = 8080
ensemble = "rest.ensemble.org"

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def read_html_template(self, file_name):
        file_path = Path("html") / file_name
        contents = Path(file_path).read_text()
        template = jinja2.Template(contents)
        return template

    def server_request(self, server, url):
        error = False
        data = None
        full_url = f"https://{server}{url}"
        try:
            response = requests.get(full_url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            error = True
            print(f"Request error: {e}")
        return error, data

    def handle_error(self, endpoint, message):
        template = self.read_html_template("error.html")
        return template.render(endpoint, message)

    def do_GET(self):
        parsed_url = urlparse(self.path)
        endpoint = parsed_url.path
        parameters = parse_qs(parsed_url.query)
        termcolor.cprint(self.requestline, 'green')

        if endpoint == "/":
            file_path = "html/index.html"
            file_contents = Path(file_path).read_text()
            self.send_response(200)

        elif endpoint == "/listSpecies":
            file_contents = self.list_species(endpoint, parameters)
            self.send_response(200)

        elif endpoint == "/karyotype":
            file_contents = self.karyotype(endpoint, parameters)
            self.send_response(200)

        elif endpoint == "/chromosomeLength":
            file_contents = self.chromosome_length(endpoint, parameters)
            self.send_response(200)

        elif endpoint == "/geneSeq":
            file_contents = self.gene_seq(endpoint, parameters)
            self.send_response(200)

        elif endpoint == "/geneInfo":
            file_contents = self.gene_info(endpoint, parameters)
            self.send_response(200)

        elif endpoint == "/geneCalc":
            file_contents = self.gene_calc(endpoint, parameters)
            self.send_response(200)

        elif endpoint == "/geneList":
            file_contents = self.gene_list(parameters)
            self.send_response(200)

        else:
            file_contents = self.handle_error(endpoint, "Resource not available")
            self.send_response(404)

        contents_bytes = file_contents.encode()
        self.send_header('Content-Type', "text/html")
        self.send_header('Content-Length', str(len(contents_bytes)))
        self.end_headers()
        self.wfile.write(contents_bytes)

    # Placeholder methods for the endpoints
    def list_species(self, endpoint, parameters):
        url = "/info/species/?content-type=application/json"
        error, data = self.server_request(ensemble, url)
        if not error:
            limit = None
            if 'limit' in parameters:
                limit = int(parameters['limit'][0])
            species = data['species']
            name_species = [specie['display_name'] for specie in species[:limit]]

            file_contents = self.read_html_template("species.html").render(number_of_species=len(species), limit=limit, name_species=name_species)
            code = HTTPStatus.OK
        else:
            file_contents = self.handle_error(endpoint," Error in communication with the Ensembl server")
            code = HTTPStatus.SERVICE_UNAVAILABLE

        return code, file_contents

    def karyotype(self, endpoint, parameters):
        species = quote(parameters["species"][0])
        url = f"/info/assembly/{species}?content-type=application/json"
        error, data = self.server_request(ensemble, url)

        if not error:
            karyotype = data.get("karyotype")
            species_name = species.replace("%20", " ")

            file_contents = self.read_html_template("karyotype.html").render(species=species_name, karyotype=karyotype)
            code = HTTPStatus.OK
        else:
            file_contents = self.handle_error(endpoint, " Error in communicating with ensemble.")
            code = HTTPStatus.SERVICE_UNAVAILABLE

        return code, file_contents

    def chromosome_length(self, endpoint, parameters):
        species = parameters["species"][0]
        chromo = parameters["chromo"][0]
        url = f"/info/assembly/{species}?content-type=application/json"
        error, data = self.server_request(ensemble, url)
        if not error:
            chromosomes = data["top_level_region"]
            c_length = None
            for c in chromosomes:
                if c["name"] == chromo:
                    c_length = c["length"]
                    break
            file_contents = self.read_html_template("chromosome_length.html").render(species=species, chromo=chromo,length=c_length)
            code = HTTPStatus.OK
        else:
            file_contents = self.handle_error(endpoint, "Error in communicating with ensemble.")
            code = HTTPStatus.SERVICE_UNAVAILABLE
        return code, file_contents

    def gene_seq(self, endpoint, parameters):
        gene = parameters['gene'][0]
        resource = f"/homology/symbol/human/{gene}"
        params = 'content-type=application/json;format=condensed'
        url = f"{resource}?{params}"
        error, data = self.server_request(ensemble, url)
        if not error:
            gene_id = data['data'][0]['id']
            url = f"/sequence/id/{gene_id}?content-type=application/json"
            error, data = self.server_request(ensemble, url)
            if not error:
                bases = data['seq']
                file_contents = self.read_html_template("gene_seq.html").render(gene=gene, bases=bases)
                code = HTTPStatus.OK
            else:
                file_contents = self.handle_error(endpoint, "Error communicating with ensemble.")
                code = HTTPStatus.SERVICE_UNAVAILABLE
        else:
            file_contents = self.handle_error(endpoint, "Error communicating with ensemble.")
            code = HTTPStatus.NOT_FOUND

        return code, file_contents

    def gene_info(self, endpoint, parameters):
        gene = parameters['gene'][0]
        resource = f"/homology/symbol/human/{gene}"
        params = 'content-type=application/json;format=condensed'
        url = f"{resource}?{params}"
        error, data = self.server_request(ensemble, url)
        if not error:
            gene_id = data['data'][0]['id']
            url = f"/sequence/id/{gene_id}?content-type=application/json;feature=gene"
            error, data = self.server_request(ensemble, url)
            if not error:
                data = data[0]
                start = data["start"]
                end = data["end"]
                length = end - start
                chromosome_name = data["assembly_name"]

                file_contents = self.read_html_template("gene_info.html").render(gene=gene, start=start, length=length, gene_if=gene_id, chromosome_name=chromosome_name)
                code = HTTPStatus.OK
            else:
                file_contents = self.handle_error(endpoint, "Error communicating with ensemble.")
                code = HTTPStatus.SERVICE_UNAVAILABLE
        else:
            file_contents = self.handle_error(endpoint, "Error communicating with ensemble.")
            code = HTTPStatus.NOT_FOUND
        return file_contents, code

    def gene_calc(self, endpoint, parameters):
        gene = parameters['gene'][0]
        resource = f"/homology/symbol/human/{gene}"
        params = 'content-type=application/json;format=condensed'
        url = f"{resource}?{params}"
        error, data = self.server_request(ensemble, url)
        if not error:
            gene_id = data['data'][0]['id']
            url = f"/sequence/id/{gene_id}?content-type=application/json"
            error, data = self.server_request(ensemble, url)
            if not error:
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
                a = round((A / total_length) * 100, 2)
                c = round((C / total_length) * 100, 2)
                g = round((G / total_length) * 100, 2)
                t = round((T / total_length) * 100, 2)

                file_contents = self.read_html_template("gene_calc.html").render(gene=gene,total_length=total_length, A=a,C=c, G=g, T=t)
                code = HTTPStatus.OK
            else:
                file_contents = self.handle_error(endpoint, "Error communicating with ensemble.")
                code = HTTPStatus.SERVICE_UNAVAILABLE
        else:
            file_contents = self.handle_error(endpoint, "Error communicating with ensemble.")
            code = HTTPStatus.NOT_FOUND

        return code, file_contents

    def gene_list(self, parameters):
        chromo = parameters["chromo"][0]
        start = int(parameters["start"][0])
        end = int(parameters["end"][0])
        endpoint = f"/overlap/region/human/{chromo}:{start}-{end}"
        params = "content-type=application/json;feature=gene;feature=transcript;feature=cds;feature=exon"
        url = f"{endpoint}?{params}"
        error, data = self.server_request(ensemble, url)
        if not error:
            data = data[0]
            chromo = int(data["seq_region_name"])
            start = data["start"]
            end = data["end"]
            genes_list = []
            for gene in data:
                if "external_name" in gene:
                    name = data["external_name"]
                    genes_list.append(name)
                    genes_list = genes_list[0]

            file_contents = self.read_html_template("gene_list.html").render(chromo=chromo, start=start, end=end, gene_list=genes_list)
            code = HTTPStatus.OK
        else:
            file_contents = self.handle_error(endpoint, "Error communicating with ensemble.")
            code = HTTPStatus.SERVICE_UNAVAILABLE
        return code, file_contents


with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Serving at PORT {PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Stopped by the user")
        httpd.server_close()


