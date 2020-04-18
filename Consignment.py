class Consignment():
    def __init__(self, name):
        self.name = name
        self.origin = ''
        self.destination = ''
    
    def __str__(self):
        return self.name