import random, math, config

def genHubs(mapWidth, mapLength, numHubs):
    # I defined the hubs names and locations manuallly because I wanted to place them relative to where the population centres of the UK are
    print("Generating Hubs...")
    hubs_list_total = {
        "carley" : {
            "location" : {"x" : int(mapWidth*.36), "y" : int(mapLength*.28)}, 
            "available_depots" : [],
            "available_hubs" : ["gollingshire", "spack"]
        },
        "gollingshire" : {
            "location" : {"x" : int(mapWidth*.29), "y" : int(mapLength*.30)}, 
            "available_depots" : [],
            "available_hubs" : ["carley", "spack"]
        },
        "spack" : {
            "location" : {"x" : int(mapWidth*.38), "y" : int(mapLength*.53)}, 
            "available_depots" : [],
            "available_hubs" : ["gollingshire", "carley", "kingsbury", "stootlan"]
        },
        "kingsbury" : {
            "location" : {"x" : int(mapWidth*.32), "y" : int(mapLength*.67)},
            "available_depots" : [],
            "available_hubs" : ["gollingshire", "spack", "stootlan", "diddley", "lount"]
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
            "available_depots" : [],
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
            "location" : {"x" : int(mapWidth*.36), "y" : int(mapLength*.94)},
            "available_depots" : [],
            "available_hubs" : ["chillham", "diddley", "atherstone"]
        },
        "stootlan" : {
            "location" : {"x" : int(mapWidth*.42), "y" : int(mapLength*.70)},
            "available_depots" : [],
            "available_hubs" : ["kingsbury", "spack", "diddley", "chillham", "tuddle"]
        }
    }

    def common(iter1, iter2):
        """Common returns true if there are any common elements between two lists"""
        common = False
        for i in iter1:
            for j in iter2:
                if i == j:
                    common = True
                    return common
        return common
        
    
    hubs_list = {}
    count = 0
    allowed = []
    while count < numHubs:
        # This loop will make sure that the specified number of hubs have been selected before continuing
        selection = random.choice(list(hubs_list_total.keys()))
        if hubs_list == {}:
            hubs_list.update({selection : hubs_list_total[selection]}) # Adds the first hub to the hubs list
            allowed.extend(hubs_list_total[selection]["available_hubs"]) # This makes sure that only hubs connected to the first hub are chosen otherwise the network will not be connected
            count += 1
        elif selection not in hubs_list and selection in allowed and common(hubs_list_total[selection]["available_hubs"], hubs_list):
            # Chooses a hub provided; hub not selected already, hub can be reached by others, hub can reach others
            hubs_list.update({selection : hubs_list_total[selection]})
            allowed.extend(hubs_list_total[selection]["available_hubs"])
            count += 1

    for hub in hubs_list:
        # This nested for loop removes any of the hubs that do not exist in the network from the 'available_hubs'
        allowed = []
        for ahub in hubs_list[hub]["available_hubs"]:
            if ahub in hubs_list:
                allowed.append(ahub)
        hubs_list[hub]["available_hubs"] = allowed 

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
    
    def dijkstra(graph, sourceVertex, targetVertex):
        """The Dijkstra SPF algorithm is used to find the shortest path through the network from the source to target node. https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm"""
        def pythag(x1, x2, y1, y2):
            """Uses the Pythagorean theorem to find the distance between two coordinates."""
            return math.sqrt((x1-x2)**2 + (y1-y2)**2)
        
        Q = []
        distance = {}
        previous = {}
        x2 = graph[sourceVertex]["location"]["x"]
        y2 = graph[sourceVertex]["location"]["y"]
        
        for vertex in graph:
            # Sets the initial condition for all of the vertices
            distance[vertex] = 1000000 # Infinity for this application
            previous[vertex] = ""
            Q.append(vertex)
        distance[sourceVertex] = 0
        
        while Q != []:
            minVal = ""
            for v in Q:
                if minVal == "":
                    minVal = [v, distance[v]]
                elif distance[v] < minVal[1]:
                    minVal = [v,  distance[v]]
            vertex = minVal[0] # Select the closest node to the source, this will of course be the source for the first path.
            Q.pop(Q.index(vertex))

            if vertex == targetVertex:
                break
            for link in graph[vertex]["available_hubs"]:
                # Suggest an alternate path for the neighbour vertex; selected vertex as its previous vertex 
                alternate = distance[vertex] + pythag(graph[vertex]["location"]["x"], graph[link]["location"]["x"], graph[vertex]["location"]["y"], graph[link]["location"]["y"])
                if alternate < distance[link]:
                    # If this alternative path through the selected vertex is shorter than its current path then it will overwrite it.
                    # This will automatically be true for every neighbour that is still at the initial infinite distance condition.
                    distance[link] = alternate
                    previous[link] = vertex

        path = []
        pathdistance = distance[targetVertex]

        u = targetVertex
        path.append(u)
        while u != sourceVertex:
            # Loop through the previous dictionary to construct the complete path between the source and the target.
            path.append(previous[u])
            u = previous[u]
        path.reverse()

        return pathdistance, path

    for con in cons_list:
        for ohub in depots_list[cons_list[con]["origin"]]["available_hubs"]:
            for dhub in depots_list[cons_list[con]["destination"]]["available_hubs"]:
                # Uses the dijkstra function to find the best option out of all the available origin and destination hubs for the consignment
                if cons_list[con]["path"] == []:
                    cons_list[con]["distance"], cons_list[con]["path"] = dijkstra(hubs_list, ohub, dhub)
                elif cons_list[con]["distance"] > dijkstra(hubs_list, ohub, dhub)[0]:
                    cons_list[con]["distance"], cons_list[con]["path"] = dijkstra(hubs_list, ohub, dhub)

    return cons_list

