import sys
import csv
import math
import re


'''
compute the class-class semantic value baed on the short class name (without the package name)
only compute single direction:  c1-c2.  c2-c1 is not computed
'''

# stop words for the ebc application
Java_stop_words=[
        'Provider', 'Helper', 'Resource', '', 'controller', 'model', 'mongo', 'initializer', 'exception',
        'abstract', 'interface', 'mapper', 'service', 'bean', 'action',
        'type',
]


# split by hump
def splitByHump(name):
    resList = list()
    upperIndexList = list()
    upperIndexList.append(0) #first index
    for index in range(0, len(name)):
        if name[index].isupper():
            upperIndexList.append(index)
    upperIndexList.append(len(name)) #last index + 1

    for i in range(0, len(upperIndexList) - 1):
        index_s = upperIndexList[i]
        index_e = upperIndexList[i + 1]
        strstr = name[index_s: index_e]
        resList.append(strstr)

    resList = [each.lower() for each in resList]
    return resList



#filter by 's/d' or 'ing ' or 'number' endsup
def removeNumFushu(word):
    if word.endswith('s') and word.endswith('es') == False:
        word = word[0: len(word) - 1]

    elif len(word) > 2 and (word.endswith('ed') or word.endswith('es')):
        word = word[0: len(word) - 2]
        if len(word) > 2 and word[len(word) -1 ] == word[len(word) - 2]:
            word = word[0: len(word) - 1]

    elif word.endswith('ing'):
        word = word[0: len(word) - 3]
        if len(word) > 2 and word[len(word) -1 ] == word[len(word) - 2]:
            word = word[0: len(word) - 1]

    if re.search(r'[0-9]+', word):
        #print word
        m = re.search(r'[0-9]+', word)  #search any-pos substring,  match from start
        #print 'match:', m.group() #match's str
        (start, end) = m.span() #match pos
        if start < end:
            word = ( word[0: start] + word[start + 1: end] + word[end + 1 : len(word)] )
        elif start == end:
            word = ( word[0: start] + word[start + 1: len(word)] )
        #print word
    return word

def isAllBigLetter(word):
    if re.match(r'[A-Z_0-9]+', word):  #all big letter
        m = re.match(r'[A-Z_0-9]+', word)
        if len(m.group()) == len(word):
            return True
    return False


def processIdentifierFile(fileName):
    classwordDict = dict() #[classname] = [w1,w2]
    import nltk
    nltk.download('stopwords')
    stopWords = nltk.corpus.stopwords.words('english')
    stopWords.extend(Java_stop_words)

    with open (fileName, 'r') as fp:
        reader = csv.reader(fp)
        for each in reader: #eachline corresponds to a class
            longclassname = each[0]
            tmpList = longclassname.split('.')
            className = tmpList[len(tmpList) - 1]
            if className == 'T':
                continue

            #if words are all captain letter
            if isAllBigLetter(className):
                className = className.lower()
            #split by  _
            wordList = list()
            tmpList = re.split( r'[._\[\]]', className)
            wordList.extend(tmpList)
            #split by hump
            newWordList = list()
            for word in wordList:
                tmpList = splitByHump(word)
                newWordList.extend(tmpList)
            #filter
            wordList = list()
            for word in newWordList:
                word = removeNumFushu(word) #filter by 's' or 'number' endsup
                if (word != '') and (len(word) > 1) and (word not in stopWords):
                    wordList.append(word)
            classwordDict[longclassname] = wordList
            print(longclassname, wordList)
    return classwordDict


def writeCSV(listList, fileName):
    with open(fileName, 'w') as fp:
        writer = csv.writer(fp)
        writer.writerows(listList)
    print (fileName)

def computedep(classwordDict):
    classdepdict = dict() #[class1][class2] = dep
    classList = list(classwordDict.keys())
    for id1 in range(0, len(classList) - 1):
        className1 = classList[id1]
        set1 = set(classwordDict[className1])
        if className1 not in classdepdict:
            classdepdict[className1] = dict()

        for id2 in range(id1 + 1, len(classList)):
            className2 = classList[id2]
            set2 = set(classwordDict[className2])
            if len(set1 | set2) == 0:
                jaccard = 0
            else:
                jaccard = (len(set1 & set2)) / float(len(set1 | set2))
            classdepdict[className1][className2] = jaccard
            #print(className1, className2, set1, set2, jaccard)

    return classdepdict

#python pro.py  jpetstore6_classlist.txt  classsemantic_dep.csv
if __name__ == '__main__':
    classfilenane = sys.argv[1]
    classsemanticdepfilename = sys.argv[2]
    classwordDict = processIdentifierFile(classfilenane)
    classdepdict = computedep(classwordDict)

    alist = list()
    for className1 in classdepdict:
        for className2 in  classdepdict[className1]:
            dep = classdepdict[className1][className2]
            alist.append([className1, className2, dep])

    writeCSV(alist, classsemanticdepfilename)
