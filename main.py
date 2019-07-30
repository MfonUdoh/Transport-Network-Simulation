import random, math

names = {
        "prefix" : [
            "abing", "aber", "bark", "berry", "chelms", "car", "wood","strem", "ling", "spack",
            "trem", "mug", "deck", "tillin", "nod", "mabb", "golling", "miad", "ebbing", "nike",
            "dell"
    ],
        "suffix" : [
            "shire", "ton", "don", "ford", "cester", "ley"
        ]
}

hubs_list = {
    "carley" : {
        "location" : {"x" : 42, "y" : 73}, 
        "available_depots" : []
    },
    "gollingshire" : {
        "location" : {"x" : 95, "y" : 21}, 
        "available_depots" : []
    },
    "spack" : {
        "location" : {"x" : 10, "y" : 11}, 
        "available_depots" : []
    },
    "kingsbury" : {
        "location" : {"x" : 15, "y" : 14},
        "available_depots" : []
    },
    "diddley" : {
        "location" : {"x" : 24, "y" : 5},
        "available_depots" : []
    },
    "tuddle" : {
        "location" : {"x" : 7, "y" : 80},
        "available_depots" : []
    },
    "lount" : {
        "location" : {"x" : 55, "y" : 22},
        "available_depots" : []
    }
}
depots_list = {}
for hub in hubs_list:
    for dep in range(6):
        dx, dy = 10, 10
        while (dx**2 + dy**2) > 10**2:
            (dx, dy) = (random.randrange(-10,10), random.randrange(-10,10))
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
        if (depots_list[depot]["location"]["x"] - hubs_list[hub]['location']['x'])**2 + (depots_list[depot]["location"]["y"] - hubs_list[hub]['location']['y'])**2 < 10**2:
            depots_list[depot]["available_hubs"].append(hub)
            hubs_list[hub]["available_depots"].append(depot)

num_cons = 10000
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

for con in cons_list:
    originPreference = []
    destinationPreference = []
    hub_dist = {}
    for hub in hubs_list:
        hub_dist.update({ hub : {math.sqrt(abs(hubs_list[hub]['location']['x']-cons_list[con]['origin']['x'])**2+abs(hubs_list[hub]['location']['y']-cons_list[con]['origin']['y'])**2)}})
    while len(hub_dist) != 0:
        hub_rank.append(hub_dist[:].min())
        hub_dist[:].min().pop()
    for hub in hub_rank:
        con.path.append(hub)
        if con.destination in hubs_list[hub][available_hubs]:
            break
    con[distance] = con.path[:].sum()
total_distance = cons[:][distance].sum()