def genRoutes(hubs_list, depots_list, cons_list):
    routes = {}
    for con in cons_list:
        path = cons_list[con]["path"]
        cons_list[con]["routes"] = []
        for dep in path:
            if path.index(dep) != (len(path)-1):
                # Extract each leg of the path and count how many times its used
                rt = "{}:{}".format(dep, path[path.index(dep)+1])
                if (rt not in routes) and ("{}:{}".format(rt.split(":")[1], rt.split(":")[0]) not in routes):
                    routes.update({rt : [1, 0]})
                    cons_list[con]["routes"].append(rt)
                else:
                    if rt in routes:
                        routes[rt][0] += 1
                        cons_list[con]["routes"].append(rt)
                    else:
                        # Make sure to count the reverse journey also
                        rt = "{}:{}".format(rt.split(":")[1], rt.split(":")[0])
                        routes[rt][0] += 1
                        cons_list[con]["routes"].append(rt)
    
    for route in routes:
        # Calculate length of each route using the distance between the two hubs
        hub1 = hubs_list[route.split(":")[0]]["location"]
        hub2 = hubs_list[route.split(":")[1]]["location"]
        routes[route][1] = int(math.sqrt((hub2["x"] - hub1["x"])**2 + (hub2["y"]-hub1["y"])**2))

    totalDistance = 0
    longestDistance = ["", 0]
    mostUsedRoute = ["", 0]
    mostUsedHub = ["", 0]
    leastUsedRoute = ["", 1000000]
    leastUsedHub = ["", 1000000]

    for con in cons_list:
        dis = cons_list[con]["distance"]
        totalDistance += dis
        if dis > longestDistance[1]:
            longestDistance = [cons_list[con]["path"], dis]
    averageDistance = totalDistance / len(cons_list)
    
    for rt in routes:
        if routes[rt][0] > mostUsedRoute[1]:
            mostUsedRoute = [rt, routes[rt][0]]
        if routes[rt][0] < leastUsedRoute[1]:
            leastUsedRoute = [rt, routes[rt][0]]

    for rt in routes:
        for i in rt.split(":"):
            hubCounter = 0
            for r in routes:
                if i == r.split(":")[0] or i == r.split(":")[1]:
                    hubCounter += routes[r][0]
            if hubCounter > mostUsedHub[1]:
                mostUsedHub = [i, hubCounter]
            if hubCounter < leastUsedHub[1]:
                leastUsedHub = [i, hubCounter]
    summary = [totalDistance, averageDistance, longestDistance, mostUsedRoute, mostUsedHub, leastUsedRoute, leastUsedHub]

    return routes, summary

def saveData(hubs_list, depots_list, cons_list, routes, summary):
    print("Saving Hubs .....")
    with open("Hubs.txt", "w") as text_file:
        for hub in hubs_list:
            print(
"""Hub Name: {}
Hub Location: {}
Hub Available Depots: {}
Hub Available Hubs: {}
""".format(hub, hubs_list[hub]["location"], hubs_list[hub]["available_depots"], hubs_list[hub]["available_hubs"]), file=text_file)

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
Least Used Route: {}
Least Used Hub: {}
""".format(len(cons_list), summary[0], summary[1], summary[2], summary[3], summary[4], summary[5], summary[6]), file=text_file)

