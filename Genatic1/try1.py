import random, heapq

MUTATION_RATE = 0.2
CROSSOVER_RATE = 0.5
Master_Chromosome = [1,2,3,4,5,6]

req_chro = [3,5,1,2,4,6]
count = 0

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

def getNodeSet():
    return [1,2,3,4,5]

def get_random(li):
    index = random.randint(0, len(li)-1)
    return li[index]

def copy(li):
    return [i for i in li]

population = []

for p in range(100):
    TempSet = copy(Master_Chromosome)
    chromosome = []
    while len(TempSet) > 0:
        index = (int)(getProb() * len(TempSet))
        chromosome.append(TempSet.pop(index))            
    population.append(chromosome)
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
    h = []
    for i in p:
        # print i,
        # print " -> " + str(get_fitness(i))
        h.append((get_fitness(i),i))
    return h

# print population
h = getPopulationFitness(population)
heapq.heapify(h)
for i in h:
    print i


while count < 1000:
    ax = heapq.heappop(h)
    bx = heapq.heappop(h)
    a,b = crossover(ax[1],bx[1])
    # print a
    a = mutate(a)
    b = mutate(b)
    # print a
    heapq.heappush(h,(get_fitness(a),a))
    # print b
    heapq.heappush(h,(get_fitness(b),b))
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
