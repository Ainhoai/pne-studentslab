from Seq1 import Seq

PRACTICE = 1
EXERCISE = 3
print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")
seq_list = [Seq(), Seq("ACTGA"), Seq("Invalid Sequence")]
for i, s in enumerate(seq_list):
    print(f"Sequence {i + 1}: {s}")