import csv
import sys

"""
You can use this by running python classClassDepM2M.py [file_name]_class_depedencies.csv [filename]_testcase_class.csv
"""


def readCSV(fileName):
    reducedTraceList = []
    with open(fileName, newline='') as f:
        reader = csv.reader(f)
        for trace in reader:
            reducedTraceList.append(trace)
    return reducedTraceList

def readRSF(fileName):
    depList = []
    with open(fileName) as f:
        for n in f:
            depList.append(n.split())
    return depList

# Finds all the unique class names and stores them as keys, the values are just empty dictionaries.
def buildDictionary(className):
    class_dict = {}
    for name in className:
        if name[0] not in class_dict:
            class_dict[name[0]] = {}
    return class_dict

def computeClassDependencies(reducedTraceList, classDepDict):
    for trace in reducedTraceList:
        calling_class = trace[0]
        called_class = trace[1]
        if called_class in classDepDict[calling_class]:
            classDepDict[calling_class][called_class] += trace[2]
        else:
            classDepDict[calling_class][called_class] = trace[2]

def writeCSV(classDepDict, fileName):
    with open(fileName, "w") as f:
        writer = csv.writer(f)
        for main_key in classDepDict:
            for sub_key in classDepDict[main_key]:
                writer.writerow([main_key, sub_key, classDepDict[main_key][sub_key]])

if __name__ == "__main__":
    method_calls = sys.argv[1]
    inheritance = sys.argv[2]
    data_dependency = sys.argv[3]
    class_names = sys.argv[4]
    import pdb
    mc = readCSV(method_calls)
    i = readRSF(inheritance)
    d = readRSF(data_dependency)
    cn = readCSV(class_names)

    class_dict = buildDictionary(cn)

    computeClassDependencies(mc, class_dict)
    computeClassDependencies(i, class_dict)
    computeClassDependencies(d, class_dict)

    writeCSV(class_dict, 'static_dependencies_graph.csv')
