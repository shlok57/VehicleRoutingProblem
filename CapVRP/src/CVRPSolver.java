import java.util.ArrayList;
import java.util.Random;
import java.util.SortedSet;
import java.util.TreeSet;

/**
 * Skeleton and some of the methods for this code is used from
 * https://github.com/leonardean/CVRP
 * 
 * @author Chirayu Desai
 *
 */
public class CVRPSolver {

	// Index of Depot
	private static final int DEPOT = 1;

	// An ArrayList with the current state of locations(Nodes)
	private ArrayList<Location> locations;

	// An ArrayList with the original state of locations(Nodes)
	private ArrayList<Location> locationsCopy;

	// Population Represented as an ArrayList of Routes, which in turn are
	// ArrayLists of Node Numbers
	private ArrayList<ArrayList<Integer>> population;

	// The best Solution(Routes) found so far
	private ArrayList<ArrayList<Integer>> bestRoutes;

	// The Cost of the best Solution so far
	private double bestCost = 99999;

	// To extract and initialize data
	private FileDataReaderGenerator fileDataReaderGenerator;

	public static void main(String[] args) {

		// The Number of Individuals in the Initial Population
		int populationNumber; // 100

		// The Number of Generation for which genetic Algorithm will work
		int numberOfGenerations; // 500

		// The crossover rate
		int crossoverRate; // 70

		// The mutation Rate
		int mutationRate; // 5

		// The path of cvrp data file
		String datafilePath;

		// Flag to keep track of command line arguments presence
		boolean commandLineArgsPresent = false;

		//initialize parameter values
		if (args.length == 0) {
			populationNumber = 100;
			numberOfGenerations = 100;
			crossoverRate = 70;
			mutationRate = 5;
			datafilePath = "data/fruitybun75.txt";
		} else {
			populationNumber = Integer.parseInt(args[0]);
			numberOfGenerations = Integer.parseInt(args[1]);
			crossoverRate = (int) (Double.parseDouble(args[2]) * 100.00);
			mutationRate = (int) (Double.parseDouble(args[3]) * 100.00);
			datafilePath = args[4];
			commandLineArgsPresent = true;
		}

		CVRPSolver cvrp = new CVRPSolver();

		
		if (commandLineArgsPresent) {
			System.out.println(cvrp.getClass().getName() + " -> Received Inputs In Main : \n"
					+ "Population Number: " + args[0] + ", Number of Generations : " + args[1]
					+ ", Crossover Rate: " + args[2] + ", Mutation Rate : " + args[3]
					+ ", Data File Path : " + args[4]);

		} else {
			System.out.println(cvrp.getClass().getName()
					+ " -> No command line inputs received finding solution for default inputs");
		}

		
		System.out.println(cvrp.getClass().getName()
				+ " -> Finding solution with following parameters : \n" + "Population Number: "
				+ populationNumber + ", Number of Generations : " + numberOfGenerations
				+ ", Crossover Rate: " + crossoverRate + ", Mutation Rate : " + mutationRate
				+ ", Data File Path : " + datafilePath);

		
		// Set dataReaderGenerator
		cvrp.setFileDataReaderGenerator(FileDataReaderGenerator.getDataFromFile(datafilePath));

		// run Greedy search and genetic algorithm
		cvrp.run(populationNumber, numberOfGenerations, crossoverRate, mutationRate);

		// Print Solutions
		if (cvrp.allNodesVisited(cvrp.bestRoutes, cvrp.getFileDataReaderGenerator())) {
			System.out.println("Best Solution Route: ");
			for (int i = 0; i < cvrp.bestRoutes.size(); i++) {
				System.out.println(cvrp.bestRoutes.get(i));
				/*
				 * for (int locIndex : cvrp.bestRoutes.get(i)) {
				 * System.out.println(cvrp.getFileDataReaderGenerator().getxCoordinates()
				 * .get(locIndex) + "," +
				 * cvrp.getFileDataReaderGenerator().getyCoordinates().get(locIndex)); }
				 */
			}
			System.out.println("Best Solution Cost: " + cvrp.bestCost);
			System.out.println("Best Solution Number of Vehicles: " + cvrp.bestRoutes.size());
		} else {
			System.out.println("Not All Nodes Could Be Visited for given capacity constraint");
			System.out.println("Partial Solution Route: ");
			for (int i = 0; i < cvrp.bestRoutes.size(); i++) {
				System.out.println(cvrp.bestRoutes.get(i));
			}
			System.out.println("Partial Solution Cost: " + cvrp.bestCost);
			System.out.println("Partial Solution Number of Vehicles: " + cvrp.bestRoutes.size());
		}

	}

