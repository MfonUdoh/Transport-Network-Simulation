import json, random, numpy, Trailer, Hub, Consignment, Road

class Controller(object):
    def __init__(self, num_hubs, num_deps, num_cons):
        self.world = {
            'hubs'    :   {},
            'roads'   :   {}
        }
        self.time = 0
        self.create_hubs(num_hubs)
        self.create_cons(num_cons)

    def create_hubs(self, num_hubs):
        for hub in ['hub{}'.format(x) for x in range(num_hubs)]:
            self.world['hubs'][hub] = Hub.Hub(hub)
            self.world['hubs'][hub].x = random.random()
            self.world['hubs'][hub].y = random.random()

        for hubA in self.world['hubs']:
            dist = []
            for hubB in self.world['hubs']:
                distance = self.distance(self.world['hubs'][hubA].x, self.world['hubs'][hubA].y, self.world['hubs'][hubB].x, self.world['hubs'][hubB].y)
                if distance != 0 and hubB not in self.world['hubs'][hubA].connections:
                    dist.append([distance, hubB])

            connections = []
            number_connections = random.randint(1, 2)
            passes = 1
            while passes <= number_connections and dist != []:
                min = []
                for element in dist:
                    if min == [] or min[0] > element[0]:
                        min = [element[0], element[1], dist.index(element)]
                dist.pop(min[2])
                connections.append(min[1])
                self.world['hubs'][min[1]].connections.append(hubA)
                passes += 1
            
            for e in connections:
                self.world['hubs'][hubA].connections.append(e)
        
        for hub in self.world['hubs']:
            print(self.world['hubs'][hub].connections)

        for i in self.world['hubs']:
            for j in self.world['hubs']:
                if i != j:
                    self.world['roads']['{}:{}'.format(i, j)] = Road.Road('{}:{}'.format(i, j))
                    self.world['hubs'][i].park['Trailer{}:{}'.format(i, j)] = Trailer.Trailer('Trailer{}:{}'.format(i, j))

    def create_cons(self, num_cons):
        cons = ['con{}'.format(x) for x in range(num_cons*len(self.world['hubs']))]
        while cons != []:
            choice = random.choice(list(self.world['hubs'].values()))
            choice2 = random.choice(list(self.world['hubs'].values()))
            if choice != choice2:
                choice.cargo.append(Consignment.Consignment(cons[0], choice, choice2))
                cons.pop(0)

    def load_trailers(self):
        for hub in self.world['hubs']:
            for trailer in hub.park:
                if trailer.state == 'loading':
                    pass

    def sim(self):
        self.time += 1

    def distance(self, x1, y1, x2, y2):
        return numpy.sqrt(abs(x1 - x2)**2 + abs(y1 - y2)**2)

# time = 1
# trailers = ['tnt{}'.format(x) for x in range(15)]
# cons = ['con{}'.format(x) for x in range(750)]
# hubs = ['ath', 'kin', 'lount']
# places = []

# # Builds hubs
# for hub in hubs:
#     places.append(Hub.Hub(hub))

# # Builds roads between all the hubs
# for i in range(len(places)):
#     for j in range(len(places)):
#         if i != j:
#             places[i].roads.append(Road.Road('{}:{}'.format(places[i], places[j])))

# # Make trailers
# for trailer in trailers:
#     choice = random.choice([*places])
#     choice.trailers.append(Trailer.Trailer(trailer))
    
#     choice.trailers[-1].origin = choice
#     choice2 = choice
#     while choice == choice2:
#         choice2 = random.choice([*places])
#         choice.trailers[-1].destination = choice2

# # Make consignments
# for con in cons:
#     choice = random.choice([*places])
#     choice.cargo.append(Consignment.Consignment(con))
    
#     choice.cargo[-1].origin = choice
#     choice2 = choice
#     while choice == choice2:
#         choice2 = random.choice([*places])
#         choice.cargo[-1].destination = choice2

# run = True
# with open('manifest.txt', 'w') as text_file:
#     while run:
#         for hub in places:
#             hub.send(time)
#         for hub in places:
#             hub.receive(time)

#         time += 1
#         if time % 10 == 0:
#             print("""


# Time: {}""".format(time), file=text_file)
#             for hub in places:
#                 print('{}: {}'.format(hub.name, len(hub.cargo)), file=text_file)
#                 for trailer in range(len(hub.trailers)):
#                     print(hub.trailers[trailer].define(), file=text_file)
#                 for i in range(len(hub.roads)):
#                     print('Road {}'.format(hub.roads[i]), file=text_file)
#                     for j in range(len(hub.roads[i].trailers)):
#                         print(hub.roads[i].trailers[j].define(), file=text_file)
#                 print("", file=text_file)
    
#         # Stops the loop when all has arrived
#         if time == 2000:
#             run = False
    
# for hub in places:
#     hub.check()
#     print("")
#     print(hub.name)
#     for trailer in hub.trailers:
#         if trailer.dep_time == -1:
#             print(trailer.define())
