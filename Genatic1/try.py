import random, heapq, math

MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.5
POPULATION_SIZE = 100
FITNESS = 0
TRUCKS = 5
DEPOT = None
CAPACITY = 100
INF = float("inf")

class PrioritySet(object):
    
    def __init__(self):
        self.heap = []
        self.set = set()

    def push(self, d):
        if not d in self.set:
            heapq.heappush(self.heap, d)
            self.set.add(d)

    def pop(self):
        d = heapq.heappop(self.heap)
        self.set.remove(d)
        return d

    def size(self):
        return len(self.heap)

    def __str__(self):
        op = ""
        for i in self.heap:
            op += str(i[0]) + " : " + i[1].__str__()
            op += "\n"
        return op

    def __getitem__(self, index):
        return self.heap[index]

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

    def __str__(self):
        return str(self.name) #+ " -> (" + str(self.pos.x) + ", " + \
                #str(self.pos.y) + ") -> " + str(self.demand)

class VRP:

    def __init__(self):
        pass

    # methods

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
        # print "Yea i do it "
        # cross_point = (int)(getProb() * len(a))
        # new_a = a[:cross_point] + b[cross_point:]
        # new_b = b[:cross_point] + a[cross_point:]
        # return new_a, new_b

        cxpoint1, cxpoint2 = sorted(random.sample(range(len(a)), 2))
        temp1 = a[cxpoint1:cxpoint2+1] + b
        temp2 = b[cxpoint1:cxpoint2+1] + a
        new_a = []
        depo_count = 0
        for x in temp1:
            if x == DEPOT and depo_count < TRUCKS - 1:
                new_a.append(x)
                depo_count += 1
            elif x not in new_a:
                new_a.append(x)
        new_b = []
        depo_count = 0
        for x in temp2:
            if x == DEPOT and depo_count < TRUCKS - 1:
                new_b.append(x)
                depo_count += 1
            elif x not in new_b:
                new_b.append(x)
        return new_a, new_b
    
    return a, b

def getProb():
    return random.random()

# def getNodeSet():
#     return [1,2,3,4,5,6,7]

def get_random(li):
    index = random.randint(0, len(li)-1)
    return li[index]

def copy(li):
    return [i for i in li]

def get_fitness(li):
    # fitness = 0
    # # print req_chro
    # # print li
    # for i in range(len(li)):
    #     fitness += abs(li[i] - req_chro[i])
    # return fitness
    num_custo = len(li)
    fitness = 0

    for i in range(num_custo - 1):
        fitness += get_distance(li[i], li[i+1])

    fitness += get_distance(DEPOT, li[0])
    fitness += get_distance(li[-1], DEPOT)

    # chk for valid capacity
    temp = copy(li)
    temp.insert(0,DEPOT)
    temp.append(DEPOT)
    valid = 1
    curr_demand = 0
    for i in range(len(temp)):
        if temp[i] == DEPOT and curr_demand > CAPACITY:
            fitness = INF
        elif temp[i] == DEPOT:
            curr_demand = 0
        else:
            curr_demand += temp[i].demand

    # print_tuple(li)
    # print
    return fitness
    # return random.randint(0,100)


def get_distance(cus1, cus2):
    # Euclideian
    dist = 0 
    dist = math.sqrt(((cus1.pos.x - cus2.pos.x) ** 2) + ((cus1.pos.y - cus2.pos.y) ** 2))
    return dist

def getPopulationFitness(p):
    h = PrioritySet()
    for i in p:
        # print i,
        # print " -> " + str(get_fitness(i))
        # print_tuple(i)
        h.push((get_fitness(i),i))
    return h

def print_tuple(t):
    print "0", 
    for i in t:
        print i,        
    print "0 ",
    print " -> f: " + str(get_fitness(t))

