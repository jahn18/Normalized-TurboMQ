"""
Converts a given csv file to an rsf file.
"""

import sys
import csv

def CSVtoRSF(csvFilename):
    rsfFileName = csvFilename.replace('.csv', '') + '.rsf'
    open(rsfFileName, 'w').write('\n'.join(map(' '.join, __import__('csv').reader(open(csvFilename)))))

if __name__ == "__main__":
    csvFilename = sys.argv[1]
    CSVtoRSF(csvFilename)
