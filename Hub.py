class Hub(object):
    def __init__(self, name):
        self.name = name
        self.trailers = []
        self.roads = []
        self.cargo = []
        self.load_count = 0
        self.load_time = 3

    def __str__(self):
        return self.name
