"""
Converts the partition.txt file produced by mono2micro into an RSF file.

"""

import sys

def readPartitions(file_name):
     clusters = []
     for line in open(file_name, 'r'):
         line = line.rstrip("\n")
         cluster_line = line.split(",")
         clusters.append((cluster_line[1], cluster_line[0]))
     return clusters

def writePartitionstoRSF(file_name, clusters):
     rsfFilename = file_name.replace('.txt', '') + '.rsf'
     rsf_file = open(rsfFilename, "x")
     for c in clusters:
         line = "contain" + " " + c[0].replace(" ", "") + " " + c[1].replace(" ", "") + "\n"
         rsf_file.write(line)

if __name__ == "__main__":
     filename = sys.argv[1]
     clusters = readPartitions(filename)
     writePartitionstoRSF(filename, clusters)
