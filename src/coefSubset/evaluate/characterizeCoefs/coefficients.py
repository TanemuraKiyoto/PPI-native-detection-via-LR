# 13 November 2019

# Kiyoto Aramis Tanemura

# The magnitude of coefficients can be used to identify salient features in the descriptor set because all features were standardized when read to build the LR classifier. This script returns the summary statistics for the coefficients obtained in building LR classifiers on 0.99 of the dataset.

import pandas as pd
import numpy as np
import os

inPath = 'results/characterizeCoefs/'
outPath = inPath

fileList = [x for x in os.listdir(inPath) if 'coefficients' in x]

fullDf = pd.DataFrame()

for theFile in fileList:
	df = pd.read_csv(inPath + theFile, index_col = 0)
	df = df.transpose()
	df.columns = [theFile[12]]
	fullDf = pd.concat([fullDf, df], axis = 1, sort = False)

with open(outPath + 'coefSummary.csv', 'w') as f:
	fullDf.to_csv(f)
