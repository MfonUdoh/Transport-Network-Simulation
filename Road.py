import numpy
class Road(object):
    def __init__(self, name, x1, y1, x2, y2):
        self.name = name
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.trailers = []
        self.length = numpy.sqrt(abs(x1 - x2)**2 + abs(y1 - y2)**2)
        self.time_length = self.length*1000

    def __str__(self):
        return self.name

    def positions(self, now):
        for trailer in self.trailers:
            amount_completed = (now - trailer.dep_time)/(self.time_length)
            dx = self.x2 - self.x1
            dy = self.y2 - self.y1
            trailer.x = self.x1 + dx * amount_completed
            trailer.y = self.y1 + dy * amount_completed

    def arrive(self, now):
        check = True
        while check:
            check = False
            for trailer in self.trailers:
                if trailer.dep_time + self.time_length <= now:
                    trailer.x = trailer.destination.x
                    trailer.y = trailer.destination.y
                    trailer.destination.park[trailer] = trailer
                    self.trailers.remove(trailer)
                    check = True
                    break
