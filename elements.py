import random, math, config

def genHubs(mapWidth, mapLength, numHubs):
    # I defined the hubs names and locations manuallly because I wanted to place them relative to where the population centres of the UK are
    print("Generating Hubs...")
    hubs_list_total = {
        "carley" : {
            "location" : {"x" : int(mapWidth*.36), "y" : int(mapLength*.28)}, 
            "available_depots" : [],
            "available_hubs" : ["golligshire", "spack"]
        },
        "gollingshire" : {
            "location" : {"x" : int(mapWidth*.29), "y" : int(mapLength*.30)}, 
            "available_depots" : [],
            "available_hubs" : ["carley", "spack"]
        },
        "spack" : {
            "location" : {"x" : int(mapWidth*.38), "y" : int(mapLength*.53)}, 
            "available_depots" : [],
            "available_hubs" : ["golligshire", "carley", "kingsbury", "stootlan"]
        },
        "kingsbury" : {
            "location" : {"x" : int(mapWidth*.32), "y" : int(mapLength*.67)},
            "available_depots" : [],
            "available_hubs" : ["golligshire", "spack", "stootlan", "diddley", "lount"]
        },
        "diddley" : {
            "location" : {"x" : int(mapWidth*.32), "y" : int(mapLength*.80)},
            "available_depots" : [],
            "available_hubs" : ["kingsbury", "stootlan", "lount", "atherstone", "kevlan", "chillham", "tuddle"]
        },
        "tuddle" : {
            "location" : {"x" : int(mapWidth*.53), "y" : int(mapLength*.80)},
            "available_depots" : [],
            "available_hubs" : ["stootlan", "chillham", "diddley"]
        },
        "lount" : {
            "location" : {"x" : int(mapWidth*.25), "y" : int(mapLength*.82)},
            "available_depots" : ["kingsbury", "diddley", "atherstone"],
            "available_hubs" : ["kingsbury", "diddley", "atherstone"]
        },
        "atherstone" : {
            "location" : {"x" : int(mapWidth*.28), "y" : int(mapLength*.90)},
            "available_depots" : [],
            "available_hubs" : ["kevlan", "diddley", "lount"]
        },
        "chillham" : {
            "location" : {"x" : int(mapWidth*.45), "y" : int(mapLength*.89)},
            "available_depots" : [],
            "available_hubs" : ["kevlan", "diddley", "tuddle"]
        },
        "kevlan" : {
            "location" : {"x" : int(mapWidth*.36), "y" : int(mapLength*.93)},
            "available_depots" : [],
            "available_hubs" : ["chillham", "diddley", "atherstone"]
        },
        "stootlan" : {
            "location" : {"x" : int(mapWidth*.42), "y" : int(mapLength*.70)},
            "available_depots" : [],
            "available_hubs" : ["kingsbury", "spack", "diddley", "chillham", "tuddle"]
        }
    }
    hubs_list = {}
    count = 0
    for hub in hubs_list_total:
        if count < numHubs:
            hubs_list.update({hub : hubs_list_total[hub]})
            count += 1

    return hubs_list


def genDepots(mapWidth, mapLength, numDeps, hubs_list):
    print("Generating Depots...")
    # The depots are generated dynamically using the following code block
    names = config.names
    depots_list = {}
    dist = 10 # This is the divisor that determines how far away the depots can be from the hubs they want to send consignments to (fraction of map's size)
    for hub in hubs_list:
        # if hub == "kingsbury" or hub == "tuddle":
        for dep in range(numDeps):
            dx, dy = (mapWidth/dist), (mapLength/dist) # dx and dy are by how much the hub's coordinates are changed by to determine the new depot's x and y coordinates resepectively
            while ((dx**2 + dy**2) > (mapWidth/dist)**2) or (hubs_list[hub]['location']['x'] + dx not in range(mapWidth + 1)) or (hubs_list[hub]['location']['y'] + dy not in range(mapLength + 1)):
                # loop keeps trying different dx and dy values until the new depot location is both inside the map and within delivery range of the hub
                (dx, dy) = (random.randrange(-(mapWidth/dist),(mapWidth/dist)), random.randrange(-(mapLength/dist),(mapLength/dist)))
            depotname = ""
            while depotname not in depots_list:
                # loop makes a unique name using the words in the names dictionary
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
            depots_list.update({
                depotname : {
                    "location" : {
                        "x" : hubs_list[hub]['location']['x'] + dx, 
                        "y" : hubs_list[hub]['location']['y'] + dy}, 
                    "available_hubs" : []}})

    for depot in depots_list:
        for hub in hubs_list:
            # loop goes through every depot and attaches its available hubs, concurrently adding available depots to each hub
            if (depots_list[depot]["location"]["x"] - hubs_list[hub]['location']['x'])**2 + (depots_list[depot]["location"]["y"] - hubs_list[hub]['location']['y'])**2 <= (mapWidth/dist)**2:
                depots_list[depot]["available_hubs"].append(hub)
                hubs_list[hub]["available_depots"].append(depot)

    return depots_list, hubs_list

