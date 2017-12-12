import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

/**
 * 
 * @author Chirayu Desai
 *
 */
public class FileDataReaderGenerator {

	//The capacity of each vehicle in the homogeneous fleet of vehicles
	private int capacity;
	
	//The number of customers
	private int numNodes;
	
	//Numbers identifying each node
	private ArrayList<Integer> nodeNumber;
	
	//The x coordinates of nodes
	private ArrayList<Integer> xCoordinates;
	
	//The y coordinates of nodes
	private ArrayList<Integer> yCoordinates;
	
	//The demands of nodes
	private ArrayList<Integer> demands;
	
	//The degree measures of nodes with respect to the depots location
	private ArrayList<Double> degrees;

	//constructor
	public FileDataReaderGenerator() {
		this.setCapacity(0);
		this.setNumNodes(0);
		this.nodeNumber = new ArrayList<Integer>();
		this.xCoordinates = new ArrayList<Integer>();
		this.yCoordinates = new ArrayList<Integer>();
		this.demands = new ArrayList<Integer>();
		this.degrees = new ArrayList<Double>();

	}

	/**
	 * @param filename, name of file to parse vrp data from
	 * @return a FileDataReaderGenerator object with fields set from data parsed from given file
	 */
	public static FileDataReaderGenerator getDataFromFile(String filename) {

		FileDataReaderGenerator fileDataReaderGenerator = new FileDataReaderGenerator();
		try (BufferedReader br = new BufferedReader(new FileReader(filename))) {

			String sCurrentLine;
			fileDataReaderGenerator.setCapacity(Integer.parseInt(br.readLine()));
			fileDataReaderGenerator.setNumNodes(Integer.parseInt(br.readLine()));
			int lineNumber = 0;
			while ((sCurrentLine = br.readLine()) != null) {
				fileDataReaderGenerator = fileDataReaderGenerator
						.populateData(fileDataReaderGenerator, sCurrentLine, lineNumber);
				lineNumber++;
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		return fileDataReaderGenerator;
	}

	
	/**
	 * Populates the fields for FileDataReaderGenerator object
	 * @param fileDataReaderGenerator FileDataReaderGenerator object
	 * @param line the current line in file as a string
	 * @param lineNumber the number of the current line in file
	 * @return updated FileDataReaderGenerator object
	 */
	private FileDataReaderGenerator populateData(FileDataReaderGenerator fileDataReaderGenerator,
			String line, int lineNumber) {
		String[] dataArray = line.split("\t");
		int x = Integer.parseInt(dataArray[1]);
		int y = Integer.parseInt(dataArray[2]);
		fileDataReaderGenerator.nodeNumber.add(Integer.parseInt(dataArray[0]));
		fileDataReaderGenerator.xCoordinates.add(x);
		fileDataReaderGenerator.yCoordinates.add(y);
		fileDataReaderGenerator.demands.add(Integer.parseInt(dataArray[3]));
		if (lineNumber > 1) {
			int depotX = fileDataReaderGenerator.getxCoordinates().get(1);
			int depotY = fileDataReaderGenerator.getyCoordinates().get(1);
			fileDataReaderGenerator.degrees.add(getAngle(depotX, depotY, x, y));

		} else {
			fileDataReaderGenerator.degrees.add(450.00);
		}
		return fileDataReaderGenerator;
	}

	/**
	 * 
	 * @param x1 the x coordinate of the first point
	 * @param y1 the y coordinate of the first point
	 * @param x2 the x coordinate of the second point
	 * @param y2 the y coordinate of the second point
	 * @return the positive angle in degrees between the two given points
	 */
	public double getAngle(int x1, int y1, int x2, int y2) {

		double angle = (double) Math.toDegrees(Math.atan2(y2 - y1, x2 - x1));
		if (angle < 0) {
			angle += 360;
		}
		return angle;
	}

	public int getCapacity() {
		return capacity;
	}

	public void setCapacity(int capacity) {
		this.capacity = capacity;
	}

	public int getNumNodes() {
		return numNodes;
	}

	public void setNumNodes(int numNodes) {
		this.numNodes = numNodes;
	}

	public ArrayList<Integer> getNodeNumber() {
		return nodeNumber;
	}

	public void setNodeNumber(ArrayList<Integer> nodeNumber) {
		this.nodeNumber = nodeNumber;
	}

	public ArrayList<Integer> getxCoordinates() {
		return xCoordinates;
	}

	public void setxCoordinates(ArrayList<Integer> xCoordinates) {
		this.xCoordinates = xCoordinates;
	}

	public ArrayList<Integer> getyCoordinates() {
		return yCoordinates;
	}

	public void setyCoordinates(ArrayList<Integer> yCoordinates) {
		this.yCoordinates = yCoordinates;
	}

	public ArrayList<Integer> getDemands() {
		return demands;
	}

	public void setDemands(ArrayList<Integer> demands) {
		this.demands = demands;
	}

	public ArrayList<Double> getDegrees() {
		return degrees;
	}

	public void setDegrees(ArrayList<Double> degrees) {
		this.degrees = degrees;
	}
}