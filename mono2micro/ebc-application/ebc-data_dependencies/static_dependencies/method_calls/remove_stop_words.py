"""
Removes stop words produced from the script SemanticParser.py when deriving the method call dependency graph.
ex. python remove_stop_words.py [input].csv [output].csv

"""

import csv
import sys

ebc_stop_words = ['com', 'ibm', 'elastic', 'build', 'cloud', 'api', 'core', 'external', 'system', 'bundle', 'feature', 'instance', 'ucd', 'jenkins', \
                  'logstash', 'openstack', 'rtc', 'resource', 'runtime', 'staticpool', 'unittest', 'util', 'web']

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
        first_class = line[0].split(".")
        second_class = line[1].split(".")
        first_name = None
        second_name = None
        # Change the message name
        if first_class[len(first_class)-1] == 'Messages':
            if 'external' in first_class:
                first_name = 'Messages[Duplicate_#001]'
            elif 'api' in first_class:
                first_name = 'Messages[Duplicate_#002]'
            elif 'jenkins' in first_class:
                first_name = 'Messages[Duplicate_#003]'
            elif 'rtc' in first_class:
                first_name = 'Messages[Duplicate_#004]'
            elif 'util' in first_class:
                first_name = 'Messages[Duplicate_#005]'
            elif 'instance' in first_class:
                first_name = 'Messages[Duplicate_#006]'
            elif 'core' in first_class:
                first_name = 'Messages[Duplicate_#007]'
            elif 'openstack' in first_class:
                first_name = 'Messages[Duplicate_#008]'

        if second_class[len(second_class)-1] == 'Messages':
            if 'external' in second_class:
                second_name = 'Messages[Duplicate_#001]'
            elif 'api' in second_class:
                second_name = 'Messages[Duplicate_#002]'
            elif 'jenkins' in second_class:
                second_name = 'Messages[Duplicate_#003]'
            elif 'rtc' in second_class:
                second_name = 'Messages[Duplicate_#004]'
            elif 'util' in second_class:
                second_name = 'Messages[Duplicate_#005]'
            elif 'instance' in second_class:
                second_name = 'Messages[Duplicate_#006]'
            elif 'core' in second_class:
                second_name = 'Messages[Duplicate_#007]'
            elif 'openstack' in second_class:
                second_name = 'Messages[Duplicate_#008]'

        if first_class[len(first_class)-1] in class_name_list and second_class[len(second_class)-1] in class_name_list:
            if first_name is None:
                first_name = first_class[len(first_class) - 1]
            if second_name is None:
                second_name = second_class[len(second_class) - 1]

        if first_name is not None and second_name is not None:
            new_list.append([first_name, second_name, line[2]])
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

