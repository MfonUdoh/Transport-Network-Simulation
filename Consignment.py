class Consignment():
    def __init__(self, name):
        self.name = name
        self.origin = ''
        self.destination = ''
        self.delivered = False
    
    def __str__(self):
        return self.name

    def define(self):
        return {'name': self.name, 'destination':self.destination.name, 'delivered': self.delivered}