from Seq1 import Seq

PRACTICE = 1
EXERCISE = 9
print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")



s = Seq()
FILENAME = ["U5.txt"]
print("Null sequence created.")
for i, s in enumerate(FILENAME):
    print(f"Sequence {i + 1}: (length: {s.len()}) {s}")
    print(f"\tBases: {s.count()}")
    print(f"\tRev: {s.reverse()}")
    print(f"\tComp: {s.complement()}")
s.read_fasta(FILENAME)
