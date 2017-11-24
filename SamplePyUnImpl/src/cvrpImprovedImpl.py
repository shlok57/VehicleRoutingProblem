import json
import util
import operator
from audioop import reverse
import new
from ortools.constraint_solver._pywrapcp import new_BaseLns

with open('data1.json') as inputFile:
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

#initially none of the customers have been served
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
             
routes = list()
l = len(cust_pairs)

for i in range(l):
    if allCustomersConsidered(customerServed):
        break
    if customerServed[cust_pairs[i][0]] == False and customerServed[cust_pairs[i][1]] == False:
        customerServed[cust_pairs[i][0]] = True
        customerServed[cust_pairs[i][1]] = True
        routes.append([cust_pairs[i][0],cust_pairs[i][1]])
    for j in range(i+1,l-1):
        if customerServed[cust_pairs[j][1]] == True:
            continue
        res = inPrevious(cust_pairs[j][0],routes[i])
        if res == 0 and capacityValid(routes[i], cust_pairs[j][1]):
            customerServed[cust_pairs[j][1]] = True
            routes[i].append(cust_pairs[j][1]) #matched at end, add the other tuple at end
        elif res == 1 and capacityValid(routes[i], cust_pairs[j][1]):
            customerServed[cust_pairs[j][1]] = True
            routes[i].insert(0,cust_pairs[j][1]) #matched at start, add the other tuple at start
        
        #try with the other tuple
        else:
            if customerServed[cust_pairs[j][0]] == True:
                continue
            res = inPrevious(cust_pairs[j][1],routes[i])
            if res == 0 and capacityValid(routes[i], cust_pairs[j][0]):
                customerServed[cust_pairs[j][0]] = True
                routes[i].append(cust_pairs[j][0]) #matched at end, add the other tuple at end
            elif res == 1 and capacityValid(routes[i], cust_pairs[j][0]):
                customerServed[cust_pairs[j][0]] = True
                routes[i].insert(0,cust_pairs[j][0]) #matched at start, add the other tuple at start

# print len(routes)
for r in routes:
    print r