def genConsignments(numCons, depots_list):
    print("Generating Consignments...")
    num_cons = numCons*len(depots_list) # generates a number of consignments per each depot
    cons_list = {}
    for i in range(num_cons):
        while True:
            # loop picks a random start and end point for the consignment
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
    return cons_list

def genPath(hubs_list, depots_list, cons_list):
    for con in cons_list:
        sorter = []
        sorterOrigin = []
        sorterDestination = []
        for hub in hubs_list:
            # loop calculates the combined distance of a given hub to both the origin and destination of a consignment and records it
            startDepot = cons_list[con]["origin"]
            Origin = depots_list[startDepot]
            targetDepot = cons_list[con]["destination"]
            Destination = depots_list[targetDepot]
            Hub = hubs_list[hub]
            distanceToOrigin = int(math.sqrt((Hub["location"]["x"] - Origin["location"]["x"])**2 + (Hub["location"]["y"] - Origin["location"]["y"])**2))
            distanceToDestination = int(math.sqrt((Hub["location"]["x"] - Destination["location"]["x"])**2 + (Hub["location"]["y"] - Destination["location"]["y"])**2))
            sorter.append([hub, distanceToOrigin + distanceToDestination])
            sorterOrigin.append([hub, distanceToOrigin])
            sorterDestination.append([hub, distanceToDestination])
        def takeSecond(elem):
            return elem[1]
        sorter.sort(key=takeSecond) # ranks the hubs by their combined distances from both origin and destination, this gives the preferred path as the straightest line  of hubs between the two points
        sorterOrigin.sort(key=takeSecond)
        sorterOriginDict = {}
        for i in sorterOrigin:
            sorterOriginDict.update({i[0] : i[1]})
        sorterDestination.sort(key=takeSecond)
        sorterDestinationDict = {}
        for i in sorterDestination:
            sorterDestinationDict.update({i[0] : i[1]})
        path = cons_list[con]["path"]
        for hub in sorter:
            if hub[0] in Origin["available_hubs"]:
                path.append(hub[0])
                distFrmOrg = sorterOriginDict[hub[0]]
                distFrmDst = sorterDestinationDict[hub[0]]
                cons_list[con]['distance'] += distFrmOrg
                sorterOriginDict.pop(hub[0])
                sorterDestinationDict.pop(hub[0])
                sorter.remove(hub)
                break
        valid = True
        while valid:
            if path[-1] in Destination["available_hubs"]:
                cons_list[con]['distance'] += distFrmDst
                valid = False
            elif (sorterOriginDict[sorter[0][0]] >= distFrmOrg) and (sorterDestinationDict[sorter[0][0]] <= distFrmDst):
                path.append(sorter[0][0])
                distFrmOrg = sorterOriginDict[sorter[0][0]]
                distFrmDst = sorterDestinationDict[sorter[0][0]]
                sorterOriginDict.pop(sorter[0][0])
                sorterDestinationDict.pop(sorter[0][0])
                sorter.remove(sorter[0])
            elif (sorterOriginDict[sorter[0][0]] >= distFrmOrg):
                path.append(sorter[0][0])
                distFrmOrg = sorterOriginDict[sorter[0][0]]
                distFrmDst = sorterDestinationDict[sorter[0][0]]
                sorterOriginDict.pop(sorter[0][0])
                sorterDestinationDict.pop(sorter[0][0])
                sorter.remove(sorter[0])
            else:
                path.append(sorter[0][0])
                distFrmOrg = sorterOriginDict[sorter[0][0]]
                distFrmDst = sorterDestinationDict[sorter[0][0]]
                sorterOriginDict.pop(sorter[0][0])
                sorterDestinationDict.pop(sorter[0][0])
                sorter.remove(sorter[0])
    return cons_list

