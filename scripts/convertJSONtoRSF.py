"""
Converts the dependencies found in the mono2micro JSON dependency graphs into an RSF dependency file.

"""

import json
import sys

def convertJSONtoRSF(jsonFilename):
    json_file =  open(jsonFilename,)
    dependencies_json = json.load(json_file)

    mono_runtime_call_graph_file = open("mono_run_time_call_graph.rsf", "x")
    for link in dependencies_json["mono_run_time_call_graph"]["links"]:
        line = link["source"].replace(" ", "") + " " + link["target"].replace(" ", "") + " " + str(link["value"]) + "\n"
        mono_runtime_call_graph_file.write(line)

    mono_data_dependency_graph = open("mono_data_dependency_graph.rsf", "x")
    for link in dependencies_json["mono_data_dependency_graph"]["links"]:
        line = link["source"].replace(" ", "") + " " + link["target"].replace(" ", "") + " " + str(link["value"]) + "\n"
        mono_data_dependency_graph.write(line)

    micro_detail_partition_by_business_logic = open("micro_detail_partition_by_business_logic.rsf", "x")
    for link in dependencies_json["micro_detail_partition_by_business_logic"]["links"]:
        line = link["source"].replace(" ", "") + " " + link["target"].replace(" ", "") + " " + str(link["value"]) + "\n"
        micro_detail_partition_by_business_logic.write(line)

    micro_detail_partition_by_natural_seam = open("micro_detail_partition_by_natural_seam.rsf", "x")
    for link in dependencies_json["micro_detail_partition_by_natural_seam"]["links"]:
        line = link["source"].replace(" ", "") + " " + link["target"].replace(" ", "") + " " + str(link["value"]) + "\n"
        micro_detail_partition_by_natural_seam.write(line)

if __name__ == "__main__":
    jsonFilename = sys.argv[1]
    convertJSONtoRSF(jsonFilename)