	/**
	 * run Greedy search and genetic algorithm over generations
	 * 
	 * @param populationNumber
	 * @param numberOfGenerations
	 * @param crossoverRate
	 * @param mutationRate
	 */
	private void run(int populationNumber, int numberOfGenerations, int crossoverRate,
			int mutationRate) {

		// Initialize the data order locations in which they are to be traversed
		initailizeData();

		// Best Greedy Route for each ONE Vehicle
		ArrayList<Integer> bestRouteForVehicle = new ArrayList<Integer>();

		// Best Solution Routes
		ArrayList<ArrayList<Integer>> bestSolutionRoutes = new ArrayList<ArrayList<Integer>>();

		double bestCostSoFar = 9999;
		double totalBestCost = 0;

		// A Vehicle
		Vehicle vehicle;

		do {
			bestCostSoFar = 9999;
			vehicle = new Vehicle(fileDataReaderGenerator);

			makeClusterForVehicle(vehicle);

			if (vehicle.getRouteNumber().size() <= 2)
				break;
			ArrayList<Integer> routeConvert = new ArrayList<Integer>();

			for (int i = 0; i < vehicle.getRoute().size(); i++)
				routeConvert.add(vehicle.getRoute().get(i).getNodeNumber());

			generatePopulation(routeConvert, populationNumber);

			for (int i = 0; i < numberOfGenerations; i++) {
				crossOver(crossoverRate);
				mutate(mutationRate);
				for (int j = 0; j < population.size(); j++) {
					if (calcuateRouteCost(
							new ArrayList<Integer>(population.get(j))) < bestCostSoFar) {
						bestCostSoFar = calcuateRouteCost(
								new ArrayList<Integer>(population.get(j)));
						bestRouteForVehicle = new ArrayList<Integer>(population.get(j));
					}
				}
			}
			totalBestCost += bestCostSoFar;
			bestSolutionRoutes.add(new ArrayList<Integer>(bestRouteForVehicle));
		} while (vehicle.getRoute().size() > 2);

		if (totalBestCost < bestCost) {
			bestCost = totalBestCost;
			bestRoutes = new ArrayList<ArrayList<Integer>>(bestSolutionRoutes);
		}
	}

	/**
	 * crossover the population using partially matched crossover
	 * 
	 * @param crossRate
	 * @return the resulting offspring's after crossover
	 */
	private ArrayList<ArrayList<Integer>> crossOver(int crossRate) {
		ArrayList<ArrayList<Integer>> nextGen = new ArrayList<ArrayList<Integer>>();
		ArrayList<ArrayList<Integer>> parents = new ArrayList<ArrayList<Integer>>();
		ArrayList<Integer> parent1 = new ArrayList<Integer>();
		ArrayList<Integer> parent2 = new ArrayList<Integer>();
		ArrayList<Integer> child1 = new ArrayList<Integer>();
		ArrayList<Integer> child2 = new ArrayList<Integer>();
		Random random = new Random();
		int position1 = 0;
		int position2 = 0;
		while (population.size() != 0) {
			parents = getParents(crossRate);
			parent1 = parents.get(0);
			parent2 = parents.get(1);
			child1 = parent1;
			child2 = parent2;
			position1 = random.nextInt(parent1.size() - 2) + 1;
			position2 = random.nextInt(parent1.size() - 2 - position1 + 1) + position1 + 1;
			for (int j = position1; j <= position2; j++) {
				int gene1 = child1.get(j);
				int gene2 = child2.get(j);
				int tmp1 = gene2;
				int tmp2 = gene1;
				child1.set(child1.indexOf(gene2), gene1);
				child1.set(j, new Integer(tmp1));
				child2.set(child2.indexOf(gene1), gene2);
				child2.set(j, new Integer(tmp2));
			}
			nextGen.add(new ArrayList<Integer>(child1));
			nextGen.add(new ArrayList<Integer>(child2));
		}
		population = nextGen;
		return nextGen;
	}

