import csv
import sys
import json


def retrieveDepDictFromFile(useCasesFilename):
    depDict = dict()
    with open(useCasesFilename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            className1 = row[0]
            className2 = row[1]
            dep = row[2]

            if className1 not in depDict:
                depDict[className1] = dict()
            depDict[className1][className2] = dep

            if className2 not in depDict:
                depDict[className2] = dict()
            depDict[className2][className1] = dep

    return depDict

def createPartitionDict(jsonFileName):
    json_file = open(jsonFileName)
    dependencies_json = json.load(json_file)
    nodes = dependencies_json['micro_detail_partition_by_business_logic']['nodes']

    partitionDict = dict()

    for node in nodes:
        className = node["name"]
        partition = node["category"]

        if partition not in partitionDict:
            partitionDict[partition] = [className]
        else:
            partitionDict[partition].append(className)

    return partitionDict
        
    
def calcAverageForPartition(partition, classes, depDict):
    partitiondep = []
    # print(partition)

    for id1 in range(0, len(classes)-1):
        className1 = classes[id1]
        for id2 in range(id1+1, len(classes)):
            className2 = classes[id2]

            dep = float(depDict[className1][className2])
            partitiondep.append(dep)
            # print(className1, className2, dep)
    

    return sum(partitiondep)/len(partitiondep)

def writeCSV(listList, fileName):
    with open(fileName, 'w') as fp:
        writer = csv.writer(fp)
        writer.writerows(listList)
    print (fileName)


# python calculateBusinessUseCaseSimilarityPerPartition.py businessUseCaseSimilarityGraph.csv final_graph.json
if __name__ == "__main__":
    useCasesFilename = sys.argv[1]
    print(useCasesFilename)
    jsonFileName = sys.argv[2]
    print(jsonFileName)
    
    depDict = retrieveDepDictFromFile(useCasesFilename)

    partitionDict = createPartitionDict(jsonFileName)

    partitionAvgDepDict = dict()
    for partition in partitionDict.keys():
        avgdep = calcAverageForPartition(partition, partitionDict[partition], depDict)
        partitionAvgDepDict[partition] = avgdep
    
    print(partitionAvgDepDict)

    alist = []
    for partition in partitionAvgDepDict:
        avg = partitionAvgDepDict[partition]
        alist.append([partition, avg])

    writeCSV(alist, 'avgBusinessUseCaseSimilarityPerPartition.csv')
    

    

