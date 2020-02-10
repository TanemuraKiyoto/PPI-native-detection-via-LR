# 25 September 2019

# Kiyoto Aramis Tanemura

# Script to consolidate results calculated for individual protein-protein complexes.

import os
import pandas as pd
import numpy as np
from multiprocessing import Pool

thresholds = ['0', '1', '5', '10']

def readData(fileName):
    return pd.read_csv(inputPath + fileName)

#for theSF in score_functions:

subdirs = ['fivePercent', 'tenPercent', 'twentyPercent', 'thirtyPercent', 'fortyPercent', 'fiftyPercent']

for theDir in subdirs:
    inputPath = '/mnt/home/tanemur1/6May2019/2019-11-11/results/coefSubset/evaluate/' + theDir + '/individualSR/'
    outputPath = '/mnt/home/tanemur1/6May2019/2019-11-11/results/coefSubset/evaluate/' + theDir + '/'
    for thres in thresholds:
        fileList = [x for x in os.listdir(inputPath) if x[5:-4] == thres]

        with Pool() as p:
            dfList = list(p.map(readData, fileList))

        SR = []
        meanK = []
        Y = []

        for i in range(2001):
            SRList = []
            KList = []
            YList = []
            for theDf in dfList:
                if i >= theDf.shape[0]:
                    continue
                SRList.append(theDf.at[i, 'SRi'])
                KList.append(theDf.at[i, 'K'])
                YList.append(theDf.at[i, 'F'])
            SR.append(np.mean(SRList))
            meanK.append(np.mean(KList))
            Y.append(np.mean(YList))

        myData = {'N': range(1, 2002),
                  'SR': SR,
                  'K': meanK,
                  'Y': Y
        }

        with open(outputPath + 'SR' + thres + '.csv', 'w') as f:
            pd.DataFrame(myData).to_csv(f)
