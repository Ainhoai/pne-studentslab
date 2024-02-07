from Seq0 import *
folder = "../sequences/"
filename = "U5.txt"
print("DNA file : ", filename)
body = seq_read_fasta(folder + filename)
print("The first 20 bases are:", body[0:20])
