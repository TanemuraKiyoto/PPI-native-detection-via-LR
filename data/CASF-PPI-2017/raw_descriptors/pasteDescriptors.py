# 21 October 2019

# Kiyoto Aramis Tanemura

# Combine partial descriptors together in one csv for each PPI system.

import os
import pandas as pd

thePDB = '1ay7'

inputPath = 'data/CASF-PPI-2017/raw_descriptors/partial1ay7/'
outPath = 'data/CASF-PPI-2017/raw_descriptors/'
partialFileList = os.listdir(inputPath)
if len(partialFileList) < 21:
    print(thePDB + ' incomplete descriptors')
    quit()
finalDf = pd.read_csv(inputPath + partialFileList[0])
for i in range(1, len(partialFileList)):
    finalDf = pd.merge(finalDf, pd.read_csv(inputPath+ partialFileList[i]))
with open(outPath + thePDB + '.csv', 'w') as f:
    finalDf.to_csv(f)
