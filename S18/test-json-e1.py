import json
import termcolor
from pathlib import Path

json_string = Path("people-e1.json").read_text()
people = json.loads(json_string)['people']
for person in people:
    firstname = person['Firstname']
    lastname = person['Lastname']
    age = person['Age']
    phoneNumbers = person['PhoneNumbers']

    print()
    termcolor.cprint("Name: ", 'green', end="")
    print(firstname, lastname)
    termcolor.cprint("Age: ", 'green', end="")
    print(age)
    termcolor.cprint("Phone numbers: ", 'green', end='')
    print(len(phoneNumbers))

    for i, num in enumerate(phoneNumbers):
        termcolor.cprint("  Phone {}:".format(i), 'blue')
        termcolor.cprint("    Type: ", 'red', end='')
        print(num['type'])
        termcolor.cprint("    Number: ", 'red', end='')
        print(num['number'])