from pathlib import Path

bases = ["A", "C", "T", "G"]
bases_complement = {"A": "T", "T": "A", "C": "G", "G": "C"}
def seq_ping():
    print("OK")

def seq_read_fasta(filename):
    file_content = Path(filename).read_text()
    lines = file_content.splitlines()
    body = lines[1:]
    "".join(body)
    return body

def seq_len(seq):
    return len(seq)
def seq_count_base(seq, base):
    return seq.count(base)

def seq_count(seq):
    base_apperances = {}
    for base in bases:
        base_apperances[base] = seq_count_base(seq, base)
    return base_apperances

def seq_reverse(seq, n):
    new_seq = seq[:n]
    return new_seq[::-1]

def seq_complement(seq):
    complement = ""
    for base in seq:
        complement += bases_complement[base]
    return complement




