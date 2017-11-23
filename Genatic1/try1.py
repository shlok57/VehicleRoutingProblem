import random, heapq

MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.5
POPULATION_SIZE = 1000
Master_Chromosome = [1,2,3,4,5,6,7,8,9]

req_chro = [3,5,1,8,9,2,7,4,6]
count = 0

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
            op += str(i)
            op += "\n"
        return op

    def __getitem__(self, index):
        return self.heap[index]

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
        for x in temp1:
            if x not in new_a:
                new_a.append(x)
        new_b = []
        for x in temp2:
            if x not in new_b:
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

population = set()

while len(population) <= POPULATION_SIZE:
    TempSet = copy(Master_Chromosome)
    chromosome = []
    while len(TempSet) > 0:
        index = (int)(getProb() * len(TempSet))
        chromosome.append(TempSet.pop(index))            
    population.add(tuple(chromosome))
    # print str(p) + " ",
    # print chromosome

def get_fitness(li):
    fitness = 0
    # print req_chro
    # print li
    for i in range(len(li)):
        fitness += abs(li[i] - req_chro[i])
    return fitness

def getPopulationFitness(p):
    h = PrioritySet()
    for i in p:
        # print i,
        # print " -> " + str(get_fitness(i))
        h.push((get_fitness(i),i))
    return h

# print population
h = getPopulationFitness(population)
print h

while True: # count < 10000:
    ax = h.pop()
    bx = h.pop()
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
        while len(TempSet) > 0:
            index = (int)(getProb() * len(TempSet))
            chromosome.append(TempSet.pop(index))
        h.push((get_fitness(chromosome),tuple(chromosome)))
    print (str)(count+1) + " -> ",
    print a, " ",
    print " -> ",
    print b
    # print b
    count = count + 1
    if a == req_chro or b == req_chro:
        print "hurray"
        break

print h[0]
print h[1]
print h.size()