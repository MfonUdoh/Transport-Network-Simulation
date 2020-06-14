import numpy
class Road(object):
    def __init__(self, name, x1, y1, x2, y2, speed):
        self.name = name
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.trailers = []
        self.length = numpy.sqrt(abs(x1 - x2)**2 + abs(y1 - y2)**2)
        self.time_length = self.length*1000/speed

    def __str__(self):
        return self.name

    def positions(self, now):
        for trailer in self.trailers:
            if trailer.prev_time == -1:
                trailer.prev_time = trailer.dep_time
            amount_completed = (now - trailer.prev_time)/(self.time_length)
            trailer.prev_time = now
            dx = self.x2 - self.x1
            dy = self.y2 - self.y1
            trailer.x = dx * amount_completed
            trailer.y = dy * amount_completed

    def arrive(self, now):
        check = True
        while check:
            check = False
            for trailer in self.trailers:
                if trailer.dep_time + self.time_length <= now:
                    trailer.x = trailer.destination.x
                    trailer.y = trailer.destination.y
                    trailer.prev_time = -1
                    trailer.destination.park[trailer] = trailer
                    self.trailers.remove(trailer)
                    check = True
                    break
