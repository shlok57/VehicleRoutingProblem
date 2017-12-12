import json
import operator
from math import degrees, atan2, sqrt
import random
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2


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
        # return str(self.name) #+ " -> (" + str(self.pos.x) + ", " + \
                #str(self.pos.y) + ") -> " + str(self.demand)
        return "(" + str(self.pos.x) + ", " + \
                   str(self.pos.y) + " )"

def print_tuple(t):
    print "[", 
    for i in t:
        print i,        
    print "]"

def copy(li):
    return [i for i in li]

def get_distance(cus1, cus2):
    # Euclideian
    dist = 0 
    dist = sqrt(((cus1.pos.x - cus2.pos.x) ** 2) + ((cus1.pos.y - cus2.pos.y) ** 2))
    return dist

def calculateDepotAngle(x,y,depot_x,depot_y):
    angle = degrees(atan2(y - depot_y, x - depot_x))
    bearing = (90 - angle) % 360
    return bearing

def make_dictionary(route):
    global route_node
    route_node = {}
    counter = 0
    for r in route:
        route_node[counter] = r
        counter += 1
    # for k in route_node.keys():
    #     print k, " ", route_node[k]

def get_route(route):
    final = []
    for r in route:
        final.append(route_node[r])
    return final

def get_demand_route(route):
    route_demand = 0
    for c in route:
        route_demand += c.demand
    return route_demand

def get_cost_route(route):
    route_cost = 0
    for i in range(len(route)- 1):
        route_cost += get_distance(route[i], route[i+1])
    return route_cost

def print_solution(final_routes):
    COST = 0
    for r in final_routes:
        print_tuple(r)
        print get_demand_route(r)
        cost = get_cost_route(r)
        print cost
        COST += cost 
    print "Total Cost = ", COST

def Distance(i, j):
    I = route_node[i]
    J = route_node[j]
    # print "here ", I
    # print J
    return get_distance(I,J)

def TSP(size):
  # Create routing model
    route_list = []
    if size > 0:
        # TSP of size args.tsp_size
        # Second argument = 1 to build a single tour (it's a TSP).
        # Nodes are indexed from 0 to parser_tsp_size - 1, by default the start of
        # the route is node 0.
        routing = pywrapcp.RoutingModel(size, 1, 0)

        search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
        # Setting first solution heuristic (cheapest addition).
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        routing.SetArcCostEvaluatorOfAllVehicles(Distance)
        # Forbid node connections (randomly).
        rand = random.Random()
        rand.seed(0)

        assignment = routing.Solve()
        if assignment:
            # Solution cost.
            # print(assignment.ObjectiveValue())
            # Inspect solution.
            # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1
            route_number = 0
            node = routing.Start(route_number)
            route = ''
            while not routing.IsEnd(node):
                route += str(node) + ' -> '
                route_list.append(node)
                node = assignment.Value(routing.NextVar(node))
            route += '0'
            route_list.append(0)
            # print(route)
        else:
            print('No solution found.')
            return -1
    return route_list


with open('data36.json') as inputFile:
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
route_node = {}
clusters = list()
final_routes = list()
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
        
# print get_distance(DEPOT,Customers[0])
clusters.append(tempCluster)
for c in clusters:
    c.insert(0,DEPOT)
    # print_tuple(c)
    make_dictionary(c)
    route = TSP(len(c))
    # print route
    route = get_route(route)
    final_routes.append(route)

print_solution(final_routes)