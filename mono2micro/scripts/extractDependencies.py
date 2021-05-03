"""
Converts the dependencies found in the mono2micro JSON final_graph into an RSF dependency file.
ex.) python extractDependencies.py final_graph.json

"""

import json
import sys

def extractDependencies(jsonFilename):
    json_file =  open(jsonFilename,)
    dependencies_json = json.load(json_file)

    # Dynamic dependencies
    mono_runtime_call_graph_file = open("mono_run_time_call_graph.rsf", "x")
    for link in dependencies_json["mono_run_time_call_graph"]["links"]:
        total_trace_sum = 0
        for method in link["method"]:
            total_trace_sum += link["method"][method]
        line = link["source"].replace(" ", "") + " " + link["target"].replace(" ", "") + " " + str(total_trace_sum) + "\n"
        mono_runtime_call_graph_file.write(line)

    # Static dependency
    mono_data_dependency_graph = open("mono_data_dependency_graph.rsf", "x")
    for link in dependencies_json["mono_data_dependency_graph"]["links"]:
        line = link["source"].replace(" ", "") + " " + link["target"].replace(" ", "") + " " + str(link["value"]) + "\n"
        mono_data_dependency_graph.write(line)

if __name__ == "__main__":
    jsonFilename = sys.argv[1]
    extractDependencies(jsonFilename)
