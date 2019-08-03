import random, math

def generateElements():
    names = {
            "prefix" : [
                "abing", "aber", "bark", "berry", "chelms", "car", "wood","strem", "ling", "spack",
                "trem", "mug", "deck", "tillin", "nod", "mabb", "golling", "miad", "ebbing", "nike",
                "dell"
        ],
            "suffix" : [
                "shire", "ton", "don", "ford", "cester", "ley", "e"
            ]
    }

    mapWidth = 100
    mapLength = 100

    hubs_list = {
        "carley" : {
            "location" : {"x" : int(mapWidth*.42), "y" : int(mapLength*.73)}, 
            "available_depots" : []
        },
        "gollingshire" : {
            "location" : {"x" : int(mapWidth*.95), "y" : int(mapLength*.21)}, 
            "available_depots" : []
        },
        "spack" : {
            "location" : {"x" : int(mapWidth*.10), "y" : int(mapLength*.11)}, 
            "available_depots" : []
        },
        "kingsbury" : {
            "location" : {"x" : int(mapWidth*.15), "y" : int(mapLength*.14)},
            "available_depots" : []
        },
        "diddley" : {
            "location" : {"x" : int(mapWidth*.24), "y" : int(mapLength*.5)},
            "available_depots" : []
        },
        "tuddle" : {
            "location" : {"x" : int(mapWidth*.7), "y" : int(mapLength*.80)},
            "available_depots" : []
        },
        "lount" : {
            "location" : {"x" : int(mapWidth*.55), "y" : int(mapLength*.22)},
            "available_depots" : []
        }
    }


    depots_list = {}
    for hub in hubs_list:
        for dep in range(6):
            dx, dy = (mapWidth/10), (mapWidth/10)
            while ((dx**2 + dy**2) > (mapWidth/10)**2) or (hubs_list[hub]['location']['x'] + dx not in range(mapWidth + 1)) or (hubs_list[hub]['location']['y'] + dy not in range(mapLength + 1)):
                (dx, dy) = (random.randrange(-(mapWidth/10),(mapWidth/10)), random.randrange(-(mapLength/10),(mapLength/10)))
            depotname = ""
            while depotname not in depots_list:
                choice = random.choice(range(1,4))
                if choice == 1:
                    depotname = random.choice(names["prefix"])
                    break
                if choice == 2:
                    depotname = random.choice(names["prefix"]) + random.choice(names["suffix"])
                    break
                if choice == 3:
                    depotname = random.choice(names["prefix"]) + random.choice(names["prefix"]) + random.choice(names["suffix"])
                    break
            depots_list.update({depotname : {"location" : {"x" : hubs_list[hub]['location']['x'] + dx, "y" : hubs_list[hub]['location']['y'] + dy}, "available_hubs" : []}})

    for depot in depots_list:
        for hub in hubs_list:
            if (depots_list[depot]["location"]["x"] - hubs_list[hub]['location']['x'])**2 + (depots_list[depot]["location"]["y"] - hubs_list[hub]['location']['y'])**2 <= (mapWidth/10)**2:
                depots_list[depot]["available_hubs"].append(hub)
                hubs_list[hub]["available_depots"].append(depot)

    num_cons = 100*len(depots_list)
    cons_list = {}
    for i in range(num_cons+1):
        while True:
            origin = random.choice([*depots_list])
            destination = random.choice([*depots_list])
            if origin != destination:
                break 
        conName = "con" + str(i)
        cons_list.update(
            {conName : {
                "origin" : origin, 
                "destination" : destination,
                "path" : [],
                "distance" : 0
            }})

    with open("Hubs.txt", "w") as text_file:
        for hub in hubs_list:
            print(f"Hub Name: {hub}", file=text_file)
            print("Hub Location: {}".format(hubs_list[hub]["location"]), file=text_file)
            print("Hub Available Depots: {}".format(hubs_list[hub]["available_depots"]), file=text_file)
            print(f"", file=text_file)

    with open("Depots.txt", "w") as text_file:
        for depot in depots_list:
            print(f"Depot Name: {depot}", file=text_file)
            print("Depot Location: {}".format(depots_list[depot]["location"]), file=text_file)
            print("Depot Available Hubs: {}".format(depots_list[depot]["available_hubs"]), file=text_file)
            print(f"", file=text_file)

    return hubs_list, depots_list, cons_list

hubs_list, depots_list, cons_list = generateElements()

# TODO generate the optimal paths

# 1. For origin and destination, make a ranked list of all the hubs, by distance.
# 2. Then rank them by combined distance from origin and destination.
# 3. First hub is first in combined rank in available hubs for origin
# 4. Check if available depots for hub is destination, if so end, else, select next on rankec list


for con in cons_list:
    sorter = []
    for hub in hubs_list:
        startDepot = cons_list[con]["origin"]
        Origin = depots_list[startDepot]
        targetDepot = cons_list[con]["destination"]
        Destination = depots_list[targetDepot]
        Hub = hubs_list[hub]
        distanceToOrigin = (Hub["location"]["x"] - Origin["location"]["x"])**2 + (Hub["location"]["y"] - Origin["location"]["y"])**2
        distanceToDestination = (Hub["location"]["x"] - Destination["location"]["x"])**2 + (Hub["location"]["y"] - Destination["location"]["y"])**2
        sorter.append([hub, distanceToOrigin + distanceToDestination])
    def takeSecond(elem):
        return elem[1]
    sorter.sort(key=takeSecond)
    path = cons_list[con]["path"]
    for hub in sorter:
        if hub[0] in Origin["available_hubs"]:
            path.append(hub[0])
            sorter.remove(hub)
            break
    valid = True
    while valid:
        if path[-1] in Destination["available_hubs"]:
            valid = False
        else:
            path.append(sorter[0][0])
            sorter.remove(sorter[0])

with open("Consignments.txt", "w") as text_file:
    for con in cons_list:
        print(f"Consignment ID: {con}", file=text_file)
        print("Origin: {}".format(cons_list[con]["origin"]), file=text_file)
        print("Destination: {}".format(cons_list[con]["destination"]), file=text_file)
        print("Path: {}".format(cons_list[con]["path"]), file=text_file)
        print(f"", file=text_file)
    
#     cons_list[con]['distance'].update(con.path[:].sum())
# total_distance = cons[:][distance].sum()