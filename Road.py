import numpy
class Road(object):
    def __init__(self, name, x1, y1, x2, y2):
        self.name = name
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.trailers = []
        self.time_length = numpy.sqrt(abs(x1 - x2)**2 + abs(y1 - y2)**2)*500

    def __str__(self):
        return self.name

    def arrive(self, now):
        check = True
        while check:
            check = False
            for trailer in self.trailers:
                if trailer.dep_time + self.time_length >= now:
                    trailer.destination.park[trailer] = trailer
                    self.trailers.remove(trailer)
                    check = True
                    break
