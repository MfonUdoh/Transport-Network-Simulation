import json, random, Trailer, Hub, Consignment, Road

time = 1
trailers = ['tnt{}'.format(x) for x in range(20)]
cons = ['con{}'.format(x) for x in range(500)]
hubs = ['ath', 'kin', 'lount']
places = []

# Builds hubs
for hub in hubs:
    places.append(Hub.Hub(hub))

# Builds roads between all the hubs
for i in range(len(places)):
    for j in range(len(places)):
        if i != j:
            places[i].roads.append(Road.Road('{}:{}'.format(places[i], places[j])))

# Make trailers
for trailer in trailers:
    choice = random.choice([*places])
    choice.trailers.append(Trailer.Trailer(trailer))
    
    choice.trailers[-1].origin = choice
    choice2 = choice
    while choice == choice2:
        choice2 = random.choice([*places])
        choice.trailers[-1].destination = choice2

# Make consignments
for con in cons:
    choice = random.choice([*places])
    choice.cargo.append(Consignment.Consignment(con))
    
    choice.cargo[-1].origin = choice
    choice2 = choice
    while choice == choice2:
        choice2 = random.choice([*places])
        choice.cargo[-1].destination = choice2

run = True
with open('manifest.txt', 'w') as text_file:
    while run:
        for hub in places:
            hub.send(time)
        for hub in places:
            hub.receive(time)

        time += 1
        if time % 10 == 0:
            print("""


Time: {}""".format(time), file=text_file)
            for hub in places:
                print('{}: {}'.format(hub.name, len(hub.cargo)), file=text_file)
                for trailer in range(len(hub.trailers)):
                    print(hub.trailers[trailer].define(), file=text_file)
                print('Road---', file=text_file)
                for i in range(len(hub.roads)):
                    for j in range(len(hub.roads[i].trailers)):
                        print(hub.roads[i].trailers[j].define(), file=text_file)
                print("", file=text_file)
    
        # Stops the loop when all has arrived
        if time == 2000:
            run = False
    
for hub in places:
    hub.check()
    for con in hub.cargo:
        print(con.define())
