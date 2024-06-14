import http.server
from http import HTTPStatus
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import jinja2
import requests

PORT = 8080


class RequestHandler(http.server.BaseHTTPRequestHandler):
    def read_html_template(self, file_name):

        file_path = Path("html") / file_name
        file_contents = Path(file_path).read_text()
        file_contents = jinja2.Template(file_contents)
        return file_contents

    def do_GET(self):
        parsed_url = urlparse(self.path)
        endpoint = parsed_url.path
        parameters = parse_qs(parsed_url.query)
        termcolor.cprint(self.requestline, 'green')
        code = HTTPStatus.OK

        if endpoint == "/":
            file_path = "html/index.html"
            try:
                file_contents = Path(file_path).read_text()
                self.send_response(200)
            except FileNotFoundError:
                self.send_error(HTTPStatus.NOT_FOUND, "File Not Found")
                return

        elif endpoint == "/listSpecies":
            file_contents, code = self.list_species(parameters)

        elif endpoint == "/karyotype":
            file_contents, code = self.karyotype(parameters)

        elif endpoint == "/chromosomeLength":
            file_contents, code = self.chromosome_length(parameters)

        elif endpoint == "/geneSeq":
            file_contents, code = self.gene_seq(parameters)

        elif endpoint == "/geneInfo":
            file_contents, code = self.gene_info(parameters)

        elif endpoint == "/geneCalc":
            file_contents, code = self.gene_calc(parameters)

        elif endpoint == "/geneList":
            file_contents, code = self.gene_list(parameters)

        else:
            file_contents = self.read_html_template("error.html")
            self.send_response(404)

        self.send_response(code)
        contents_bytes = file_contents.encode()
        self.send_header('Content-Type', "text/html")
        self.send_header('Content-Length', str(len(contents_bytes)))
        self.end_headers()
        self.wfile.write(contents_bytes)

    # Placeholder methods for the endpoints
    def list_species(self, parameters):
        try:
            url = f"https://rest.ensembl.org/info/species?"
            headers = {"content-type": "application/json"}
            response = requests.get(url, headers=headers)
            data = response.json()

            species = data.get('species')
            names = []
            limit = None
            if 'limit' in parameters:
                limit = int(parameters['limit'][0])
                for specie in species[:limit]:
                    names = specie['display_name']

            file_contents = self.read_html_template("species.html").render(species=species,
                                                                           number_of_species=len(species), limit=limit,
                                                                           name_species=names)
            code = HTTPStatus.OK

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            file_contents = self.read_html_template("error.html")
            code = HTTPStatus.SERVICE_UNAVAILABLE

        return code, file_contents

    def karyotype(self, parameters):
        try:
            species = parameters.get('species')[0]
            url = f"https://rest.ensembl.org/info/assembly/{species}"
            headers = {"Content-Type": "application/json"}
            response = requests.get(url, headers=headers)
            data = response.json()
            karyotype = data["karyotype"]

            file_contents = self.read_html_template("karyotype.html").render(species=species, karyotype=karyotype)
            code = HTTPStatus.OK

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            file_contents = self.read_html_template("error.html")
            code = HTTPStatus.SERVICE_UNAVAILABLE

        return code, file_contents

    def chromosome_length(self, parameters):
        try:
            species = parameters.get('species')[0]
            chromo = parameters.get("chromo")[0]
            url = f"/rest.ensembl.org/info/assembly/{species}"
            headers = {"Content-Type": "application/json"}
            response = requests.get(url, headers=headers)
            data = response.json()

            chromosomes = data.get("top_level_region", [])
            c_length = None
            for c in chromosomes:
                if c["name"] == chromo:
                    c_length = c["length"]
                    break

            file_contents = self.read_html_template("chromosome_length.html").render(species=species, chromo=chromo,
                                                                                     length=c_length)
            code = HTTPStatus.OK

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            file_contents = self.read_html_template("error.html")
            code = HTTPStatus.SERVICE_UNAVAILABLE
        return code, file_contents

    def gene_seq(self, parameters):
        try:
            gene = parameters.get('gene')[0]
            url = f"http://rest.ensembl.org/homology/symbol/human/{gene}?content-type=application/json;format=condensed"
            response = requests.get(url)
            data = response.json()

            gene_id = data['data'][0]['id']
            url = f"http://rest.ensembl.org/sequence/id/{gene_id}?content-type=application/json"
            response = requests.get(url)
            data = response.json()

            bases = data['seq']
            file_contents = self.read_html_template("gene_seq.html").render(gene=gene, bases=bases)
            code = HTTPStatus.OK

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            file_contents = self.read_html_template("error.html")
            code = HTTPStatus.SERVICE_UNAVAILABLE

        return code, file_contents

    def gene_info(self, parameters):
        try:
            gene = parameters.get('gene')[0]
            url = (f"https://rest.ensembl.org/homology/symbol/human/{gene}"
                   f"?content-type=application/json;format=condensed")
            response = requests.get(url)
            data = response.json()

            gene_id = data['data'][0]['id']
            url = f"https://rest.ensembl.org/sequence/id/{gene_id}?content-type=application/json;feature=gene"
            response = requests.get(url)
            data = response.json()
            print(data)

            start = data["start"]
            end = data["end"]
            length = end - start
            chromosome_name = data["assembly_name"]
            file_contents = self.read_html_template("gene_info.html").render(gene=gene, start=start, length=length,
                                                                             gene_if=gene_id,
                                                                             chromosome_name=chromosome_name)
            code = HTTPStatus.OK

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            file_contents = self.read_html_template("error.html")
            code = HTTPStatus.SERVICE_UNAVAILABLE

        return code, file_contents

    def gene_calc(self, parameters):
        try:
            gene = parameters.get('gene')[0]
            url = (f"https://rest.ensembl.org/homology/symbol/human/{gene}?"
                   f"content-type=application/json;format=condensed")
            response = requests.get(url)
            data = response.json()

            gene_id = data['data'][0]['id']
            url = f"https://rest.ensembl.org/sequence/id/{gene_id}?content-type=application/json"
            response = requests.get(url)
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

            file_contents = self.read_html_template("gene_calc.html").render(gene=gene,
                                                                             total_length=total_length, A=A,
                                                                             C=C, G=G, T=T)
            code = HTTPStatus.OK

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            file_contents = self.read_html_template("error.html")
            code = HTTPStatus.SERVICE_UNAVAILABLE
        return file_contents, code

    def gene_list(self, parameters):
        try:
            chromo = parameters["chromo"][0]
            start = int(parameters["start"][0])
            end = int(parameters["end"][0])

            url = (f"https://rest.ensembl.org/overlap/region/human/{chromo}:{start}-{end}"
                   f"?content-type=application/json;feature=gene;feature=transcript;feature=cds;feature=exon")
            response = requests.get(url)
            data = response.json()

            genes_list = []
            for gene in data:
                if "external_name" in gene:
                    name = gene["external_name"]
                    genes_list.append(name)

            file_contents = self.read_html_template("gene_list.html").render(chromo=chromo, start=start, end=end,
                                                                             gene_list=genes_list)
            code = HTTPStatus.OK

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            file_contents = self.read_html_template("error.html")
            code = HTTPStatus.SERVICE_UNAVAILABLE

        return file_contents, code


with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Serving at PORT {PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Stopped by the user")
        httpd.server_close()
