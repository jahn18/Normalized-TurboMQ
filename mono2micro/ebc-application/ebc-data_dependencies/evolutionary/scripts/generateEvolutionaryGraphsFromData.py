import numpy as np
import re
import sys
import json

Attributes = ['Contributors', 'Commits']

## produces a list of all classes changed by the commit history (keys)
## produces the a commit history dictionary (keys = classes changed, value = contributors & commits)
def sortCommitsByFile(): 
    print('Beginning to sort commits by file...')

    fileCommitTree = []
    commitList = []
    keys = []

    with open('cleanCommitHistory.csv', 'r') as ch:
       for line in ch:
           elements = line.splitlines()[0].split(',')
           commitList.append(elements)
           files = elements[2:]
           author = elements[1]
           commitID = elements[0]
           for f in files:
               keys.append(f)
       keys = list(dict.fromkeys(keys))
       fileCommitTree = dict.fromkeys(keys)

    Attributes = ['Contributors', 'Commits']

    for commit in commitList:
        author = commit[1]
        commitID = commit[0]
        for f in commit[2:]:
            if not fileCommitTree[f]:
                fileCommitTree[f] = dict.fromkeys(Attributes)
                for Attr in Attributes:
                    fileCommitTree[f][Attr] = []
            # append contributors and commits
            fileCommitTree[f]['Contributors'].append(author) 
            fileCommitTree[f]['Commits'].append(commitID)

    for key in keys:
        for Attr in fileCommitTree[key]:
            fileCommitTree[key][Attr] = list(set(fileCommitTree[key][Attr]))

    return keys, fileCommitTree

## produces full graph, commitGraph and contributorGraphs using the fileCommitTree
def generateGraphs (keys, fileCommitTree):
    print("Generating Graph...")

    headers = ['File A', 'File B', 'Contributor Weight', 'Commit Weight']
    graph = []
    commitGraph = []
    contributorGraph = []


    relCount = 0
    x = np.multiply(len(keys),(len(keys) - 1))
    totalRel = np.divide(x,2)
    percentUpdate = False

    print("Number of Relations: {0}".format(totalRel))

    for index, aKey in enumerate(keys):
        for bKey in keys[index+1:]:
           fileA = fileCommitTree[aKey] 
           fileB = fileCommitTree[bKey]

           weights = []

           # Intersection over Union
           # Calculate Contributor Weight
           for attr in Attributes:
               intersection = 0
               union = 0
               union_set = []
               for indexA, instA in enumerate(fileA[attr]):
                   for instB in fileB[attr]:
                       if instA == instB:
                           intersection = intersection + 1
                       union_set.append(instA)
                       union_set.append(instB)
               union = len(set(union_set))
               weight = np.divide(intersection,union)
               weights.append(str( weight ))
            
           cleanAKey = simplifyKeyUsingPackageName(aKey, packageName)
           # cleanAKey = aKey.replace('/', '.')
           # cleanAKey = cleanAKey.replace('.java', '');
           # nameStart = cleanAKey.find(packageName);
           # if nameStart != -1:
               # cleanAKey = cleanAKey[nameStart:]
            
           cleanBKey = simplifyKeyUsingPackageName(bKey, packageName)
           # cleanBKey = bKey.replace('/', '.')
           # cleanBKey = cleanBKey.replace('.java', '');
           # nameStart = cleanBKey.find(packageName);
           # if nameStart != -1:
               # cleanBKey = cleanBKey[nameStart:]
           
           contributorLine = []
           contributorLine.append(cleanAKey)
           contributorLine.append(cleanBKey)
           contributorLine.append(str(weights[0]))

           commitLine = []
           commitLine.append(cleanAKey)
           commitLine.append(cleanBKey)
           commitLine.append(str(weights[1]))

           line = []
           line.append(aKey)
           line.append(bKey)

           for weight in weights:
               line.append(str(weight))
                
           graph.append(line)
           commitGraph.append(commitLine)
           contributorGraph.append(contributorLine)

           relCount = relCount + 1
           percent = np.multiply(100,np.divide(relCount, totalRel))

           if (int(percent*100) % 10 == 0):
               if percentUpdate:
                   print(".", end = '')
                   if (int(percent*10) % 10 == 0):
                       print("{0:4.1f}%".format(percent))
               percentUpdate = False 
           else: percentUpdate = True

    return graph, commitGraph, contributorGraph

## simplifies a class file (key) using the package name
## TODO
def simplifyKeyUsingPackageName(key, packageName): 
    # cleanKey = key.replace('/', '.')
    # cleanKey = cleanKey.replace('.java', '')
    # nameStart = cleanKey.find(packageName)
    # if nameStart != -1:
        # cleanAKey = cleanKey[nameStart:]
    # return cleanKey
    return key

## writes graph, commitGraph and contributorGraph to file
def writeGraphsToFile(graph, commitGraph, contributorGraph):
    headers = ['File A', 'File B', 'Contributor Weight', 'Commit Weight']
    print("Writing graph to file...")

    print("evoGraph.csv")
    with open('evoGraph.csv','w') as uf:
        uf.write(','.join(headers) + '\n')
        for line in graph:
            uf.write((','.join(line) + '\n'))

    print(commitGraphFile)
    with open(commitGraphFile,'w') as uf:
        uf.write(','.join(headers) + '\n')
        for line in commitGraph:
            uf.write((','.join(line) + '\n'))

    print(contributorGraphFile)
    with open(contributorGraphFile,'w') as uf:
        uf.write(','.join(headers) + '\n')
        for line in contributorGraph:
            uf.write((','.join(line) + '\n'))

    print("Finished.")

