import math
def manhattanDistance( xy1, xy2 ):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )

def euclideanDistance( xy1, xy2 ):
    "Returns the Manhattan distance between points xy1 and xy2"
    return  math.sqrt(( xy2[0] - xy1[0] )**2 + ( xy2[1] - xy1[1] )**2)

def calculateRouteCost(r):
    total = 0
    for i in range(len(r) - 1):
        total+= euclideanDistance(r[i] , r[i+1])
    return total

def addDepotAtEnds(depot,route):
    route.insert(0,depot)
    route.append(depot)
    