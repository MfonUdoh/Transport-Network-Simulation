import random, math, pygame
from pygame.locals import *

def generateElements():
    
    # I used this dictionary of english-sounding words / syllables to generate the names of the depots
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
    
    # The mapWidth / Length sets the aspect ratio of the map; can make it thinner or wider using these variables
    mapWidth = 100
    mapLength = 100
    
    # I defined the hubs names and locations manuallly because I wanted to place them relative to where the population centres of the UK are
    hubs_list = {
        "carley" : {
            "location" : {"x" : int(mapWidth*.36), "y" : int(mapLength*.28)}, 
            "available_depots" : []
        },
        "gollingshire" : {
            "location" : {"x" : int(mapWidth*.29), "y" : int(mapLength*.30)}, 
            "available_depots" : []
        },
        "spack" : {
            "location" : {"x" : int(mapWidth*.38), "y" : int(mapLength*.53)}, 
            "available_depots" : []
        },
        "kingsbury" : {
            "location" : {"x" : int(mapWidth*.32), "y" : int(mapLength*.67)},
            "available_depots" : []
        },
        "diddley" : {
            "location" : {"x" : int(mapWidth*.32), "y" : int(mapLength*.80)},
            "available_depots" : []
        },
        "tuddle" : {
            "location" : {"x" : int(mapWidth*.53), "y" : int(mapLength*.80)},
            "available_depots" : []
        },
        "lount" : {
            "location" : {"x" : int(mapWidth*.25), "y" : int(mapLength*.82)},
            "available_depots" : []
        },
        "atherstone" : {
            "location" : {"x" : int(mapWidth*.28), "y" : int(mapLength*.90)},
            "available_depots" : []
        },
        "chillham" : {
            "location" : {"x" : int(mapWidth*.45), "y" : int(mapLength*.89)},
            "available_depots" : []
        },
        "kevlan" : {
            "location" : {"x" : int(mapWidth*.36), "y" : int(mapLength*.93)},
            "available_depots" : []
        },
        "stootlan" : {
            "location" : {"x" : int(mapWidth*.42), "y" : int(mapLength*.70)},
            "available_depots" : []
        }
    }

    # The depots are generated dynamically using the following code block
    depots_list = {}
    dist = 5 # This is the divisor that determines how far away the depots can be from the hubs they want to send consignments to (fraction of map's size)
    numbDeps = 10 # How many depots should be generated per Hub
    for hub in hubs_list:
        for dep in range(1+numbDeps):
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

    num_cons = 100*len(depots_list) # generates a number of consignments per each depot
    cons_list = {}
    for i in range(num_cons+1):
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

    for con in cons_list:
        sorter = []
        for hub in hubs_list:
            # loop calculates the combined distance of a given hub to both the origin and destination of a consignment and records it
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
        sorter.sort(key=takeSecond) # ranks the hubs by their combined distances from both origin and destination, this gives the preferred path as the straightest line  of hubs between the two points
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
        # cons_list[con]['distance'] = con["path"][:]
        # total_distance = cons[:][distance].sum()

    routes = {}
    for con in cons_list:
        path = cons_list[con]["path"]
        for dep in path:
            if path.index(dep) != (len(path)-1):
                rt = "{}:{}".format(dep, path[path.index(dep)+1])
                if (rt not in routes) and ("{}:{}".format(rt.split(":")[1], rt.split(":")[0]) not in routes):
                    routes.update({rt : 1})
                else:
                    if rt in routes:
                        routes[rt] += 1
                    else:
                        rt = "{}:{}".format(rt.split(":")[1], rt.split(":")[0])
                        routes[rt] += 1

    with open("Routes.txt", "w") as text_file:
        for rt in routes:
            print(
"""{}
{}
""".format(rt, routes[rt]), file=text_file)

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
    
    with open("Consignments.txt", "w") as text_file:
        for con in cons_list:
            print(
"""
Consignment ID: {}
Origin: {}
Destination: {}
Path: {}
""".format(con, cons_list[con]["origin"], cons_list[con]["destination"], cons_list[con]["path"]), file=text_file)

    return hubs_list, depots_list, cons_list, routes