## old implementation - this is all functions above compressed to one
## it uses regex to isolate files belonging to one package, we don't use that above anymore
def agenerateGraphs(javaFiles, commitGraphFile, contributorGraphFile, packageName):
    print('Beginning to sort commits by file...')

    fileCommitTree = []
    commitList = []
    keys = []

    with open('cleanCommitHistory.csv', 'r') as ch:
       for line in ch:
           elements = line.splitlines()[0].split(',')
           commitList.append(elements)
           files = elements[2:]
           author = elements[1]
           commitID = elements[0]
           for f in files:
               keys.append(f)
               #print("{0}: {1}, {2}".format(f,author,commit))
       keys = list(dict.fromkeys(keys))
       fileCommitTree = dict.fromkeys(keys)


    for commit in commitList:
        author = commit[1]
        commitID = commit[0]
        for f in commit[2:]:
            if not fileCommitTree[f]:
                fileCommitTree[f] = dict.fromkeys(Attributes)
                for Attr in Attributes:
                    fileCommitTree[f][Attr] = []
            # append contributors and commits
            fileCommitTree[f]['Contributors'].append(author) 
            fileCommitTree[f]['Commits'].append(commitID)

    for key in keys:
        
        for Attr in fileCommitTree[key]:
            fileCommitTree[key][Attr] = list(set(fileCommitTree[key][Attr]))

    mcdougle = []

    for key in keys:
        regex =  javaFiles + "/.*.java"
        dougle = re.match(r'' + regex,key,re.I|re.M)
        if dougle:
            dougle = dougle.string.splitlines()[0]
            print(dougle)
            mcdougle.append(dougle)

    keys = mcdougle
    # print (json.dumps(fileCommitTree, indent=2))
    # f = open("fileCommitTreeTest.txt", "w")
    # f.write(json.dumps(fileCommitTree, indent=2))
    # f.close()


    print("Generating Graph...")

    headers = ['File A', 'File B', 'Contributor Weight', 'Commit Weight']
    graph = []
    commitGraph = []
    contributorGraph = []


    relCount = 0
    x = np.multiply(len(keys),(len(keys) - 1))
    totalRel = np.divide(x,2)
    percentUpdate = False

    print("Number of Relations: {0}".format(totalRel))

    for index, aKey in enumerate(keys):
        for bKey in keys[index+1:]:
           fileA = fileCommitTree[aKey] 
           fileB = fileCommitTree[bKey]

           weights = []

           # Intersection over Union
           # Calculate Contributor Weight
           for attr in Attributes:
               intersection = 0
               union = 0
               union_set = []
               for indexA, instA in enumerate(fileA[attr]):
                   for instB in fileB[attr]:
                       if instA == instB:
                           intersection = intersection + 1
                       union_set.append(instA)
                       union_set.append(instB)
               union = len(set(union_set))
               weight = np.divide(intersection,union)
               weights.append(str( weight ))

           cleanAKey = aKey.replace('/', '.')
           cleanAKey = cleanAKey.replace('.java', '');
           nameStart = cleanAKey.find(packageName);
           if nameStart != -1:
               cleanAKey = cleanAKey[nameStart:]

           cleanBKey = bKey.replace('/', '.')
           cleanBKey = cleanBKey.replace('.java', '');
           nameStart = cleanBKey.find(packageName);
           if nameStart != -1:
               cleanBKey = cleanBKey[nameStart:]
            
           contributorLine = []
           contributorLine.append(cleanAKey)
           contributorLine.append(cleanBKey)
           contributorLine.append(str(weights[0]))

           commitLine = []
           commitLine.append(cleanAKey)
           commitLine.append(cleanBKey)
           commitLine.append(str(weights[1]))

           line = []
           line.append(aKey)
           line.append(bKey)

           for weight in weights:
               line.append(str(weight))
                
           graph.append(line)
           commitGraph.append(commitLine)
           contributorGraph.append(contributorLine)

           relCount = relCount + 1
           percent = np.multiply(100,np.divide(relCount, totalRel))

           if (int(percent*100) % 10 == 0):
               if percentUpdate:
                   print(".", end = '')
                   if (int(percent*10) % 10 == 0):
                       print("{0:4.1f}%".format(percent))
               percentUpdate = False 
           else: percentUpdate = True


    print("Writing graph to file...")

    with open('evoGraph.csv','w') as uf:
        uf.write(','.join(headers) + '\n')
        for line in graph:
            uf.write((','.join(line) + '\n'))

    print(commitGraphFile)
    with open(commitGraphFile,'w') as uf:
        uf.write(','.join(headers) + '\n')
        for line in commitGraph:
            uf.write((','.join(line) + '\n'))

    print(contributorGraphFile)
    with open(contributorGraphFile,'w') as uf:
        uf.write(','.join(headers) + '\n')
        for line in contributorGraph:
            uf.write((','.join(line) + '\n'))

    print("Finished.")

if __name__ == "__main__":
    # javaFiles = sys.argv[1] # output of function_logic_identify
    # commitGraphFile = sys.argv[2]
    # contributorGraphFile = sys.argv[3]
    # packageName = sys.argv[4]
    # javaFiles = 'C:\Users\Evelien Boerstra\Documents\GitHub\elastic-build-cloud'
    javaFiles = 'com.ibm.elastic.build.cloud.api/src/com/ibm/elastic/build/cloud/api'
    packageName = 'com.ibm.elastic.build.cloud.api'
    
    commitGraphFile = 'ebcCommitGraph.csv'
    contributorGraphFile = 'ebcContributorGraph.csv'
        
    # agenerateGraphs(javaFiles, commitGraphFile, contributorGraphFile, packageName)
    keys, fileCommitTree = sortCommitsByFile()
    graph, commitGraph, contributorGraph = generateGraphs(keys, fileCommitTree)
    writeGraphsToFile(graph, commitGraph, contributorGraph)


