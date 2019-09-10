import random, math, pygame, elements, config
from pygame.locals import *

# The mapWidth / Length sets the aspect ratio of the map; can make it thinner or wider using these variables
mapWidth = 100
mapLength = 100

print("Welcome to the Road Network Simulation")
while True:
    h = input("Enter how many hubs are required (2-11): ")
    d = input("Enter how many depots are required for each hub: ")
    c = input("Enter how many consignments are required for each depot: ")
    if d.isnumeric() and c.isnumeric() and h.isnumeric() and int(h) <= 11 and int(h) >= 2:
        numHubs = int(h)
        numDeps = int(d)
        numCons = int(c)
        break
    else:
        print("ERROR: Please enter valid numbers.")

depots_list, hubs_list = elements.genDepots(mapWidth, mapLength, numDeps, elements.genHubs(mapWidth, mapLength, numHubs))
cons_list = elements.genPath(hubs_list, depots_list, elements.genConsignments(numCons, depots_list))
routes, summary = elements.genRoutes(hubs_list, depots_list, cons_list)
elements.saveData(hubs_list, depots_list, cons_list, routes, summary)

print("Displaying....")
pygame.init()
f = pygame.font.SysFont(None,20)
screen_width = 800
screen_height = 800
scalerMultiple = ((screen_height + screen_width)/(2*100))
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Network Map")

hubSize = 20
depotSize = 5
landSize = 90
run = True

routesMax = ["", 0]
for rt in routes:
    if routes[rt][0] > routesMax[1]:
        routesMax = [rt, routes[rt][0]]

screen.fill((125, 175, 245)) # Light-Blue water colour for the background
ukMap = config.ukMap

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
    pygame.draw.line(screen, (230, (140-int(100*(routes[rt][0]/routesMax[1]))), 255), (int(scalerMultiple * ((hubSize/10) + hub1x)), int(scalerMultiple * ((hubSize/10) + hub1y))), (int(scalerMultiple * ((hubSize/10) + hub2x)), int(scalerMultiple * ((hubSize/10) + hub2y))), int(20*(routes[rt][0]/routesMax[1])))

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
print("DONE.")
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.quit()