def genRoutes(hubs_list, depots_list, cons_list):
    routes = {}
    for con in cons_list:
        path = cons_list[con]["path"]
        cons_list[con]["routes"] = []
        for dep in path:
            if path.index(dep) != (len(path)-1):
                rt = "{}:{}".format(dep, path[path.index(dep)+1])
                if (rt not in routes) and ("{}:{}".format(rt.split(":")[1], rt.split(":")[0]) not in routes):
                    routes.update({rt : [1, 0]})
                    cons_list[con]["routes"].append(rt)
                else:
                    if rt in routes:
                        routes[rt][0] += 1
                        cons_list[con]["routes"].append(rt)
                    else:
                        rt = "{}:{}".format(rt.split(":")[1], rt.split(":")[0])
                        routes[rt][0] += 1
                        cons_list[con]["routes"].append(rt)
    
    for route in routes:
        hub1 = hubs_list[route.split(":")[0]]["location"]
        hub2 = hubs_list[route.split(":")[1]]["location"]
        routes[route][1] = int(math.sqrt((hub2["x"] - hub1["x"])**2 + (hub2["y"]-hub1["y"])**2))
    for con in cons_list:
        for route in cons_list[con]["routes"]:
            cons_list[con]["distance"] += routes[route][1]
    totalDistance = 0
    longestDistance = ["", 0]
    for con in cons_list:
        dis = cons_list[con]["distance"]
        totalDistance += dis
        if dis > longestDistance[1]:
            longestDistance = [cons_list[con]["path"], dis]
    averageDistance = totalDistance / len(cons_list)
    mostUsedRoute = ["", 0]
    mostUsedHub = ["", 0]
    for rt in routes:
        if routes[rt][0] > mostUsedRoute[1]:
            mostUsedRoute = [rt, routes[rt][0]]

    for rt in routes:
        for i in rt.split(":"):
            hubCounter = 0
            for r in routes:
                if i == r.split(":")[0] or i == r.split(":")[1]:
                    hubCounter += routes[r][0]
            if hubCounter > mostUsedHub[1]:
                mostUsedHub = [i, hubCounter]
    summary = [totalDistance, averageDistance, longestDistance, mostUsedRoute, mostUsedHub]

    return routes, summary

def saveData(hubs_list, depots_list, cons_list, routes, summary):
    print("Saving Hubs .....")
    with open("Hubs.txt", "w") as text_file:
        for hub in hubs_list:
            print(
"""Hub Name: {}
Hub Location: {}
Hub Available Depots: {}
""".format(hub, hubs_list[hub]["location"], hubs_list[hub]["available_depots"]), file=text_file)

    print("Saving Depots .....")
    with open("Depots.txt", "w") as text_file:
        for depot in depots_list:
            print(
"""Depot Name: {}
Depot Location: {}
Depot Available Hubs: {}
""".format(depot, depots_list[depot]["location"], depots_list[depot]["available_hubs"]), file=text_file)

    print("Saving Consignments.....")
    with open("Consignments.txt", "w") as text_file:
        for con in cons_list:
            print(
"""Consignment ID: {}
Origin: {}
Destination: {}
Path: {}
Distance: {}
""".format(con, cons_list[con]["origin"], cons_list[con]["destination"], cons_list[con]["path"], cons_list[con]["distance"]), file=text_file)

    print("Saving Routes .....")
    with open("Routes.txt", "w") as text_file:
        for rt in routes:
            print(
"""{}
Distance: {}
Used {} times
""".format(rt, routes[rt][1], routes[rt][0]), file=text_file)

    with open("Summary.txt", "w") as text_file:
        print(
"""Total Consignments: {}
Total Distance: {}
Average Distance: {}
Longest Distance: {}
Most Used Route: {}
Most Used Hub: {}
Least Used Route: 
Least Used Hub: 
""".format(len(cons_list), summary[0], summary[1], summary[2], summary[3], summary[4]), file=text_file)

