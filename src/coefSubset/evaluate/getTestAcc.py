# 18 November 2019

# Kiyoto Aramis Tanemura

# Summarize test accuracy data in one csv file. 

import os
import pandas as pd

subdirs = ['fivePercent', 'tenPercent', 'twentyPercent', 'thirtyPercent', 'fortyPercent', 'fiftyPercent']
fracVals = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5]

testAcc = []
frac = []

outputDf = pd.DataFrame()

for i in range(len(subdirs)):
    inPath = 'results/coefSubset/evaluate/' + subdirs[i] + '/testAcc/'
    fileList = os.listdir(inPath)
    for theFile in fileList:
        with open(inPath + theFile, 'r') as f:
            accuracy = f.readlines()[0].split(':')[1]
            accuracy = float(accuracy)
        testAcc.append(accuracy)
        frac.append(fracVals[i])
#        cond.append(theDir)

outputDf = pd.DataFrame({'test_accuracy': testAcc, 'fraction': frac})

print(outputDf)

with open('results/coefSubset/evaluate/testAcc.csv', 'w') as g:
    outputDf.to_csv(g)
