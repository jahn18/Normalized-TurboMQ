import java.util.ArrayList;

public class TurboMQ {

    public static double computeTurboMQ(String clusteringFile, String dependencyFile) {
		RSFParser parser = new RSFParser(clusteringFile);
		parser.parseDependencyInputFile(dependencyFile);

		ArrayList<ArrayList<String>> clusteredItems = parser.getClusteredItems();
		int count = clusteredItems.size();

		double[][] interClusterDSM = new double[count][count];
		for(int c1 = 0; c1 < count; c1++) {
			ArrayList<String> elements1 = clusteredItems.get(c1);
			for(int c2 = c1+1; c2 < count; c2++) {
				ArrayList<String> elements2 = clusteredItems.get(c2);
				double total = 0;
				for(int e1 = 0; e1 < elements1.size(); e1++) {
					for(int e2 = 0; e2 < elements2.size(); e2++) {
						total += parser.dependency(elements1.get(e1), elements2.get(e2));
					}
				}
				interClusterDSM[c1][c2] = interClusterDSM[c2][c1] = total;
			}
		}

		double sum = 0;
		for (int i = 0; i < count; i++) {
			ArrayList<String> elements = clusteredItems.get(i);
			double u = 0;
			for(int e1 = 0; e1 < elements.size(); e1++) {
				for(int e2 = e1+1; e2 < elements.size(); e2++) {
					u += parser.dependency(elements.get(e1), elements.get(e2));
				}
			}
			double exdep = 0;
			for(int j = 0; j < count; j++) {
				exdep += interClusterDSM[i][j];
			}
			double cf = u /(u + 0.5*exdep);
			if(cf > 0)
				sum += cf;
		}
		//System.out.println(sum/count);
		//System.out.println(count);
		return (sum / count);
	}

	public static void main(String[] args) {
		//System.out.println("Working Directory = " + System.getProperty("user.dir"));
		String partitionsFile = "/newGraph.rsf";
		String dynamic_dep_file = "/deps/dynamicDep.rsf";
		String evolutionary_commit_dep_file = "/deps/commitsDep.rsf";
		String evolutionary_contri_dep_file = "/deps/contributorDep.rsf";
		String class_names_dep_file = "classname_dep_parts.rsf";
		String class_terms_dep_file = "/deps/classTermDep.rsf";
		String static_dep_file = "static_dep_parts.rsf";

		System.out.println("Partitions: Static");
		System.out.println(computeTurboMQ(partitionsFile, static_dep_file));

//		System.out.println("Partitions: Dynamic");
//		System.out.println(computeTurboMQ(partitionsFile, dynamic_dep_file));

		System.out.println("Partitions: Class Names");
		System.out.println(computeTurboMQ(partitionsFile, class_names_dep_file));

//		System.out.println("Partitions: Class Terms");
//		System.out.println(computeTurboMQ(partitionsFile, class_terms_dep_file));

//		System.out.println("Partitions: Contributor");
//		System.out.println(computeTurboMQ(partitionsFile, evolutionary_contri_dep_file));
//
//		System.out.println("Partitions: Commit");
//		System.out.println(computeTurboMQ(partitionsFile, evolutionary_commit_dep_file));
	}
}
