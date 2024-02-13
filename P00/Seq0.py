from pathlib import Path
def seq_ping():
    print("OK")
def seq_read_fasta(filename):
    first_line = Path(filename).read_text().find("\n")
    body = Path(filename).read_text()[first_line:]
    body = body.replace("\n", "")
    return body

def seq_len(seq):
    first_line = Path(seq).read_text().find("\n")
    body = Path(seq).read_text()[first_line:]
    body = body.replace("\n", "")
    return len(body)

def seq_count_base(seq, base):
    first_line = Path(seq).read_text().find("\n")
    body = Path(seq).read_text()[first_line:]
    body = body.replace("\n", "")
    base = len(body)
    return base


def seq_count(seq):
    k
def seq_reverse(seq, n):
    seq = seq[::-1]
    return seq[:n]


def seq_complement(seq):



