import csv
import sys

def orderEdges(fileName):
    dynamic_dependencies_file = open(fileName)
    csv_reader = csv.reader(dynamic_dependencies_file)
    list_of_edges = []
    for row in csv_reader:
        list_of_edges.append(row[0].split())
    sortedList = insertionSort(list_of_edges)
    return sortedList

def writeCSV(sortedList, fileName):
    with open(fileName, "w") as f:
          writer = csv.writer(f)
          writer.writerows(sortedList)

def insertionSort(list_of_values):
    for i in range(len(list_of_values)):
        j = findMin(i, list_of_values)
        list_of_values[i], list_of_values[j] = list_of_values[j], list_of_values[i]
    return list_of_values

def findMin(i, list_of_values):
    smallest_value = int(list_of_values[i][2])
    index = i
    for j in range(i, len(list_of_values)):
        if int(list_of_values[j][2]) < smallest_value:
            index = j
            smallest_value = int(list_of_values[j][2])
    return index

if __name__ == "__main__":
    fileName = sys.argv[1]
    sortedList = orderEdges(fileName)
    writeCSV(sortedList, 'sorted_edges.csv')
