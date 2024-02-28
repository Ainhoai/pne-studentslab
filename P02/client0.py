class Client:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT


    def ping(self):
        print("Ok!")


    def __str__(self):

        return f"Connection to SERVER at {self.IP}, PORT: {self.PORT}"

    def talk(self, socket, msg):
        pass

