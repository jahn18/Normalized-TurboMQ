"""
Removes stop words produced from the script SemanticParser.py when deriving the method call dependency graph.
ex. python remove_stop_words.py [input].csv [output].csv

"""

import csv
import sys

ebc_stop_words = ['com', 'ibm', 'elastic', 'build', 'cloud', 'api', 'core', 'external', 'system', 'bundle', 'feature', 'instance', 'ucd', 'jenkins', \
                  'logstash', 'openstack', 'rtc', 'resource', 'runtime', 'staticpool', 'unittest', 'util', 'web', 'java']

def removeStopWords(csvFileName, csvClassName):
    class_name_file = open(csvClassName)
    csv_reader = csv.reader(class_name_file)
    class_name_list = []
    for name in csv_reader:
        class_name_list.append(name[0])
    print(class_name_list)
    csv_file = open(csvFileName)
    csv_reader = csv.reader(csv_file, delimiter=',')
    new_list = []
    for line in csv_reader:
        first_class = None
        second_class = None
        dep = line[2]

        for f1 in line[0].split("."):
            for f2 in f1.split("/"):
                if f2 not in ebc_stop_words and f2 in class_name_list:
                    first_class = f2

        for f1 in line[1].split("."):
            for f2 in f1.split("/"):
                if f2 not in ebc_stop_words and f2 in class_name_list:
                    second_class = f2

        if first_class is not None and second_class is not None:
            row = [first_class, second_class, dep]
            new_list.append(row)
    return new_list

def writeCSV(reducedList, fileName):
     with open(fileName, "w") as f:
         writer = csv.writer(f)
         writer.writerows(reducedList)

if __name__ == "__main__":
    csvFileName = sys.argv[1]
    outputFileName = sys.argv[2]
    csvClassName = sys.argv[3]
    list_of_ebc_classes = removeStopWords(csvFileName, csvClassName)
    writeCSV(list_of_ebc_classes, outputFileName)
