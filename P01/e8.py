from Seq1 import Seq

PRACTICE = 1
EXERCISE = 8
print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

seq_list = [Seq(), Seq("ACTGA"), Seq("Invalid Sequence")]
for i, s in enumerate(seq_list):
    print(f"Sequence {i + 1}: (length: {s.len()}) {s}")
    print(f"\tBases: {s.count()}")
    print(f"\tRev: {s.reverse()}")
    print(f"\tComp: {s.complement()}")
