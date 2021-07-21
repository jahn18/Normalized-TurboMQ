import sys
import csv

def readCSV(csvFilename):
    listTable = []
    indexFile = open(csvFilename)
    csv_reader = csv.reader(indexFile)
    for row in csv_reader:
        listTable.append(row[1])
    indexFile.close()
    return listTable

def convertIndexToClassName(csvDependencyFile, listTable, graph_name):
    print(listTable)
    file_name = graph_name
    new_csv_file = open(file_name, 'w')
    writer = csv.writer(new_csv_file)

    dependencyGraph = open(csvDependencyFile)
    csv_reader = csv.reader(dependencyGraph)
    for row in csv_reader:
        check = True
        if row[0] not in listTable or row[1] not in listTable:
            check = False

        if check is True:
            writer.writerow(row)

    new_csv_file.close()

if __name__ == '__main__':
    csv_file_index = sys.argv[1]
    graph = sys.argv[2]
    graph_name = sys.argv[3]
    convertIndexToClassName(graph, readCSV(csv_file_index), graph_name)

