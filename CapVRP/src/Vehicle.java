import java.util.ArrayList;
/**
 * Skeleton for this code is used from https://github.com/leonardean/CVRP
 * @author Chirayu Desai
 *
 */
public class Vehicle {

	//The index of depot on the map
	private static final int DEPOT = 1;

	//The current remaining capacity of the vehicle
	private int remainingCapacity;
	
	//The current length of route of the vehicle
	private double lengthOfRoute;
	
	//The current location of the vehicle
	private Location location;
	
	//The current route of the vehicle
	private ArrayList<Location> route;
	
	//The node numbers of the nodes in the current route of the vehicle
	private ArrayList<Integer> routeNodeNumber;

	@SuppressWarnings("unused")
	private Vehicle() {

	}

	//constructor
	public Vehicle(FileDataReaderGenerator fileDataReaderGenerator) {
		route = new ArrayList<Location>();
		routeNodeNumber = new ArrayList<Integer>();
		this.remainingCapacity = fileDataReaderGenerator.getCapacity();
		this.lengthOfRoute = 0;
		this.location = new Location(DEPOT, fileDataReaderGenerator);
		this.route.add(new Location(DEPOT, fileDataReaderGenerator));
		this.routeNodeNumber.add(DEPOT);
	}

	/**
	 * prints the route
	 */
	public void printRoute() {
		String result = routeNodeNumber.get(0).toString();
		for (int i = 1; i < routeNodeNumber.size(); i++)
			result += ">" + routeNodeNumber.get(i).toString();
		System.out.println(result);
	}

	public void setRemainingCapacity(int remaining) {
		this.remainingCapacity = remaining;
	}

	public void setLocation(Location location) {
		this.location = location;
	}

	public void addRoute(Location dest) {
		this.route.add(dest);
	}

	public void addRouteNumber(int dest) {
		this.routeNodeNumber.add(dest);
	}

	public int getRemainingCapacity() {
		return remainingCapacity;
	}

	public Location getLocation() {
		return location;
	}

	public ArrayList<Location> getRoute() {
		return route;
	}

	public ArrayList<Integer> getRouteNumber() {
		return routeNodeNumber;
	}

	public void addLengthOfRoute(double length) {
		this.lengthOfRoute += length;
	}

	public double getLengthOfRoute() {
		return this.lengthOfRoute;
	}
}