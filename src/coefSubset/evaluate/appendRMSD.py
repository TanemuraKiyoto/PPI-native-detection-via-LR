# 26 September 2019

# Kiyoto Aramis Tanemura

# The RF model is evaluated against other scoring functions via means of success rate (SR), modified success rate (Y), and recall. I will append RMSD values for the complexes ranked using the RF model so that I can compare against the ZDOCK score, as well as other scoring functions using these metrics. 

# Modified 20 October 2019 by KAT. Appropriate code for CASF-PPI-2017. (DOI: 10.4155/fmc-2017-0261)

import os
import pandas as pd

# First, construct a dictionary to contain the i-RMSD files for quick reference to these values. i-RMSD values are contained in the CASF-PPI-2017/Power_docking/ directory.

rmsdFilePath = '/mnt/home/tanemur1/6May2019/13Oct2019/CASF-PPI-2017/Power_docking/rmsd/'
rawScorePath = '/mnt/home/tanemur1/6May2019/2019-11-11/results/coefSubset/evaluate/'

rmsdSummary = {}
rmsdFileList = [x for x in os.listdir(rmsdFilePath) if 'rmsd' in x]

for theRMSDfile in rmsdFileList:
    rmsdSummary[theRMSDfile[:4]] = {}
    with open(rmsdFilePath + theRMSDfile, 'r') as f:
        for theLine in f.readlines():
            values = theLine.split()
            if values[0] == 'crystal':
                theID = 0
            else:
                theID = int(values[0])
            rmsdSummary[theRMSDfile[:4]][theID] = float(values[1])

subdirs = ['fivePercent', 'tenPercent', 'twentyPercent', 'thirtyPercent', 'fortyPercent', 'fiftyPercent']
for theDir in subdirs:
    inPath = '/mnt/home/tanemur1/6May2019/2019-11-11/results/coefSubset/evaluate/' + theDir + '/ranks/'
    outputPath = '/mnt/home/tanemur1/6May2019/2019-11-11/results/coefSubset/evaluate/' + theDir + '/appendRMSD/'
    fileList = os.listdir(inPath)
    os.system('mkdir ' + outputPath)
    for theFile in fileList:
        thePDB = theFile[:4]
        score = []
        indices = []
        with open(inPath + theFile, 'r') as g:
            for theLine in g.readlines()[1:]:
                vals = theLine.split(',')
                if vals[0] == 'native':
                    theID = 0
                else:
                    theID = int(vals[0][8:12])
                score.append(int(vals[1]))
                indices.append(theID)
        df = pd.DataFrame({'score': score}, index = indices)
        df['RMSD'] = -1.0
        for theIndex in df.index:
            df.at[theIndex, 'RMSD'] = rmsdSummary[thePDB][theIndex]
        df.sort_values(by = 'score', axis = 0, ascending = False, inplace = True)
        with open(outputPath + theFile[:-4] + '.csv', 'w') as h:
            df.to_csv(h)