hubs_list, depots_list, cons_list, routes = generateElements()

pygame.init()
f = pygame.font.SysFont(None,20)
screen_width = 600
screen_height = 600
scalerMultiple = ((screen_height + screen_width)/(2*100))
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Network Map")

hubSize = 20
depotSize = 5
landSize = 60
run = True

routesMax = ["", 0]
for rt in routes:
    if routes[rt] > routesMax[1]:
        routesMax = [rt, routes[rt]]

screen.fill((125, 175, 245)) # Light-Blue water colour for the background

ukMap = [
    [20, 10], [30, 10], 
    [20, 20], [30, 20], 
    [20, 30], [30, 30], 
    [20, 40], [30, 40], 
    [30, 50], [40, 50], 
    [20, 60], [30, 60], [40, 60], 
    [10, 70], [20, 70], [30, 70], [40, 70], [ 50, 70], 
    [20, 80], [30, 80], [40, 80], [50, 80], 
    [10, 90], [20, 90], [30, 90], [40, 90]
]
for block in ukMap:
    pygame.draw.rect(screen, (185, 235, 170), (int(scalerMultiple * (block[0])), int(scalerMultiple * (block[1])), landSize, landSize))

for con in cons_list:
    for i in range(len(depots_list[cons_list[con]["origin"]]["available_hubs"])):
        x1 = depots_list[cons_list[con]["origin"]]["location"]["x"]
        y1 = depots_list[cons_list[con]["origin"]]["location"]["y"]
        x2 = hubs_list[depots_list[cons_list[con]["origin"]]["available_hubs"][i]]["location"]["x"]
        y2 = hubs_list[depots_list[cons_list[con]["origin"]]["available_hubs"][i]]["location"]["y"]

        pygame.draw.line(screen, (230, 255, 100), (int(scalerMultiple * (1 + x1)), int(scalerMultiple * (1 + y1))), (int(scalerMultiple * ((hubSize/10) + x2)), int(scalerMultiple * ((hubSize/10) + y2))), 2)

for rt in routes:
    rt1 = rt.split(":")[0]
    rt2 = rt.split(":")[1]
    hub1x = hubs_list[rt1]["location"]["x"]
    hub1y = hubs_list[rt1]["location"]["y"]
    hub2x = hubs_list[rt2]["location"]["x"]
    hub2y = hubs_list[rt2]["location"]["y"]
    pygame.draw.line(screen, (230, (140-int(100*(routes[rt]/routesMax[1]))), 255), (int(scalerMultiple * ((hubSize/10) + hub1x)), int(scalerMultiple * ((hubSize/10) + hub1y))), (int(scalerMultiple * ((hubSize/10) + hub2x)), int(scalerMultiple * ((hubSize/10) + hub2y))), int(20*(routes[rt]/routesMax[1])))

for hub in hubs_list:
    hubx = hubs_list[hub]["location"]["x"]
    huby = hubs_list[hub]["location"]["y"]
    textsurface = f.render(str(hub), True, [0, 0, 0], [255, 255, 255])
    screen.blit(textsurface, (int(scalerMultiple * (1 + hubx)), int(scalerMultiple * (huby - 1))))
    pygame.draw.rect(screen, (50, 150, 252), (int(scalerMultiple * (1 + hubx)), int(scalerMultiple * (1 + huby)), hubSize, hubSize))

for depot in depots_list:
    depotx = depots_list[depot]["location"]["x"]
    depoty = depots_list[depot]["location"]["y"]
    pygame.draw.circle(screen, (0, 0, 255), (int(scalerMultiple * (1 + depotx)), int(scalerMultiple * (1 + depoty))), depotSize)

pygame.display.update()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.quit()