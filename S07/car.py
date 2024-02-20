class car:
    #  init is when you move an object to a class.
    def __init__(self, brand, speed = 0): #self is a parameter of all methos and it is always a parameter. It is the object of a class
        self.car_brand = brand #its an atribute, a variable attached to the object.
        self.speed = speed
        self.value = None
    def set_speed(self, speed):
        self.speed = speed
    def get_speed(self):
        return self.speed
    def get_brand_nationality(self):
        if self.car_brand == "Renault":
            return "France"
        elif self.car_brand == "Ferrari":
            return "Italy"
    def set_age(self, age):
        self.age = age
    def set_value(self, value):
        self.value = value

mycar = car("Renault", 30)
print(mycar.get_speed())
mycar.set_speed(80)
print(mycar.get_speed())
print(mycar.get_brand_nationality())

yourcar = car("Ferrari", 250)
print(yourcar.speed)

