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
        if len(self.trailers) > 0 and len(self.cargo) > 0:
            for t in self.trailers:
                if len(self.cargo) > 0:
                    if self.cargo[0].destination == t.destination:
                        t.load_count += 1
                        t.state = 'loading'
                        if t.load_count >= t.load_time:
                            t.cargo.append(self.cargo[0])
                            t.wait_time = time
                            self.cargo.pop(0)
                # Loads the trailer
                # if len(self.cargo) > 0 and len(self.trailers) > 0:
                #     self.trailers[0].load_count += 1
                #     self.trailers[0].state = 'loading'
                #     if self.trailers[0].load_count >= self.trailers[0].load_time:
                #         for c in range(len(self.cargo)):
                #             if self.cargo[c].destination == self.trailers[0].destination:
                #                 self.trailers[0].cargo.append(self.cargo[c])
                #                 self.cargo.pop(c)
                #                 self.trailers[0].load_count = 0
                #                 break
                    
                    if len(t.cargo) >= t.capacity:
                        # Sends off the trailer if it is full
                        t.travel(time)
                        for road in self.roads:
                            if road.name == "{}:{}".format(self.name, t.destination.name):
                                road.trailers.append(t)
                                for j in range(len(self.trailers)):
                                    if self.trailers[j] == t:
                                        self.trailers.pop(j)
                                        break
                                break
                    elif t.destination.name not in [self.cargo[x].destination.name for x in range(len(self.cargo))]:
                        # Sends of trailer if there are no more packages for it
                        t.travel(time)
                        for road in self.roads:
                            if road.name == "{}:{}".format(self.name, t.destination.name):
                                road.trailers.append(t)
                                for j in range(len(self.trailers)):
                                    if self.trailers[j] == t:
                                        self.trailers.pop(j)
                                        break
                                break

        # Arrives the trailer
        for road in range(len(self.roads)):
            for t in self.roads[road].check(time):
                t.destination.trailers.append(t)
                t.destination.trailers[-1].arrive(time)

    def receive(self, time):
        # Loads Hub
        if len(self.trailers) > 0:
            for t in self.trailers:
                if len(t.cargo) > 0 and t.destination == self:
                    t.state = 'unloading'
                    t.unload_count += 1
                    if t.unload_count == t.load_time:
                        for c in range(len(t.cargo)):
                            if t.cargo[c].destination == self:
                                self.cargo.append(t.cargo[c])
                                t.cargo.pop(c)
                                t.unload_count = 0
                                break
                    break

    def check(self):
        for con in self.cargo:
            if con.destination == self:
                con.delivered = True
