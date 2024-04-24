import json  #tengo herramientas.
import termcolor
from pathlib import Path

json_string = Path("people-1.json").read_text() #contenido de json en modo string.
person = json.loads(json_string) #para cargar el contenido del json en formato str en tipo diccionario.

firstname = person['Firstname']
lastname = person['Lastname']
age = person['Age']

print()
termcolor.cprint("Name: ", 'green', end="")
print(firstname, lastname)
termcolor.cprint("Age: ", 'green', end="")
print(age)