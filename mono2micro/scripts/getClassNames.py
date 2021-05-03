"""
Retrieves all the class names that exist within the application. Requires the file_graph.json file.
ex.) python getClassNames file_graph.json symTable.json

"""

import sys
import json

def getClassNames(finalGraphFile):
     json_file =  open(finalGraphFile,)
     partitions_json = json.load(json_file)

     # Gets all class names
     class_names_graph_file = open("class_names.csv", "x")
     for link in partitions_json["micro_detail_partition_by_business_logic"]["nodes"]:
         line = link["name"].replace(" ", "") + "\n"
         class_names_graph_file.write(line)

if __name__ == "__main__":
    finalGraphFile = sys.argv[1]
    getClassNames(finalGraphFile)
