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
    natRanks = []

    for theFile in fileList:
        with open(inPath + theFile, 'r') as f:
            lines = f.readlines()
            for i in range(1, len(lines)):
                line = lines[i]
                vals = line.split(',')
                if vals[0] == '0':
                    natRanks.append(i)
                    break
    print(theDir)
    print('mean: ', np.mean(natRanks))
    print('median: ', np.median(natRanks))

    outputDf = pd.DataFrame({'LR': natRanks})

    with open(outPath + 'nativeRanks.csv', 'w') as g:
        outputDf.to_csv(g)