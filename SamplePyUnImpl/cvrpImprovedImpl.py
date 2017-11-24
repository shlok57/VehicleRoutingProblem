import json
import util
import operator
from audioop import reverse
import new
from ortools.constraint_solver._pywrapcp import new_BaseLns
from itertools import repeat

with open('data2.json') as inputFile:
    data = json.load(inputFile)

# print "VehicleCap: ",data["vehicleCapacity"]
# print "Depot: ",data["depot"]["x"],":",data["depot"]["y"]
# print "Sample Node: ",data["nodes"][0]["x"],":",data["nodes"][0]["y"],"-->",data["nodes"][0]["demand"]
#def buildSavings():
    #after this customers will have x:val , y:val,demand:val

noOfCustomers = len(data["nodes"])
customerPosDemand = dict()
vehicleCap = data["vehicleCapacity"][0]["1"]
# print vehicleCap
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
#----------------------------------------------------------------#



def allCustomersConsidered(customerServed):
    for val in customerServed.values():
        if val == False:
            return False
    return True
        


# refer link - http://ieeexplore.ieee.org/document/7784340/?reload=true
#Step 1
distanceDict = dict()
for i in range(pointsLen):
    for j in range(i+1,pointsLen):
        distanceDict[(customerPositions[i], customerPositions[j])] = util.euclideanDistance(customerPositions[i], customerPositions[j])

#Step 2
for i in range(pointsLen):
    for j in range(i+1,pointsLen):
        savings[(customerPositions[i], customerPositions[j])] = computeSaving(depot,customerPositions[i], customerPositions[j])
savings = sorted(savings.items(),key=operator.itemgetter(1),reverse=True)
l = len(savings)
cust_pairs = list()
for i in range(l):
    cust_pairs.append(savings[i][0])

#initially none of the customers have been isServed
customerServed = dict()
for c in customerPositions:
    customerServed[c] = False


#Step 3
def inPrevious(new,existing):
    start = existing[0]
    end = existing[len(existing)-1]
    if new == start:
        return 1
    elif new == end:
        return 0
    else:
        return -1

def capacityValid(existing,new):
    totalCap = customerPosDemand[new]
    for c in existing:
        totalCap+=customerPosDemand[c]

    return totalCap <= vehicleCap

def isServed(c):
    return customerServed[c]

def hasBeenServed(c):
    customerServed[c] = True             
     
routes = dict()
l = len(cust_pairs)
i = 0
idx = -1
truck = [0,0,0,0,0]

while (not(allCustomersConsidered(customerServed))):
    #choosing the maximum savings customers who are unserved
    for c in cust_pairs:
        if (isServed(c[0]) == False and isServed(c[1]) == False):
            hasBeenServed(c[0])
            hasBeenServed(c[1])
            idx += 1
            routes[idx] = ([c[0],c[1]]) 
            break
        
    #finding a cust that is either at the start or end of previous route
    for c in cust_pairs:
        res = inPrevious(c[0], routes[idx])
        if res == 0 and capacityValid(routes[idx], c[1]) and (isServed(c[1]) == False):
            if c[1] == (13,7):
                print customerServed[c[1]]
            hasBeenServed(c[1])
            routes[idx].append(c[1]) 
        elif res == 1 and capacityValid(routes[idx], c[1]) and (isServed(c[1]) == False):
            if c[1] == (13,7):
                print customerServed[c[1]]
            hasBeenServed(c[1])
            routes[idx].insert(0,c[1])
        
        else:
            res = inPrevious(c[1], routes[idx])
            if res == 0 and capacityValid(routes[idx], c[0]) and (isServed(c[0]) == False):
                if c[0] == (13,7):
                    print customerServed[c[0]]
                hasBeenServed(c[0])
                routes[idx].append(c[0]) 
            elif res == 1 and capacityValid(routes[idx], c[0]) and (isServed(c[0]) == False):
                if c[0] == (13,7):
                    print customerServed[c[0]]
                hasBeenServed(c[0])
                routes[idx].insert(0,c[0])


for point in customerPosDemand.keys():
    print point

print "--------------"

for r in routes.values():
    for point in r:
        print point

# printing each truck load
for r in routes.values():
    cap = 0
    for points in r:
        cap += customerPosDemand[points]
    print cap


#adding depot at ends
for r in routes.values():
    util.addDepotAtEnds(depot, r)

totalDist = 0
for k,v in routes.iteritems():
    totalDist += util.calculateRouteCost(v)
    print k,"-",v
print totalDist
 
# for i in range(l):
#     routes.append(depot)
#     if allCustomersConsidered(customerServed):
#         break
#     if customerServed[cust_pairs[i][0]] == False and customerServed[cust_pairs[i][1]] == False:
#         customerServed[cust_pairs[i][0]] = True
#         customerServed[cust_pairs[i][1]] = True
#         routes.append([cust_pairs[i][0],cust_pairs[i][1]])
#     for j in range(i+1,l):
#         if customerServed[cust_pairs[j][1]] == True:
#             continue
#         res = inPrevious(cust_pairs[j][0],routes[i])
#         if res == 0 and capacityValid(routes[i], cust_pairs[j][1]):
#             customerServed[cust_pairs[j][1]] = True
#             routes[i].append(cust_pairs[j][1]) #matched at end, add the other tuple at end
#         elif res == 1 and capacityValid(routes[i], cust_pairs[j][1]):
#             customerServed[cust_pairs[j][1]] = True
#             routes[i].insert(0,cust_pairs[j][1]) #matched at start, add the other tuple at start
#         
#         #try with the other tuple
#         else:
#             if customerServed[cust_pairs[j][0]] == True:
#                 continue
#             res = inPrevious(cust_pairs[j][1],routes[i])
#             if res == 0 and capacityValid(routes[i], cust_pairs[j][0]):
#                 customerServed[cust_pairs[j][0]] = True
#                 routes[i].append(cust_pairs[j][0]) #matched at end, add the other tuple at end
#             elif res == 1 and capacityValid(routes[i], cust_pairs[j][0]):
#                 customerServed[cust_pairs[j][0]] = True
#                 routes[i].insert(0,cust_pairs[j][0]) #matched at start, add the other tuple at start
# 
# repeat = []
# for r in routes:
#     if r in repeat and r != depot :
#         print "repeat"
#     elif len(r) > 2:
#         repeat.append(r)
#         
# print len(repeat)
# for r in repeat:
#     print r