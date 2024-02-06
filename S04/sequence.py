from pathlib import Path
FILENAME = "ADA.txt"
file_contents = Path(FILENAME).read_text()
list_contents = file_contents.split("\n")
list_contents.pop(0) #to remove header

print(len(''.join(list_contents))) #to joim all the items of a list in the same str.
