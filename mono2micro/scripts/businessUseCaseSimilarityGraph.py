import json
import sys
import csv
import re


def computedep(classDict):
    depDict = dict()
    classList = list(classDict.keys())

    for id1 in range(0, len(classList) -1):
        className1 = classList[id1]
        set1 = set(classDict[className1])

        if className1 not in depDict:
            depDict[className1] = dict()

        for id2 in range (id1+1, len(classList)):
            className2 = classList[id2]
            set2 = set(classDict[className2])

            if len(set1 | set2) == 0:
                jaccard = 0
            else:
                jaccard = (len(set1 & set2)) / float(len(set1 | set2))
            depDict[className1][className2] = jaccard
            print(className1, className2, set1, set2, jaccard)
    return depDict



def extractBusinessUseCaseSimilarityGraph(jsonFilename):
    json_file = open(jsonFilename)
    dependencies_json = json.load(json_file)
    nodes = dependencies_json['mono_run_time_call_graph']['nodes']

    classDict = {}

    for node in nodes:
        classDict[node["name"]] = node["semantics"]

    return computedep(classDict)


def writeCSV(listList, fileName):
    with open(fileName, 'w') as fp:
        writer = csv.writer(fp)
        writer.writerows(listList)
    print (fileName)


# python businessUseCaseGraph.py final_graph.json
if __name__ == "__main__":
    jsonFilename = sys.argv[1]
    depDict = extractBusinessUseCaseSimilarityGraph(jsonFilename)

    print(depDict)

    alist = list()
    for className1 in depDict:
        for className2 in  depDict[className1]:
            dep = depDict[className1][className2]
            alist.append([className1, className2, dep])

    writeCSV(alist, 'businessUseCaseSimilarityGraph.csv')
