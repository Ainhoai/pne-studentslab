from pathlib import Path

bases = ["A", "C", "T", "G"]
bases_complement = {"A": "T", "T": "A", "C": "G", "G": "C"}


def seq_ping():
    print("OK")


def seq_read_fasta(filename):  #leer la sequencia
    file_content = Path(filename).read_text()
    lines = file_content.splitlines()  #divide el contenido en lineas
    body = lines[1:]
    "".join(body)
    return body


def seq_len(seq):
    return len(seq)


def seq_count_base(seq, base):
    return seq.count(base)


def seq_count(seq):
    base_appearances = {}
    for base in bases:
        base_appearances[base] = seq_count_base(seq, base)
    return base_appearances


def seq_reverse(seq, n):
    new_seq = seq[:n]
    return new_seq[::-1]


def seq_complement(seq):
    complement = ""
    for base in seq:
        complement += bases_complement[base]
    return complement

