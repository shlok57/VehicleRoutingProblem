/**
 * Skeleton for this code is used from https://github.com/leonardean/CVRP
 * @author Chirayu Desai
 *
 */
public class Location {

	//The x coordinate of node at this location
	private int xCoordinate;
	
	//The y coordinate of node at this location
	private int yCoordinate;
	
	//The demand of node at this location
	private int demand;
	
	//The node number of node at this location
	private int nodeNumber;
	
	////The degree of node at this location
	private double degree;

	
	@SuppressWarnings("unused")
	private Location(){
		
	}
	
	//constructor
	public Location(int index, FileDataReaderGenerator fileDataReaderGenerator) {

		this.xCoordinate = fileDataReaderGenerator.getxCoordinates().get(index);
		this.yCoordinate = fileDataReaderGenerator.getyCoordinates().get(index);
		this.demand = fileDataReaderGenerator.getDemands().get(index);
		this.nodeNumber = index;
		this.degree = fileDataReaderGenerator.getDegrees().get(index);

	}

	public int getXCoordinate() {
		return xCoordinate;
	}

	public int getYCoordinate() {
		return yCoordinate;
	}

	public int getDemand() {
		return demand;
	}

	public int getNodeNumber() {
		return nodeNumber;
	}

	public double getDegree() {
		return degree;
	}

	public void setDegree(double degree) {
		this.degree = degree;
	}

	@Override
	public String toString() {
		return "X: " + xCoordinate + ", Y: " + yCoordinate + ", Demand: " + demand + ", Index: "
				+ nodeNumber + ", Degree: " + degree;
	}

}