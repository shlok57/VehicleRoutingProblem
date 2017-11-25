import heapq
import random, math

################  CONSTANTS  #######################

MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.5
POPULATION_SIZE = 100
FITNESS = 0
TRUCKS = 10
DEPOT = None
CAPACITY = 220
INF = float("inf")

################  CLASSES  ###########################

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

    def poop(self):
        d = self.heap[-1]
        self.heap = self.heap[:-1]
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
    
###################   UTIL FUNCTIONS   ###################################


def copy(li):
    return [i for i in li]

def getProb():
    return random.random()

def get_random(li):
    index = random.randint(0, len(li)-1)
    return li[index]

def get_distance(cus1, cus2):
    # Euclideian
    dist = 0 
    dist = math.sqrt(((cus1.pos.x - cus2.pos.x) ** 2) + ((cus1.pos.y - cus2.pos.y) ** 2))
    return dist

def print_tuple(t):
    print "0", 
    for i in t:
        print i,        
    print "0 ",
    print " -> f: " + str(get_fitness(t))

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

def _pickpivots(self):
        left = random.randint(1, num_cities - 2)
        right = random.randint(left, num_cities - 1)
        return left, right

###################   HELPER FUNCTIONS   #################################

def mutate(chromosome):

    temp = [i for i in chromosome]
    
    if getProb() < MUTATION_RATE:
        left = random.randint(1, len(temp) - 2)
        right = random.randint(left, len(temp) - 1)   
        temp[left], temp[right] = temp[right], temp[left]
    # print temp_chromosome
    # replaceSet = []
    # for i in chromosome:
    #     if getProb() < MUTATION_RATE:
    #         replaceSet.append(i)
    #         index = temp_chromosome.index(i)
    #         temp_chromosome[index] = -1
    
    # for i in temp_chromosome:
    #     if i == -1:
    #         index = temp_chromosome.index(i)
    #         new_cust = get_random(replaceSet)
    #         temp_chromosome[index] = new_cust
    #         replaceSet.remove(new_cust)
    
    return temp


def crossover(a,b):

    if getProb() < CROSSOVER_RATE:
        # cxpoint1, cxpoint2 = sorted(random.sample(range(len(a)), 2))
        # temp1 = a[cxpoint1:cxpoint2+1] + b
        # temp2 = b[cxpoint1:cxpoint2+1] + a
        # new_a = []
        # depo_count = 0
        # for x in temp1:
        #     if x == DEPOT and depo_count < TRUCKS - 1:
        #         new_a.append(x)
        #         depo_count += 1
        #     elif x not in new_a:
        #         new_a.append(x)
        # new_b = []
        # depo_count = 0
        # for x in temp2:
        #     if x == DEPOT and depo_count < TRUCKS - 1:
        #         new_b.append(x)
        #         depo_count += 1
        #     elif x not in new_b:
        #         new_b.append(x)
        # return new_a, new_b
        left = random.randint(1, len(a) - 2)
        right = random.randint(left, len(a) - 1)
        # print left, " ", right
        c1 = [c for c in a[0:] if c not in b[left:right+1]]
        # print len(c1)
        p1 = c1[:left] + b[left:right+1] + c1[left:]
        # print len(p1)
        c2 = [c for c in b[0:] if c not in a[left:right+1]]
        p2 = c2[:left] + a[left:right+1] + c2[left:]

        # print_tuple(a)
        # print_tuple(b)
        # print_tuple(p1)
        # print_tuple(p2)
        # raw_input()
    
    return a, b


def get_fitness(li):
    
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

    return fitness
    # return random.randint(0,100)

def getPopulationFitness(p):
    
    h = PrioritySet()
    for i in p:
        h.push((get_fitness(i),i))
    return h

def create_new():

    TempSet = copy(Customers)
    chromosome = []
    while len(TempSet) > 0:
        index = (int)(getProb() * len(TempSet))
        chromosome.append(TempSet.pop(index))

    return chromosome 

#####################   EVOLUTION FUNTION   ##############################

