import http.server
from http import HTTPStatus
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import jinja2
import json
import requests
import http.client

PORT = 8080
server = "rest.ensemble.org"


class RequestHandler(http.server.BaseHTTPRequestHandler):
    def read_html_template(self, file_name):
        file_path = Path("html/" + file_name)
        file_contents = Path(file_path).read_text()
        file_contents = jinja2.Template(file_contents)
        return file_contents

    def server_request(self, file_name):
        endpoint = file_name + "?content-type=application/json"
        connection = http.client.HTTPConnection(server)
        try:
            connection.request("GET", endpoint)
        except ConnectionRefusedError:
            print("Error connecting to the server.")
            exit()
        response = connection.getresponse()
        print(f"Response received!: {response.status} {response.reason}\n")
        if response.status == HTTPStatus.OK:
            data_str = response.read().decode("utf-8")
            data = json.loads(data_str)
            return data

    def do_GET(self):
        parsed_url = urlparse(self.path)
        endpoint = parsed_url.path
        parameters = parse_qs(parsed_url.query)
        termcolor.cprint(self.requestline, 'green')

        if endpoint == "/":
            file_path = "html/index.html"
            file_contents = Path(file_path).read_text()
            code = 200

        elif endpoint == "/listSpecies":
            code, file_contents = self.list_species(parameters)

        elif endpoint == "/karyotype":
            code, file_contents = self.karyotype(parameters)

        elif endpoint == "/chromosomeLength":
            code, file_contents = self.chromosome_length(parameters)

        elif endpoint == "/geneSeq":
            code, file_contents = self.gene_seq(parameters)

        elif endpoint == "/geneInfo":
            code, file_contents = self.gene_info(parameters)

        elif endpoint == "/geneCalc":
            code, file_contents = self.gene_calc(parameters)

        elif endpoint == "/geneList":
            code, file_contents = self.gene_list(parameters)

        else:
            file_contents = self.read_html_template("error.html")
            code = 404

        file_contents = str(file_contents)
        file_contents = file_contents.encode()
        self.send_response(code)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(file_contents))
        self.end_headers()
        self.wfile.write(file_contents)

    # Placeholder methods for the endpoints
    def list_species(self, parameters):
        try:
            url = f"https://rest.ensembl.org/info/species?"
            headers = {"content-type": "application/json"}
            response = requests.get(url, headers=headers)
            data = response.json()

            name_species = []
            species = data['species']
            for specie in species:
                name_species.append(specie['display_name'])
            if "limit" in parameters:
                limit = parameters.get("limit")[0]
                if limit is not None:
                    limit_name_species = name_species[:int(limit)]
                else:
                    limit_name_species = name_species
            else:
                limit = "No limit has been selected"
                limit_name_species = name_species

            context = {
                'number_of_species': len(species),
                'limit': limit,
                'name_species': limit_name_species}

            file_contents = self.read_html_template("species.html").render(context=context)
            code = HTTPStatus.OK

        except (KeyError, IndexError):
            file_contents = self.read_html_template("error.html")
            code = HTTPStatus.SERVICE_UNAVAILABLE

        return code, file_contents

    def karyotype(self, parameters):
        try:
            species = parameters.get('species')[0]
            url = f"https://rest.ensembl.org/info/assembly/{species}?"
            headers = {"Content-Type": "application/json"}
            response = requests.get(url, headers=headers)
            data = response.json()
            karyotype = data["karyotype"]

            context = {"species": species,
                       "karyotype": karyotype}
            file_contents = self.read_html_template("karyotype.html").render(context=context)
            code = HTTPStatus.OK

        except KeyError:
            file_contents = self.read_html_template("error.html")
            code = HTTPStatus.SERVICE_UNAVAILABLE

        return code, file_contents

    def chromosome_length(self, parameters):
        try:
            species = parameters.get('species')[0]
            chromo = parameters.get("chromo")[0]
            url = f"https://rest.ensembl.org/info/assembly/{species}?"
            headers = {"Content-Type": "application/json"}
            response = requests.get(url, headers=headers)
            data = response.json()

            chromosomes = data["top_level_region"]
            c_length = None
            for c in chromosomes:
                if c["name"] == chromo:
                    c_length = c["length"]
                    break

            context = {"species": species,
                       "chromo": chromo,
                       "length": c_length}

            file_contents = self.read_html_template("chromosome_length.html").render(context=context)
            code = HTTPStatus.OK

        except KeyError:
            file_contents = self.read_html_template("error.html")
            code = HTTPStatus.SERVICE_UNAVAILABLE
        return code, file_contents

    def gene_seq(self, parameters):
        try:
            gene = parameters.get('gene')[0]
            url = f"https://rest.ensembl.org/lookup/symbol/homo_sapiens/{gene}?"
            headers = {"Content-Type": "application/json;format=condensed"}
            response = requests.get(url, headers=headers)
            data = response.json()

            gene_id = data['id']
            url = f"https://rest.ensembl.org/sequence/id/{gene_id}?"
            headers = {"Content-Type": "application/json;format=gene"}
            response = requests.get(url, headers=headers)
            data = response.json()

            bases = data['seq']
            context = {"gene": gene,
                       "bases": bases}

            file_contents = self.read_html_template("gene_seq.html").render(context=context)
            code = HTTPStatus.OK

        except KeyError:
            file_contents = self.read_html_template("error.html")
            code = HTTPStatus.SERVICE_UNAVAILABLE

        return code, file_contents

    def gene_info(self, parameters):
        try:
            gene = parameters.get('gene')[0]
            url = f"https://rest.ensembl.org/lookup/symbol/homo_sapiens/{gene}?"
            headers = {"Content-Type": "application/json;format=condensed"}
            response = requests.get(url, headers=headers)
            data = response.json()

            gene_id = data['id']
            url = f"https://rest.ensembl.org/overlap/id/{gene_id}?feature=gene;"
            headers = {"Content-Type": "application/json"}
            response = requests.get(url, headers=headers)
            data = response.json()

            start = data[0]["start"]
            end = data[0]["end"]
            length = end - start
            chromosome_name = data[0]["seq_region_name"]
            context = {"gene": gene,
                       "start": start,
                       "end": end,
                       "length": length,
                       "gene_id": gene_id,
                       "chromosome_name": chromosome_name}

            file_contents = self.read_html_template("gene_info.html").render(context=context)
            code = HTTPStatus.OK
        except KeyError:
            file_contents = self.read_html_template("error.html")
            code = HTTPStatus.SERVICE_UNAVAILABLE

        return code, file_contents

    def gene_calc(self, parameters):
        try:
            gene = parameters.get('gene')[0]
            url = f"https://rest.ensembl.org/lookup/symbol/homo_sapiens/{gene}?"
            headers = {"Content-Type": "application/json;format=condensed"}
            response = requests.get(url, headers=headers)
            data = response.json()

            gene_id = data['id']
            url = f"https://rest.ensembl.org/sequence/id/{gene_id}?"
            headers = {"Content-Type": "application/json;format=gene"}
            response = requests.get(url, headers=headers)
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

            context = {"gene": gene,
                       "total_length": total_length,
                       "A": A,
                       "C": C,
                       "G": G,
                       "T": T}

            file_contents = self.read_html_template("gene_calc.html").render(context=context)
            code = HTTPStatus.OK

        except KeyError:
            file_contents = self.read_html_template("error.html")
            code = HTTPStatus.SERVICE_UNAVAILABLE
        return code, file_contents

    def gene_list(self, parameters):
        try:
            chromo = parameters["chromo"][0]
            start = int(parameters["start"][0])
            end = int(parameters["end"][0])
            url = (f"https://rest.ensembl.org/overlap/region/human/{chromo}:{start}-{end}?"
                   f"feature=gene;feature=transcript;feature=cds;feature=exon")
            headers = {"Content-Type": "application/json;"}
            response = requests.get(url, headers=headers)
            data = response.json()

            genes_list = []
            for gene in data:
                if "external_name" in gene:
                    name = gene["assembly_name"]
                    genes_list.append(name)

            context = {"chromo": chromo,
                       "start": start,
                       "end": end,
                       "gene_list": genes_list}

            file_contents = self.read_html_template("gene_list.html").render(context=context)
            code = HTTPStatus.OK

        except KeyError:
            file_contents = self.read_html_template("error.html")
            code = HTTPStatus.SERVICE_UNAVAILABLE

        return code, file_contents


with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Serving at PORT {PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Stopped by the user")
        httpd.server_close()
