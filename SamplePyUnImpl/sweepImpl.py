import json
import util
import operator
from audioop import reverse
import new
from ortools.constraint_solver._pywrapcp import new_BaseLns
from itertools import repeat
from math import degrees, atan2


with open('data4.json') as inputFile:
    data = json.load(inputFile)

# print "VehicleCap: ",data["vehicleCapacity"]
# print "Depot: ",data["depot"]["x"],":",data["depot"]["y"]
# print "Sample Node: ",data["nodes"][0]["x"],":",data["nodes"][0]["y"],"-->",data["nodes"][0]["demand"]

noOfCustomers = len(data["nodes"])
customerPosDemand = dict()
vehicleCap = data["vehicleCapacity"][0]["1"]
# print vehicleCap
for i in range(noOfCustomers):
    customerPosDemand[data["nodes"][i]["x"],data["nodes"][i]["y"]] = data["nodes"][i]["demand"]
# print customerPosDemand

depot = (data["depot"]["x"],data["depot"]["y"])
customerPositions =  customerPosDemand.keys()
vehicleCap = data["vehicleCapacity"][0]["1"]

customerPosDemand = dict()
for i in range(noOfCustomers):
    customerPosDemand[data["nodes"][i]["x"],data["nodes"][i]["y"]] = data["nodes"][i]["demand"]

def calculateDepotAngle(x,y,depot_x,depot_y):
    angle = degrees(atan2(y - depot_y, x - depot_x))
    bearing = (90 - angle) % 360
    return bearing

#getting all angles
anglesWithDepot = dict()
depotX,depotY = depot 
for x,y in customerPositions:
    anglesWithDepot[(x,y)] = calculateDepotAngle(x, y, depotX, depotY)
# print anglesWithDepot
anglesWithDepot = sorted(anglesWithDepot.items(),key=operator.itemgetter(1),reverse=False)
# print anglesWithDepot


customerServed = dict()
custAngleWiseList = list()
for cust, angle in anglesWithDepot:
    custAngleWiseList.append(cust)
    customerServed[cust] = False

def allCustomersConsidered(customerServed):
    for val in customerServed.values():
        if val == False:
            return False
    return True


clusters = list()
tempCluster = list()
cap = 0
print anglesWithDepot   
print "-------------"
while (len(custAngleWiseList)):
    currCust = custAngleWiseList.pop(0)
    if cap + customerPosDemand[currCust] <= vehicleCap:
        tempCluster.append(currCust)
        cap += customerPosDemand[currCust]
    else:
        clusters.append(tempCluster)
        tempCluster = list()
        cap = 0
        tempCluster.append(currCust)
        cap += customerPosDemand[currCust]
        
clusters.append(tempCluster)
for c in clusters:
    print c