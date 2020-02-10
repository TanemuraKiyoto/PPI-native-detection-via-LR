# 25 September 2019

# Kiyoto Aramis Tanemura

# Obtain data from the ZDOCK rmsd files for calculating success rate (SR) and modified SR (Y) to compare across models.

import os
import json
import pandas as pd

#inputPath = '/mnt/home/tanemur1/6May2019/decoys_bm4_zd3.0.2_15deg/results/'
inputPath = 'results/coefSubset/evaluate/tenPercent/appendRMSD/'
outputPath = 'results/coefSubset/evaluate/tenPercent/'
fileList = os.listdir(inputPath) #[x for x in os.listdir(inputPath) if 'rmsd' in x]

rangeMax = [5, 10, 20, 30, 40, 50]

outputDf = pd.DataFrame()

for theMax in rangeMax:
    correlations = []
    for theFile in fileList:
        df = pd.read_csv(inputPath + theFile, index_col = 0)
        df['rank'] = range(len(df))
        correlations.append(df[df['RMSD'] <= theMax].corr('spearman').at['rank', 'RMSD'])
    rowDf = pd.DataFrame({'rho': correlations})
    rowDf['maxRMSD'] = theMax
    rowDf['SF'] = 'LR'
    outputDf = outputDf.append(rowDf, sort = True)

#print(outputList)
with open(outputPath + 'spearman.csv', 'w') as f:
    outputDf.to_csv(f)
