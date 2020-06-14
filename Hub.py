import random
class Hub(object):
    def __init__(self, name):
        self.name = name
        self.trailers = []
        self.connections = []
        self.roads = {}
        self.cargo = []
        self.deliveredBin = []
        self.park = {}
        self.loadingBay = {}
        self.unloadingBay = {}

    def __str__(self):
        return self.name

    def unload(self):
        for trailer in self.unloadingBay:
            if not self.unloadingBay[trailer].empty():
                self.unloadingBay[trailer].cargo[0].update_journey(self.name)
                if self.unloadingBay[trailer].cargo[0].destination == self:
                    self.deliveredBin.append(self.unloadingBay[trailer].cargo[0])
                    self.unloadingBay[trailer].cargo.pop(0)
                else:
                    self.cargo.append(self.unloadingBay[trailer].cargo[0])
                    self.unloadingBay[trailer].cargo.pop(0)
    
    def load(self):
        if not self.empty():
            choice = random.choice(self.cargo)
            for trailer in self.loadingBay:
                if not self.loadingBay[trailer].full():
                    if choice.nextStop == self.loadingBay[trailer].destination.name:
                        self.loadingBay[trailer].cargo.append(choice)
                        self.cargo.remove(choice)
                        break


    def shunt(self):
        """Moves the trailers around within the hub to their required locations"""

        # First move the trailers from the arrival parks to unloading bay
        for trailer in self.park:
            if self.park[trailer].destination == self:
                self.unloadingBay[trailer] = self.park[trailer]
                self.park.pop(trailer)
                break
            elif self.park[trailer].origin == self and (any([(con.nextStop == self.park[trailer].destination.name) for con in self.cargo]) or any([(con.nextStop == self.name) for con in self.park[trailer].destination.cargo])):
                self.loadingBay[trailer] = self.park[trailer]
                self.park.pop(trailer)
                break

        # Secondly move unloaded trailers back to park
        for trailer in self.unloadingBay:
            if self.unloadingBay[trailer].empty():
                self.park[trailer] = self.unloadingBay[trailer]
                self.park[trailer].destination = self.park[trailer].origin
                self.park[trailer].origin = self
                self.unloadingBay.pop(trailer)
                break

    def launch(self, now):
        """Launch trailers onto the road"""

        for trailer in self.loadingBay:
            if self.loadingBay[trailer].full() or (not self.loadingBay[trailer].empty() and not any([con.nextStop == self.loadingBay[trailer].destination.name for con in self.cargo])) or (not any([con.nextStop == self.loadingBay[trailer].destination.name for con in self.cargo]) and any([(con.nextStop == self.name) for con in self.loadingBay[trailer].destination.cargo])):
                self.loadingBay[trailer].dep_time = now
                self.roads[self.loadingBay[trailer].destination.name].trailers.append(self.loadingBay[trailer])
                self.loadingBay.pop(trailer)
                break

    def full(self):
        if len(self.cargo) >= self.capacity:
            return True
        else:
            return False

    def empty(self):
        if len(self.cargo) == 0:
            return True
        else:
            return False