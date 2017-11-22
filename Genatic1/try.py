class Position:

    def __init__(self,x,y):
        self.x = x
        self.y = y		

    def __str__(self):
        return "(" + self.x + ", " + self.y + ") "

    def x_coor(self):
        return self.x

    def y_coor(self):
        return self.y

class Vehicle:

    def __init__(self, capacity):
        self.capacity = capacity

    def capacity(self):
        return self.capacity

class Customer:

    pos = Position(-1,-1)
    demand = 0

    def __init__(self,name):
        self.name = name

    def setPosition(self,x,y):
        self.pos = Position(x, y)

    def setDemand(self,d):
        self.demand = d

class VRP:

    def __init__:
        pass

    //methods

def mutate(chromosome):

    temp_chromosome = [i for i in chromosome]
    # print temp_chromosome
    # temp_nodeset = getNodeSet()
    replaceSet = []
    for i in chromosome:
        if getProb() < MUTATION_RATE:
            replaceSet.append(i)
            index = temp_chromosome.index(i)
            temp_chromosome[index] = -1
    
    # print temp_chromosome
    # print replaceSet

    for i in temp_chromosome:
        if i == -1:
            index = temp_chromosome.index(i)
            new_cust = get_random(replaceSet)
            temp_chromosome[index] = new_cust
            replaceSet.remove(new_cust)
    
    return temp_chromosome

def copy(li):
    return [i for i in li]

def crossover(a,b):

    if getProb() < CROSSOVER_RATE:
        cross_point = (int)(getProb() * len(a))
        new_a = a[:cross_point] + b[cross_point+1:]
        new_b = b[:cross_point] + a[cross_point+1:]
    
    return new_a, new_b