def Genatic_Algo():
    print "here"
    minimum_chrom = h[0]
    # print str(minimum_chrom[0]) + " ",
    # print_tuple(minimum_chrom[1])
    count = 0
    while h[0][0] > 1000:
    # while count < 300:
        ax = h.pop()
        bx = h.pop()
        # print list(ax[1]),list(bx[1])
        a,b = crossover(list(ax[1]),list(bx[1]))
        # print a
        a = mutate(a)
        b = mutate(b)
        # print a
        h.push((get_fitness(a),tuple(a)))
        # print b
        h.push((get_fitness(b),tuple(b)))
        while h.size() < POPULATION_SIZE:
            TempSet = copy(Master_Chromosome)
            chromosome = []
            count += 1
            while len(TempSet) > 0:
                index = (int)(getProb() * len(TempSet))
                chromosome.append(TempSet.pop(index))
            h.push((get_fitness(chromosome),tuple(chromosome)))
        # print (str)(count+1) + " -> ",
        # # print a, " ",
        # print_tuple(a)
        # print " (" + str(len(a)) + ")",
        # print " -> ",
        # print_tuple(b)
        # print " (" + str(len(b)) + ")",
        # print
        # print b
        count = count + 1
        # print count
        if h[0][0] < minimum_chrom[0]:
            minimum_chrom = h[0] 
            print minimum_chrom[0]
    
    print minimum_chrom[0]
    print_tuple(minimum_chrom[1])
    print count
    # print h[0]
    # print h[1]
    # print h.size()

def initial():

    while len(population) < POPULATION_SIZE:
        TempSet = copy(Customers)
        chromosome = []
        while len(TempSet) > 0:
            index = (int)(getProb() * len(TempSet))
            chromosome.append(TempSet.pop(index))

        # chromosome.insert(0,DEPOT)
        # chromosome.append(DEPOT)                    
        if get_fitness(chromosome) != INF:
            population.add(tuple(chromosome))
        # print str(p) + " ",
        # print chromosome

def create_data_array():

    locations = [[82, 76], [96, 44], [50, 5], [49, 8], [13, 7], [29, 89], [58, 30], [84, 39],
                [14, 24], [12, 39], [3, 82], [5, 10], [98, 52], [84, 25], [61, 59], [1, 65],
                [88, 51], [91, 2], [19, 32], [93, 3], [50, 93], [98, 14], [5, 42], [42, 9],
                [61, 62], [9, 97], [80, 55], [57, 69], [23, 15], [20, 70], [85, 60], [98, 5]]

    demands =  [0, 19, 21, 6, 19, 7, 12, 16, 6, 16, 8, 14, 21, 16, 3, 22, 18,
                19, 1, 24, 8, 12, 4, 8, 24, 24, 2, 20, 15, 2, 14, 9]

    start_times =  [28842, 50891, 10351, 49370, 22553, 53131, 8908,
                    56509, 54032, 10883, 60235, 46644, 35674, 30304,
                    39950, 38297, 36273, 52108, 2333, 48986, 44552,
                    31869, 38027, 5532, 57458, 51521, 11039, 31063]

    for i in range(1,len(locations)):
        c = Customer(i)
        c.setPosition(locations[i][0],locations[i][1])
        c.setDemand(demands[i])
        Customers.append(c)
    
    i = 0
    c = Customer(i)
    c.setPosition(locations[i][0],locations[i][1])
    c.setDemand(demands[i])
    global DEPOT
    DEPOT = c

    for j in range(TRUCKS-1):
        Customers.append(DEPOT)

def print_population(p):

    for i in p:
        for c in i:
            print c,
        print "\n"
    
def print_population_heap(p):
    count = 1
    for i in p:
        print count, " )  "
        print_tuple(i[1])
        count += 1
        print "\n"

Customers = []
population = set()

if __name__ == '__main__':
    create_data_array()
    

# print Customers
initial()
# print_population(population)
h = getPopulationFitness(population)
# print_population_heap(h)
Genatic_Algo()