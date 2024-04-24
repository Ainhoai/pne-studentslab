import json
import termcolor
from pathlib import Path

json_string = Path("people-2.json").read_text()
person = json.loads(json_string)

firstname = person['Firstname']
lastname = person['Lastname']
age = person['Age']
phoneNumbers = person['PhoneNumbers'] #una lista de python de string.

print()
termcolor.cprint("Name: ", 'green', end="")
print(firstname, lastname)
termcolor.cprint("Age: ", 'green', end="")
print(age)

termcolor.cprint("Phone numbers: ", 'green', end='')
print(len(phoneNumbers)) #numero de numeros en la lista de numeros de telefono.

for i, num in enumerate(phoneNumbers): #genera una nueva lista de tuplas donde almacena python la posicion y el valor correspondiente de cada numero de la lista.
    termcolor.cprint(f"  Phone {i}: ", 'blue', end='')
    print(num)