import json, Trailer, Hub, Consignment, Road

time = 0
trailers = ['tnt{}'.format(x) for x in range(10)]
cons = ['con{}'.format(x) for x in range(20)]

ath = Hub.Hub('Atherstone')
ath.roads.append(Road.Road('ath:kin'))
kin = Hub.Hub('Kingsbury')
for trailer in trailers:
    ath.trailers.append(Trailer.Trailer(trailer))
    ath.trailers[-1].origin = ath
    ath.trailers[-1].destination = kin
    for con in cons:
        ath.trailers[-1].cargo.append(Consignment.Consignment(con))


with open('manifest.txt', 'w') as text_file:
    while time <= 100:
        if time % 20 == 0:
            ath.trailers[0].travel(time)
            ath.roads[-1].trailers.append(ath.trailers[0])
            ath.trailers.pop(0)
    
        for t in ath.roads[-1].check(time):
            t.destination.trailers.append(t)
            t.destination.trailers[-1].arrive(time)

        time += 1
        if time % 10 == 0:
            print("""


Time: {}""".format(time), file=text_file)
            print('Ath', file=text_file)
            for a in range(len(ath.trailers)):
                print(ath.trailers[a].define(), file=text_file)
            print('Road', file=text_file)
            for i in range(len(ath.roads[0].trailers)):
                print(ath.roads[0].trailers[i].define(), file=text_file)
            print('Kin', file=text_file)
            for a in range(len(kin.trailers)):
                print(kin.trailers[a].define(), file=text_file)