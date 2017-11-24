import json
import util
import operator
from audioop import reverse

with open('data1.json') as inputFile:
    data = json.load(inputFile)

# print "VehicleCap: ",data["vehicleCapacity"]
# print "Depot: ",data["depot"]["x"],":",data["depot"]["y"]
# print "Sample Node: ",data["nodes"][0]["x"],":",data["nodes"][0]["y"],"-->",data["nodes"][0]["demand"]
#def buildSavings():
    #after this customers will have x:val , y:val,demand:val

noOfCustomers = len(data["nodes"])
customerPosDemand = dict()


for i in range(noOfCustomers):
    customerPosDemand[data["nodes"][i]["x"],data["nodes"][i]["y"]] = data["nodes"][i]["demand"]
#print customerPosDemand

#compute Savings for depot and i,j where i <> j
def computeSaving(depot, i,j):
    iDepot = util.manhattanDistance(i, depot)
    jDepot = util.manhattanDistance(depot, j)
    ijDist = util.manhattanDistance(i, j)
    
    return (iDepot + jDepot - ijDist)
    
#def distDepot


#calculating savingss for all pairs
savings = dict()
customerPositions =  customerPosDemand.keys()
pointsLen = len(customerPositions)
depot = (data["depot"]["x"],data["depot"]["y"])
#print depot

for i in range(pointsLen):
    for j in range(pointsLen):
        if j > i :
            savings[(customerPositions[i], customerPositions[j])] = computeSaving(depot,customerPositions[i], customerPositions[j])
#print savings

#creating routes ((depot - i - depot),capacity served) for all customers[i]
routes = list()
for i in range(pointsLen):
    routes.append(((depot,customerPositions[i],depot),customerPosDemand[customerPositions[i]]))
#print routes

#ordering savings in descending order and getting the nodes
savings = sorted(savings.items(),key=operator.itemgetter(1),reverse=True)
l = len(savings)
cust_pairs = list()
for i in range(l):
    cust_pairs.append(savings[i][0])
#print cust_pairs


def depotNode1(node):
    for r in routes:
        if r[0][0] == depot and r[0][1] == node:
            return r
    return None  

def node0Depot (node):
    for r in routes:
        if r[0][len(r) - 1] == node and r[0][len(r)] == depot:
            return r
    return None  
    


def calculateRouteCost(r):
    total = 0
    for i in range(len(r[0]) - 1):
        total+= util.euclideanDistance(r[0][i] , r[0][i+1])
    #print total
    return total
#creating routes
for node in cust_pairs:
    r1 = depotNode1(node[1]) #j
    r2 = node0Depot(node[0]) #i 
    if (not(r1 == None)  and  not(r2 == None)):
#         print r1
#         print r2
        newRoute = list()
        #get path from depot to i
        newRoute.append(r2[0][0])
        newRoute.append(r2[0][1])
        
        #get path from j to depot
        addAll = False
        for i in range(0,len(r1[0])):
            if r1[0][i] == node[1] or addAll:
                newRoute.append(r1[0][i])
                addAll = True
        
#         print newRoute
        
        #add the newRoute to original List and remove the current
        routes.remove(r1)
        routes.remove(r2)

        #new current carrying capacity will be the total of both routes
        newCapacity = r1[1] + r2[1]
        routes.append((newRoute,newCapacity))

        #print r2[0][len(r2) - 1] , r1[0][1]

totalDist = 0
#print len(routes)
for r in routes:
    totalDist += calculateRouteCost(r)
#print totalDist







