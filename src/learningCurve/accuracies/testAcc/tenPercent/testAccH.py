# 1 November 2019

# Kiyoto Aramis Tanemura

# Obtain test accuracies for learning curve.

import os
import pandas as pd
import numpy as np
import pickle
from time import time
from sklearn.metrics import accuracy_score
from multiprocessing import Pool

toc = time()

pathToModel = 'results/learningCurve/tenPercent/'
pathToOutput = 'results/learningCurve/tenPercent/testAcc/'
pathToComparisons = 'data/CASF-PPI-2017/comparison_descriptors/'

def getAccuracy(clf, scaler, testFile):
    test_set = pd.read_csv(testFile, index_col = 0)
    test_set = test_set.reindex(sorted(test_set.columns), axis = 1)
    test_x = test_set.drop('class', axis = 1)
    test_x = scaler.transform(test_x)
    test_y = test_set['class']
    pred = clf.predict(test_x)
    return float(accuracy_score(test_y, pred))

allFiles = os.listdir(pathToComparisons)

accuracyList = []

theLetter = 'H'

with open(pathToModel + 'model' + theLetter + '.pkl', 'rb') as f:
    clf = pickle.load(f)
with open(pathToModel + 'standardScaler' + theLetter + '.pkl', 'rb') as g:
    scaler = pickle.load(g)
with open(pathToModel + 'trainingSet' + theLetter + '.txt', 'r') as h:
    trainList = [x.strip() for x in h.readlines() if '.csv' in x]

testList = [x for x in allFiles if x not in trainList]

def exeGetAccuracy(testFile):
    return getAccuracy(clf, scaler, pathToComparisons + testFile)

with Pool(28) as pool:
    accuracyList = list(pool.map(exeGetAccuracy, testList))

#print(accuracyList)

with open(pathToOutput + theLetter + '_testAcc.txt', 'a') as h:
    h.writelines('mean accuracy:' + str(np.mean(accuracyList)) + '\n')
    h.writelines('cumulative time:' + str((time() - toc) / 60 / 60) + ' hours\n\n' )
