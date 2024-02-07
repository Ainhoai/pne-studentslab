from Seq0 import *
folder = "../sequences/"
filename = "U5.txt"
print("DNA file : ", filename)
body = seq_read_fasta(folder + filename)
print("These are the first 20 bases:", body[0:20])
