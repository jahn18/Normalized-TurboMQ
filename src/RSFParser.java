import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.StringTokenizer;

public class RSFParser {
	private ArrayList<ArrayList<String>> clusteredItems;
	private HashMap<String, Integer> name2ID;
	private int totalItemCount;
	private double dsm[][];
	
	public ArrayList<ArrayList<String>> getClusteredItems() {
		return clusteredItems;
	}
		
	public double dependency(String e1, String e2) {
		double sum = 0;
		if(dsm[name2ID.get(e1)][name2ID.get(e2)] != 0) {
			sum += dsm[name2ID.get(e1)][name2ID.get(e2)];
		}
		if(dsm[name2ID.get(e2)][name2ID.get(e1)] != 0) {
			sum += dsm[name2ID.get(e2)][name2ID.get(e1)];
		}
		return sum;
	}

	public RSFParser(String filename) {
		
		clusteredItems = new ArrayList<ArrayList<String>>();
		name2ID = new HashMap<String,Integer>();
		totalItemCount = 0;
		
		parseClusteringInputFile(filename);
		
		dsm = new double[totalItemCount][totalItemCount];
	}

	private void parseClusteringInputFile(String filename) {
		try {
			 File f = new File(".//" + filename);
			 BufferedReader reader = new BufferedReader(new FileReader(f));
			 String readLine = "";
			 String clusterName = "";
			 String currentCluster = "";
			 String itemName = "";
			 int clusterCount = 0;
			 
			 while ((readLine = reader.readLine()) != null) {
				 StringTokenizer tokenizer = new StringTokenizer(readLine); 
				 
				 tokenizer.nextToken(); // contains
				 
				 clusterName = tokenizer.nextToken();
				 if(!currentCluster.equals(clusterName)) {
					 currentCluster = clusterName;
					 clusterCount++;
					 clusteredItems.add(new ArrayList<String>());	 
				 } 
				 
				 itemName = tokenizer.nextToken();
				 clusteredItems.get(clusterCount-1).add(itemName);
				 name2ID.put(itemName, totalItemCount);
				 totalItemCount++;
			 }
			 reader.close();
		} catch (IOException e) {
			System.out.println("Error while reading an input file!");
			e.printStackTrace();
	    }
	}
	
	public void parseDependencyInputFile(String filename) {
		try {
			 File f = new File(".//" + filename);
			 BufferedReader reader = new BufferedReader(new FileReader(f));
			 String readLine = "";
			 String itemName = "";
			 String itemName2 = "";
			 String dependencyValue = "";

			while ((readLine = reader.readLine()) != null) {
				 StringTokenizer tokenizer = new StringTokenizer(readLine); 
				 //tokenizer.nextToken(); // depends
				 itemName = tokenizer.nextToken();
				 itemName2 = tokenizer.nextToken();
				 dependencyValue = tokenizer.nextToken();
				 dsm[name2ID.get(itemName)][name2ID.get(itemName2)] = Double.parseDouble(dependencyValue);
			 }
			 reader.close();
		} catch (IOException e) {
			System.out.println("Error while reading an input file!");
			e.printStackTrace();
	    } 
	}
}
