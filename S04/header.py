from pathlib import Path
FILENAME = "RNU6_269P.txt"
file_contents = Path(FILENAME).read_text()
list_contents = file_contents.split("\n")

print(list_contents[0])
