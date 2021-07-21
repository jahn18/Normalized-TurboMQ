import sys
import csv

def getAllPartitionClasses(decompositionFile):
    decomposition_file = open(decompositionFile)
    csv_reader = csv.reader(decomposition_file)
    classNameHashTable = {}

    for row in csv_reader:
        row = row[0].split()
        classNameHashTable[row[2]] = row[1]
    return classNameHashTable

def runThroughDependencies(fileName, classNameHashTable):
     dynamic_dependencies_file = open(fileName)
     csv_reader = csv.reader(dynamic_dependencies_file)
     total_external_edges = 0
     total_internal_edges = 0

     list_of_dependencies = []

     for row in csv_reader:
         row = row[0].split()
         if {row[0], row[1]} in list_of_dependencies:
            continue
         if classNameHashTable[row[0]] == classNameHashTable[row[1]]:
             total_internal_edges += 1
         else:
             total_external_edges += 1
         list_of_dependencies.append({row[0], row[1]})

     return total_internal_edges, total_external_edges

def structuralMQ(fileName, classNameHashTable):
     dynamic_dependencies_file = open(fileName)
     csv_reader = csv.reader(dynamic_dependencies_file)

     SCOH = {'partition0': 0, 'partition1': 0, 'partition2' : 0, 'partition3' : 0, 'partition4': 0, 'Unobserved' : 0}
     #SCOH = {'partition0': 0, 'partition1': 0}
     num_of_classes = {'partition0': 0, 'partition1': 0, 'partition2' : 0, 'partition3' : 0, 'partition4': 0, 'Unobserved' : 0}
     #num_of_classes = {'partition0': 0, 'partition1': 0}
     #num_of_classes = {'partition0': 0, 'partition1': 0, 'Unobserved' : 0}
     SCOP = {}

     for key in classNameHashTable:
         num_of_classes[classNameHashTable[key]] += 1

     list_of_dependencies = []

     for row in csv_reader:
         row = row[0].split()
         if classNameHashTable[row[0]] == classNameHashTable[row[1]]:
            #if {row[0], row[1]} not in list_of_dependencies:
            SCOH[classNameHashTable[row[0]]] += 1
         else:
            combined_class = classNameHashTable[row[0]] + " " + classNameHashTable[row[1]]
            #if {row[0], row[1]} in list_of_dependencies:
            #    continue
            if combined_class in SCOP:
                SCOP[combined_class] += 1
            else:
                SCOP[combined_class] = 1
         list_of_dependencies.append({row[0], row[1]})

     total_scoh_value = 0
     for key in SCOH:
        total_scoh_value += (SCOH[key] / (num_of_classes[key]*num_of_classes[key]))

     total_scop_value = 0
     for key in SCOP:
         splitkey = key.split()
         total_scop_value += (SCOP[key] / (2*num_of_classes[splitkey[0]]*num_of_classes[splitkey[1]]))

     total_scoh_value = (total_scoh_value / (len(num_of_classes)-1))
     total_scop_value = ((2*total_scop_value) / ((len(num_of_classes)-1)*(len(num_of_classes)-2)))
     print(total_scoh_value - total_scop_value)

if __name__ == "__main__":
    decompositionFile = sys.argv[1]
    dependenciesFile = sys.argv[2]
    internal, external = runThroughDependencies(dependenciesFile, getAllPartitionClasses(decompositionFile))
    structuralMQ(dependenciesFile, getAllPartitionClasses(decompositionFile))
    #print("Internal Edges:")
    #print(internal)
    #print("External Edges:")
    #print(external)
