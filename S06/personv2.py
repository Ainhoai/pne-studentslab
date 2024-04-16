class Person: #clase padre
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f'Name{self.name}\nAge: {self.age}'

    def is_older(self):
        return self.age >= 18

class Student(Person):
    def __init__(self, name, age): #esto es una herencia, clase hija
        super().__init__(name, age) #desde el constructor de estudiante llamo al constructor de clase padre.
        self.scores = [] #como estas poniendo en la clase hija scores, solo aplica para estudiantes, esta clase.

    def add_score(self, score):
        self.scores.append(score)



p1 = Person("Elena", 18)
print(f"Is she older? {p1.is_older()}")
print(p1)


#HERENCIA--> pej. Anima es clase padre, perro es clase hija. En este ejemplo clase padre es persona y clase hija es estudiante.