import random

def values():
    """Generate random input values for number of Hubs, Depots, Consignments."""
    h = str(random.randint(0, 20))
    d = str(random.randint(1, 20))
    c = str(random.randint(1, 100))
    return h, d, c

### Use this code block to test the inputs

# testCount = 0
# while testCount < 500:
#     while True:
#         # h = str(4)#input("Enter how many hubs are required (2-11): ")
#         # d = str(5)#input("Enter how many depots are required for each hub: ")
#         # c = str(500)#input("Enter how many consignments are required for each depot: ")
#         h, d, c = test.values()
#         if d.isnumeric() and c.isnumeric() and h.isnumeric() and int(h) <= 11 and int(h) >= 2:
#             numHubs = int(h)
#             numDeps = int(d)
#             numCons = int(c)
#             break
#         else:
#             # print("ERROR: Please enter valid numbers.")
#             print("test {} passed".format(testCount))
#             testCount += 1

#     depots_list, hubs_list = elements.genDepots(mapWidth, mapLength, numDeps, elements.genHubs(mapWidth, mapLength, numHubs))
#     cons_list = elements.genPath(hubs_list, depots_list, elements.genConsignments(numCons, depots_list))
#     routes, summary = elements.genRoutes(hubs_list, depots_list, cons_list)
#     # elements.saveData(hubs_list, depots_list, cons_list, routes, summary)
#     print("test {} passed".format(testCount))
#     testCount += 1