import json, Trailer, Hub, Consignment, Road

time = 1
trailers = ['tnt{}'.format(x) for x in range(15)]
cons = ['con{}'.format(x) for x in range(500)]

ath = Hub.Hub('Atherstone')
ath.roads.append(Road.Road('ath:kin'))
kin = Hub.Hub('Kingsbury')
for trailer in trailers:
    ath.trailers.append(Trailer.Trailer(trailer))
    ath.trailers[-1].origin = ath
    ath.trailers[-1].destination = kin
for con in cons:
    ath.cargo.append(Consignment.Consignment(con))


with open('manifest.txt', 'w') as text_file:
    while time <= 1000:
        if len(ath.cargo) > 0 and len(ath.trailers) > 0:
            # Loads the trailer
            ath.load_count += 1
            if ath.load_count == ath.load_time:
                ath.trailers[0].cargo.append(ath.cargo[0])
                ath.cargo.pop(0)
                ath.load_count = 0
            if len(ath.trailers[0].cargo) >= ath.trailers[0].capacity:
                # Sends off the trailer
                ath.trailers[0].travel(time)
                ath.roads[-1].trailers.append(ath.trailers[0])
                ath.trailers.pop(0)
    
        # Arrives the trailer
        for t in ath.roads[-1].check(time):
            t.destination.trailers.append(t)
            t.destination.trailers[-1].arrive(time)

        # Loads Hub
        if len(kin.trailers) > 0:
            for t in kin.trailers:
                if len(t.cargo) > 0:
                    t.status = 'loading'
                    break
            kin.load_count += 1
            if kin.load_count == kin.load_time:
                kin.cargo.append(t.cargo[0])
                t.cargo.pop(0)
                kin.load_count = 0


        time += 1
        if time % 10 == 0:
            print("""


Time: {}""".format(time), file=text_file)
            print('Ath: {}'.format(len(ath.cargo)), file=text_file)
            for a in range(len(ath.trailers)):
                print(ath.trailers[a].define(), file=text_file)
            print('Road', file=text_file)
            for i in range(len(ath.roads[0].trailers)):
                print(ath.roads[0].trailers[i].define(), file=text_file)
            print('Kin: {}'.format(len(kin.cargo)), file=text_file)
            for a in range(len(kin.trailers)):
                print(kin.trailers[a].define(), file=text_file)
    
        # Stops the loop when all has arrived
        if len(ath.trailers) == 0 and len(ath.roads[0].trailers) == 0:
            break