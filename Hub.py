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

    def send(self, time):
        if len(self.cargo) > 0 and len(self.trailers) > 0:
            # Loads the trailer
            self.trailers[0].load_count += 1
            self.trailers[0].state = 'loading'
            if self.trailers[0].load_count >= self.trailers[0].load_time:
                for c in range(len(self.cargo)):
                    if self.cargo[c].destination == self.trailers[0].destination:
                        self.trailers[0].cargo.append(self.cargo[c])
                        self.cargo.pop(c)
                        self.trailers[0].load_count = 0
                        break
            if len(self.trailers[0].cargo) >= self.trailers[0].capacity or (len(self.trailers) > 0 and len(self.cargo) == 0):
                # Sends off the trailer
                self.trailers[0].travel(time)
                self.roads[-1].trailers.append(self.trailers[0])
                self.trailers.pop(0)
        # Arrives the trailer
        for t in self.roads[-1].check(time):
            t.destination.trailers.append(t)
            t.destination.trailers[-1].arrive(time)

    def receive(self, time):
        # Loads Hub
        if len(self.trailers) > 0:
            for t in self.trailers:
                if len(t.cargo) > 0:
                    t.state = 'unloading'
                    break
                else:
                    t.state = 'waiting'
            if len(t.cargo) > 0:
                t.load_count += 1
                if t.load_count == t.load_time:
                    for c in range(len(t.cargo)):
                        if t.cargo[c].destination == self:
                            self.cargo.append(t.cargo[c])
                            t.cargo.pop(c)
                            t.load_count = 0
                            break

    def check(self):
        for con in self.cargo:
            if con.destination == self:
                con.delivered = True

        