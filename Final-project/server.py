import http.server
from http import HTTPStatus
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs, quote
import jinja2
import requests

PORT = 8080
ensemble = "https://rest.ensemble.org"

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def read_html_template(self, file_name):
        file_path = Path("html") / file_name
        contents = Path(file_path).read_text()
        template = jinja2.Template(contents)
        return template

    def handle_error(self, endpoint, message):
        template = self.read_html_template("error.html")
        return template.render(endpoint, message)

    def do_GET(self):
        parsed_url = urlparse(self.path)
        endpoint = parsed_url.path
        parameters = parse_qs(parsed_url.query)
        termcolor.cprint(self.requestline, 'green')

        if endpoint == "/":
            file_path = "/index.html"
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
            file_contents = self.gene_list(endpoint, parameters)
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
        try:
            url = "/info/species/?content-type=application/json"
            response = requests.get(ensemble, url)
            response.raise_for_status()
            data = response.json()

            species = data.get('species')
            limit = None
            if 'limit' in parameters:
                limit = int(parameters['limit'][0])
                for specie in species[:limit]:
                    name_species = specie['display_name']

            file_contents = self.read_html_template("species.html").render(number_of_species=len(species), limit=limit, name_species=name_species)
            code = HTTPStatus.OK

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            file_contents = self.handle_error(endpoint, "Error in communication with the Ensembl server")
            code = HTTPStatus.SERVICE_UNAVAILABLE

        return code, file_contents

    def karyotype(self, endpoint, parameters):
        try:
            species = parameters.get('species', [''])[0]
            url = f"/info/assembly/{quote(species)}?content-type=application/json"
            response = requests.get(ensemble, url)
            response.raise_for_status()
            data = response.json()

            karyotype = data.get("karyotype")
            species_name = species.replace("%20", " ")

            file_contents = self.read_html_template("karyotype.html").render(species=species_name, karyotype=karyotype)
            code = HTTPStatus.OK

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            file_contents = self.handle_error(endpoint, "Error in communicating with ensemble.")
            code = HTTPStatus.SERVICE_UNAVAILABLE

        return code, file_contents

    def chromosome_length(self, endpoint, parameters):
        try:
            species = parameters.get('species', [''])[0]
            chromo = parameters.get("chromo", [''])[0]
            url = f"/info/assembly/{species}?content-type=application/json"

            response = requests.get(ensemble, url)
            response.raise_for_status()
            data = response.json()

            chromosomes = data.get("top_level_region", [])
            c_length = None
            for c in chromosomes:
                if c["name"] == chromo:
                    c_length = c["length"]
                    break

            file_contents = self.read_html_template("chromosome_length.html").render(species=species, chromo=chromo, length=c_length)
            code = HTTPStatus.OK

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            file_contents = self.handle_error(endpoint, "Error in communicating with ensemble.")
            code = HTTPStatus.SERVICE_UNAVAILABLE
        return code, file_contents

    def gene_seq(self, endpoint, parameters):
        try:
            gene = parameters.get('gene')[0]
            url = f"/homology/symbol/human/{gene}?content-type=application/json;format=condensed"
            response = requests.get(ensemble, url)
            response.raise_for_status()
            data = response.json()

            gene_id = data['data'][0]['id']
            url = f"/sequence/id/{gene_id}?content-type=application/json"
            response = requests.get(ensemble, url)
            response.raise_for_status()
            data = response.json()

            bases = data['seq']
            file_contents = self.read_html_template("gene_seq.html").render(gene=gene, bases=bases)
            code = HTTPStatus.OK

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            file_contents = self.handle_error(endpoint, "Error in communicating with ensemble.")
            code = HTTPStatus.SERVICE_UNAVAILABLE

        return code, file_contents

    def gene_info(self, endpoint, parameters):
        try:
            gene = parameters.get('gene')[0]
            url = f"/homology/symbol/human/{gene}?content-type=application/json;format=condensed"
            response = requests.get(ensemble, url)
            response.raise_for_status()
            data = response.json()

            gene_id = data['data'][0]['id']
            url = f"/sequence/id/{gene_id}?content-type=application/json;feature=gene"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            data = data[0]
            start = data["start"]
            end = data["end"]
            length = end - start
            chromosome_name = data["assembly_name"]
            file_contents = self.read_html_template("gene_info.html").render(gene=gene, start=start, length=length, gene_if=gene_id, chromosome_name=chromosome_name)
            code = HTTPStatus.OK

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            file_contents = self.handle_error(endpoint, "Error in communicating with ensemble.")
            code = HTTPStatus.SERVICE_UNAVAILABLE

        return code, file_contents

    def gene_calc(self, endpoint, parameters):
        try:
            gene = parameters.get('gene')[0]
            url = f"/homology/symbol/human/{gene}?content-type=application/json;format=condensed"
            response = requests.get(ensemble, url)
            response.raise_for_status()
            data = response.json()

            gene_id = data['data'][0]['id']
            url = f"/sequence/id/{gene_id}?content-type=application/json"
            response = requests.get(ensemble, url)
            response.raise_for_status()
            data = response.json()

            sequence = data['seq']
            nucleotide_counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
            total_length = len(sequence)
            for b in sequence:
                if b in nucleotide_counts:
                    nucleotide_counts[b] += 1

                A = round((nucleotide_counts['A'] / total_length) * 100, 2)
                C = round((nucleotide_counts['C'] / total_length) * 100, 2)
                G = round((nucleotide_counts['G'] / total_length) * 100, 2)
                T = round((nucleotide_counts['T'] / total_length) * 100, 2)

            file_contents = self.read_html_template("gene_calc.html").render(gene=gene,total_length=total_length, A=A, C=C, G=G, T=T)
            code = HTTPStatus.OK

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            file_contents = self.handle_error(endpoint, "Error in communicating with ensemble.")
            code = HTTPStatus.SERVICE_UNAVAILABLE
        return file_contents, code

    def gene_list(self, endpoint, parameters):
        try:
            chromo = parameters["chromo"][0]
            start = int(parameters["start"][0])
            end = int(parameters["end"][0])

            url = f"/overlap/region/human/{chromo}:{start}-{end}?content-type=application/json;feature=gene;feature=transcript;feature=cds;feature=exon"
            response = requests.get(ensemble, url)
            response.raise_for_status()
            data = response.json()

            genes_list = []
            for gene in data:
                if "external_name" in gene:
                    name = gene["external_name"]
                    genes_list.append(name)

            file_contents = self.read_html_template("gene_list.html").render(chromo=chromo, start=start, end=end, gene_list=genes_list)
            code = HTTPStatus.OK

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            file_contents = self.handle_error(endpoint, "Error in communicating with ensemble.")
            code = HTTPStatus.SERVICE_UNAVAILABLE

        return file_contents, code


with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Serving at PORT {PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Stopped by the user")
        httpd.server_close()