def Genatic_Algo():
    
    print "POPULATION GENERATED... EVOLUTION BEGINING ..."
    minimum_chrom = h[0]
    count = 0
    # while h[0][0] > 1800:
    while count < 10000:
        ax = h.pop()
        bx = h.pop()
        a,b = crossover(list(ax[1]),list(bx[1]))
        a = mutate(a)
        # while get_fitness(a) == INF:
        #     a = create_new()
        b = mutate(b)
        # while get_fitness(b) == INF:
        #     b = create_new()
        # print a
        h.push((get_fitness(a),tuple(a)))
        # print b
        h.push((get_fitness(b),tuple(b)))
        while h.size() < POPULATION_SIZE:
            TempSet = copy(Customers)
            chromosome = []
            count += 1
            while len(TempSet) > 0:
                index = (int)(getProb() * len(TempSet))
                chromosome.append(TempSet.pop(index))
            h.push((get_fitness(chromosome),tuple(chromosome)))
        count = count + 1
        
        if count % 1000 == 0:
            print count,
            print " Generation done"

        if h[0][0] < minimum_chrom[0]:
            minimum_chrom = h[0] 
            print "CurrMin: ",
            print minimum_chrom[0]
    
    print_tuple(minimum_chrom[1])
    print count
    

#####################   INITIAL POPULATION   #############################

def initialize_population():

    while len(population) < POPULATION_SIZE:
        TempSet = copy(Customers)
        chromosome = []
        while len(TempSet) > 0:
            index = (int)(getProb() * len(TempSet))
            chromosome.append(TempSet.pop(index))

        if get_fitness(chromosome) != INF:
            population.add(tuple(chromosome))
    
########################   DATA   ########################################

def create_data_array():

    # locations = [[82, 76], [96, 44], [50, 5], [49, 8], [13, 7], [29, 89], [58, 30], [84, 39],
    #             [14, 24], [12, 39], [3, 82], [5, 10], [98, 52], [84, 25], [61, 59], [1, 65],
    #             [88, 51], [91, 2], [19, 32], [93, 3], [50, 93], [98, 14], [5, 42], [42, 9],
    #             [61, 62], [9, 97], [80, 55], [57, 69], [23, 15], [20, 70], [85, 60], [98, 5]]

    # demands =  [0, 19, 21, 6, 19, 7, 12, 16, 6, 16, 8, 14, 21, 16, 3, 22, 18,
    #             19, 1, 24, 8, 12, 4, 8, 24, 24, 2, 20, 15, 2, 14, 9]

    locations = [(40,40) ,(22,22) ,(36,26) ,(21,45) ,(45,35) ,(55,20) ,(33,34) ,(50,50) ,(55,45) ,
                    (26,59) ,(40,66) ,(55,65) ,(35,51) ,(62,35) ,(62,57) ,(62,24) ,(21,36) ,(33,44) ,(9,56) ,
                    (62,48) ,(66,14) ,(44,13) ,(26,13) ,(11,28) ,(7,43) ,(17,64) ,(41,46) ,(55,34) ,(35,16) ,
                    (52,26) ,(43,26) ,(31,76) ,(22,53) ,(26,29) ,(50,40) ,(55,50) ,(54,10) ,(60,15) ,
                    (47,66) ,(30,60) ,(30,50) ,(12,17) ,(15,14) ,(16,19) ,(21,48) ,(50,30) ,(51,42) ,(50,15) ,
                    (48,21) ,(12,38) ,(15,56) ,(29,39) ,(54,38) ,(55,57) ,(67,41) ,(10,70) ,(6,25) ,      
                    (65,27) ,(40,60) ,(70,64) ,(64,4) ,(36,6) ,(30,20) ,(20,30) ,(15,5) ,(50,70) ,(57,72) ,
                    (45,42) ,(38,33) ,(50,4) ,(66,8) ,(59,5) ,(35,60) ,(27,24) ,(40,20) ,(40,37)]
    
    demands = [0,18,26,11,30,21,19,15,16,29,26,37,16,12,31,8,19,20,13,15,22,28,12,6,27,14,
                18,17,29,13,22,25,28,27,19,10,12,14,24,16,33,15,11,18,17,21,27,19,20,5,22,
                12,19,22,16,7,26,14,21,24,13,15,18,11,28,9,37,30,10,8,11,3,1,6,10,20]

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

#####################   MAIN   ########################################### 

Customers = []
population = set()

if __name__ == '__main__':
    create_data_array()
    initialize_population()
    # print_population(population)
    h = getPopulationFitness(population)
    # print_population_heap(h)
    Genatic_Algo()