	/**
	 * Pick two parents for crossover
	 * 
	 * @param crossRate
	 *            probability of picking two fittest parents
	 * @return two parents for crossover
	 */
	private ArrayList<ArrayList<Integer>> getParents(int crossRate) {
		Random random = new Random();
		ArrayList<ArrayList<Integer>> parent = new ArrayList<ArrayList<Integer>>();
		int prob = 0;
		double fitness = 0;
		while ((population.size() != 0) && (parent.size() < 2)) {
			prob = random.nextInt(population.size());
			if (prob < crossRate) {
				fitness = random.nextDouble() * getTotalFitness(population);
				if (fitness < getFitness(population, prob)) {
					parent.add(new ArrayList<Integer>(population.get(prob)));
					population.remove(prob);
				}
			}
		}
		return parent;
	}

	/**
	 * calculate the fitness for each chromosome
	 * 
	 * @param population
	 * @param index
	 * @return the fitness value of that chromosome
	 */
	private double getFitness(ArrayList<ArrayList<Integer>> population, int index) {
		double fitness = 0;
		double totalLength = 0;
		for (int i = 0; i < population.size(); i++) {
			totalLength += calcuateRouteCost(population.get(i));
		}
		fitness = totalLength / calcuateRouteCost(population.get(index));
		return fitness;
	}

	/**
	 * calculate the fitness of a population
	 * 
	 * @param population
	 * @return the total fitness of the population
	 */
	private double getTotalFitness(ArrayList<ArrayList<Integer>> population) {
		double totalFitness = 0;
		double totalLength = 0;
		for (int i = 0; i < population.size(); i++) {
			totalLength += calcuateRouteCost(population.get(i));
		}
		for (int i = 0; i < population.size(); i++) {
			totalFitness += totalLength / calcuateRouteCost(population.get(i));
		}
		return totalFitness;
	}

	/**
	 * make a population based on original route, with mutation rate of 50
	 * 
	 * @param route
	 * @param populationNumber
	 */
	private void generatePopulation(ArrayList<Integer> route, int populationNumber) {
		population = new ArrayList<ArrayList<Integer>>();
		ArrayList<Integer> tmp = new ArrayList<Integer>();
		for (int i = 0; i < populationNumber; i++) {
			tmp = mutateEach(route, 50);
			population.add(new ArrayList<Integer>(tmp));
		}
	}

	/**
	 * make the clusters of radially ordered nodes, until vehicles capacity
	 * is full.
	 * 
	 * @param vehicle
	 */
	private void makeClusterForVehicle(Vehicle vehicle) {

		for (int i = 2; i < locations.size(); i++) {

			if (locations.get(i) == null)
				continue;
			if (vehicle.getRemainingCapacity() < getDemand(i))
				break;
			if ((locations.get(i) != null) && (vehicle.getRemainingCapacity() >= getDemand(i))) {
				vehicle.setRemainingCapacity(vehicle.getRemainingCapacity() - getDemand(i));
				vehicle.addLengthOfRoute(getDist(vehicle.getLocation(), locations.get(i)));
				vehicle.setLocation(locations.get(i));
				vehicle.addRoute(locations.get(i));
				vehicle.addRouteNumber(i);
				locations.set(i, null);
			}
		}
		vehicle.addRoute(locations.get(DEPOT));
		vehicle.addRouteNumber(DEPOT);
		vehicle.addLengthOfRoute(getDist(vehicle.getLocation(), locations.get(DEPOT)));
	}

	/**
	 * route mutation, which switches the order of locations
	 * 
	 * @param mutationRate
	 */
	private void mutate(int mutationRate) {
		for (int i = 0; i < population.size(); i++) {
			population.set(i, mutateEach(population.get(i), mutationRate));
		}
	}

	/**
	 * @param route
	 * @param mutationRate
	 * @return the mutated variant of the given route
	 */
	private ArrayList<Integer> mutateEach(ArrayList<Integer> route, int mutationRate) {

		int temp;
		Random random = new Random();
		int probablity;
		for (int i = 1; i < route.size() - 1; i++) {
			probablity = random.nextInt(100);
			if (probablity <= mutationRate) {
				temp = 0;
				probablity = random.nextInt(route.size() - 2);
				temp = route.get(i);
				route.set(i, route.get(probablity + 1));
				route.set(probablity + 1, temp);
			}
		}
		return route;
	}

