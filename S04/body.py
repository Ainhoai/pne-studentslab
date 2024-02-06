from pathlib import Path
FILENAME = "U5.txt"
file_contents = Path(FILENAME).read_text()
list_contents = file_contents.split("\n")
for i in range(1, len(list_contents)):
    print(list_contents[i])

