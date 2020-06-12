class Road(object):
    def __init__(self, name, x1, y1, x2, y2):
        self.name = name
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.trailers = []
        self.time_length = 82

    def __str__(self):
        return self.name

    def check(self, now):
        arrived = []
        done = []
        for t in range(len(self.trailers)):
            if now - self.trailers[t].dep_time >= self.time_length:
                arrived.append(self.trailers[t])
                done.append(t)
        done.reverse()
        for i in done:
            self.trailers.pop(i)

        return arrived