	/**
	 * @param route
	 * @return the cost of the given route
	 */
	private double calcuateRouteCost(ArrayList<Integer> route) {
		double result = 0;
		for (int i = 0; i < route.size() - 1; i++) {
			result += getDist(route.get(i), route.get(i + 1));
		}
		return result;
	}

	/**
	 * get the demand of a node by its index
	 * 
	 * @param index
	 *            of node
	 * @return the demand value at that node
	 */
	private int getDemand(int index) {
		return locations.get(index).getDemand();
	}

	/**
	 * Calculate the euclidean distance between two locations
	 * 
	 * @param from
	 *            Node number
	 * @param to
	 *            Node number
	 * @return the euclidean distance between two nodes
	 */
	private double getDist(int from, int to) {
		int x1 = locationsCopy.get(from).getXCoordinate();
		int y1 = locationsCopy.get(from).getYCoordinate();
		int x2 = locationsCopy.get(to).getXCoordinate();
		int y2 = locationsCopy.get(to).getYCoordinate();

		return Math.sqrt(Math.pow((x1 - x2), 2) + Math.pow((y1 - y2), 2));
	}

	/**
	 * Calculate the euclidean distance between two locations
	 * 
	 * @param from
	 *            node
	 * @param to
	 *            node
	 * @return the euclidean distance between two nodes
	 */
	public double getDist(Location from, Location to) {
		int x1 = from.getXCoordinate();
		int y1 = from.getYCoordinate();
		int x2 = to.getXCoordinate();
		int y2 = to.getYCoordinate();

		return Math.sqrt(Math.pow((x1 - x2), 2) + Math.pow((y1 - y2), 2));
	}

	/**
	 * initialize locations, put all the data into
	 */
	private void initailizeData() {

		locations = new ArrayList<Location>();
		locationsCopy = new ArrayList<Location>();
		for (int i = 0; i < getFileDataReaderGenerator().getNumNodes() + 1; i++) {
			locations.add(new Location(i, getFileDataReaderGenerator()));
		}

		ArrayList<Location> locsMapSortedByDegree = new ArrayList<Location>(locations);
		locsMapSortedByDegree.sort((l1, l2) -> Double.compare(l1.getDegree(), l2.getDegree()));
		Location tmpl = locsMapSortedByDegree.get(locsMapSortedByDegree.size() - 1);
		locsMapSortedByDegree.remove(tmpl);
		locsMapSortedByDegree.add(0, tmpl);
		tmpl = locsMapSortedByDegree.get(locsMapSortedByDegree.size() - 1);
		locsMapSortedByDegree.remove(tmpl);
		locsMapSortedByDegree.add(0, tmpl);

		locations = new ArrayList<Location>(locsMapSortedByDegree);

		for (int i = 0; i < getFileDataReaderGenerator().getNumNodes() + 1; i++)
			locationsCopy.add(new Location(i, getFileDataReaderGenerator()));

	}

	/**
	 * @param routes
	 * @param fileDataReaderGenerator
	 * @return true if all nodes except depot are visited once in the list of routes
	 */
	private boolean allNodesVisited(ArrayList<ArrayList<Integer>> routes,
			FileDataReaderGenerator fileDataReaderGenerator) {
		SortedSet<Integer> nodesInRoutes = new TreeSet<>();
		SortedSet<Integer> allNodes = new TreeSet<>(fileDataReaderGenerator.getNodeNumber());

		allNodes.remove(0);
		for (ArrayList<Integer> arrayList : routes) {
			for (Integer integer : arrayList) {
				nodesInRoutes.add(integer);
			}
		}
		return nodesInRoutes.containsAll(allNodes);
	}

	public FileDataReaderGenerator getFileDataReaderGenerator() {
		return fileDataReaderGenerator;
	}

	public void setFileDataReaderGenerator(FileDataReaderGenerator fileDataReaderGenerator) {
		this.fileDataReaderGenerator = fileDataReaderGenerator;
	}
}