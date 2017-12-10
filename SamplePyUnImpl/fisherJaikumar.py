import json
import util
import operator
from audioop import reverse
import new
from ortools.constraint_solver._pywrapcp import new_BaseLns
from itertools import repeat

with open('data.json') as inputFile:
    data = json.load(inputFile)

print "VehicleCap: ",data["vehicleCapacity"]
print "Depot: ",data["depot"]["x"],":",data["depot"]["y"]
print "Sample Node: ",data["nodes"][0]["x"],":",data["nodes"][0]["y"],"-->",data["nodes"][0]["demand"]

noOfCustomers = len(data["nodes"])
customerPosDemand = dict()
vehicleCap = data["vehicleCapacity"][0]["1"]
print vehicleCap
for i in range(noOfCustomers):
    customerPosDemand[data["nodes"][i]["x"],data["nodes"][i]["y"]] = data["nodes"][i]["demand"]
print customerPosDemand
