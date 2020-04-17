class Hub(object):
    def __init__(self, name):
        self.name = name
        self.trailers = []
        self.roads = []

    def __str__(self):
        return self.name
