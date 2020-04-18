class Road(object):
    def __init__(self, name):
        self.name = name
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
