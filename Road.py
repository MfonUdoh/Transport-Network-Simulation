class Road(object):
    def __init__(self, name):
        self.name = name
        self.trailers = []
        self.time_length = 87

    def __str__(self):
        return self.name

    def check(self, now):
        arrived = []
        done = []
        for t in range(len(self.trailers)):
            if now - self.trailers[t].dep_time >= self.time_length:
                arrived.append(self.trailers[t])
                done.append(t)

        for d in done:        
            self.trailers.pop(d)

        return arrived
