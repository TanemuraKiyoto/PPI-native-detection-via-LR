# 26 October 2019

# Kiyoto Aramis Tanemura

# Retrieve results from first round of LR classifier building.

import os
import pickle
import pandas as pd

inPath = 'results/LR/learningCurve/'
outPath = inPath

dirList = [x for x in os.listdir(inPath) if os.path.isdir(inPath + x)]

outputDf = pd.DataFrame()

fracVals = {'tenPercent': 0.1, 'twentyPercent': 0.2, 'thirtyPercent': 0.3, 'fortyPercent': 0.4, 'fiftyPercent': 0.5, 'sixtyPercent': 0.6, 'seventyPercent': 0.7, 'eightyPercent': 0.8, 'ninetyPercent': 0.9, 'leaveOneOut':0.99}

for theDir in dirList:
    modelList = [x for x in os.listdir(inPath + theDir) if x[:5] == 'model']
    for theModel in modelList:
        with open(inPath + theDir + '/' + theModel, 'rb') as f:
            clf = pickle.load(f)
        rowData = pd.DataFrame(clf.cv_results_['params'], index = [theModel[5]])
        rowData['mean_train_score'] = clf.cv_results_['mean_train_score']
        rowData['std_train_score'] = clf.cv_results_['std_train_score']
        rowData['mean_dev_score'] = clf.cv_results_['mean_test_score']
        rowData['std_dev_score'] = clf.cv_results_['std_test_score']
        rowData['fraction'] = fracVals[theDir]
        outputDf = outputDf.append(rowData)

outputDf.sort_values(by = 'mean_dev_score', ascending = False, inplace = True)
outputDf.sort_values(by = 'fraction', ascending = True, inplace = True)

print(outputDf)
with open(outPath + 'trainValAcc.csv', 'w') as g:
    outputDf.to_csv(g)
