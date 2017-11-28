import json
import operator
from math import degrees, atan2
import or_tsp

class Position:

    def __init__(self,x,y):
        self.x = x
        self.y = y      

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ") "

    def x_coor(self):
        return self.x

    def y_coor(self):
        return self.y

class Customer:

    pos = Position(-1,-1)
    demand = 0

    def __init__(self,name):
        self.name = name

    def setPosition(self,x,y):
        self.pos = Position(x, y)

    def setDemand(self,d):
        self.demand = d

    def setAngleWithDepot(self, a):
        self.angleWithDepot = a

    def __str__(self):
        return str(self.name) #+ " -> (" + str(self.pos.x) + ", " + \
                #str(self.pos.y) + ") -> " + str(self.demand)

def print_tuple(t):
    print "[", 
    for i in t:
        print i,        
    print "]"

def copy(li):
    return [i for i in li]

def calculateDepotAngle(x,y,depot_x,depot_y):
    angle = degrees(atan2(y - depot_y, x - depot_x))
    bearing = (90 - angle) % 360
    return bearing


with open('data4.json') as inputFile:
    data = json.load(inputFile)

noOfCustomers = len(data["nodes"])
vehicleCap = data["vehicleCapacity"][0]["1"]

DEPOT = Customer(0)
DEPOT.setPosition(data["depot"]["x"],data["depot"]["y"])
DEPOT.setDemand(0)
DEPOT.setAngleWithDepot(0)

Customers = []
for i in range(0,noOfCustomers):
    c = Customer(i+1)
    c.setPosition(data["nodes"][i]["x"],data["nodes"][i]["y"])
    c.setDemand(data["nodes"][i]["demand"])
    angle = calculateDepotAngle(c.pos.x, c.pos.y, DEPOT.pos.x, DEPOT.pos.y)
    c.setAngleWithDepot(angle)
    Customers.append(c)

Customers.sort(key=lambda x: x.angleWithDepot, reverse=False)

clusters = list()
tempCluster = list()
cap = 0
temp_Customers = copy(Customers)
while len(temp_Customers):
    currCust = temp_Customers.pop(0)
    if cap + currCust.demand <= vehicleCap:
        tempCluster.append(currCust)
        cap += currCust.demand
    else:
        clusters.append(tempCluster)
        tempCluster = list()
        cap = 0
        tempCluster.append(currCust)
        cap += currCust.demand
        
clusters.append(tempCluster)
for c in clusters:
    print_tuple(c)