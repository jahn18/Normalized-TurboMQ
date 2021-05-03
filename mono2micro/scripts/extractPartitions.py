"""
Extracts the business logic graph (paritioned by dynamic data via use cases) and the natural seam graph (partiioned by dynamic data via use cases and containment relationships).
python extractPartitions.py final_graph.json

"""

import sys
import json

def extractPartitions(jsonFilename):
    json_file =  open(jsonFilename,)
    partitions_json = json.load(json_file)

    # Business logic partition
    business_logic_graph_file = open("business_logic_graph.rsf", "x")
    for link in partitions_json["micro_detail_partition_by_business_logic"]["nodes"]:
        line = "contain" + " " + link["category"].replace(" ", "") + " " + link["name"].replace(" ", "") + "\n"
        business_logic_graph_file.write(line)

    # Natural seam partition
    natural_seam_graph_file = open("natural_seam_graph.rsf", "x")
    for link in partitions_json["micro_detail_partition_by_natural_seam"]["nodes"]:
        line = "contain" + " " + link["category"].replace(" ", "") + " " + link["name"].replace(" ", "") + "\n"
        natural_seam_graph_file.write(line)

if __name__ == "__main__":
    jsonFilename = sys.argv[1]
    extractPartitions(jsonFilename)

