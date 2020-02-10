# 9 November 2019

# Kiyoto Aramis Tanemura

# Obtain descriptive statistics for native ranks determined by LR classifier.

import os
import pandas as pd
import numpy as np

subdirs = ['fivePercent', 'tenPercent', 'twentyPercent', 'thirtyPercent', 'fortyPercent', 'fiftyPercent']

for theDir in subdirs:

    inPath = '/mnt/home/tanemur1/6May2019/2019-11-11/results/coefSubset/evaluate/' + theDir + '/appendRMSD/'
    outPath = '/mnt/home/tanemur1/6May2019/2019-11-11/results/coefSubset/evaluate/' + theDir + '/'

    fileList = os.listdir(inPath)
    firstRMSDlist = []

    for theFile in fileList:
#        print(inPath, theFile)
        with open(inPath + theFile, 'r') as f:
            firstRMSD = float(f.readlines()[1].split(',')[2])
        firstRMSDlist.append(firstRMSD)

    print('mean: ', np.mean(firstRMSDlist))
    print('median: ', np.median(firstRMSDlist))

    outputDf = pd.DataFrame({'LR': firstRMSDlist})

    with open(outPath + 'firstRMSD.csv', 'w') as g:
        outputDf.to_csv(g)
