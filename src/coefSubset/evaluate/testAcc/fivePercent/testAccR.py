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

#os.chdir('/mnt/home/tanemur1/6May2019/17Jun2019/')
os.chdir('/mnt/scratch/tanemur1/')

# Paths modified for testing purposes
pathToWorking = '/mnt/home/tanemur1/6May2019/2019-11-11/'
pathToModel = 'results/coefSubset/fivePercent/'
pathToOutput = 'results/coefSubset/evaluate/fivePercent/testAcc/'
pathToComparisons = '/mnt/scratch/tanemur1/CASF-PPI/descriptors/nonb/'

coefFrac = 0.05
coefs = pd.read_csv('/mnt/home/tanemur1/6May2019/2019-11-11/results/medianCoefs.csv', index_col = 0, header = None, names = ['coefficients'])
coefs['absVal'] = np.abs(coefs['coefficients'])
coefs.sort_values(by = 'absVal', ascending = False, inplace = True)
coefs = coefs[:int(14028 * coefFrac + 0.5)]
keepList = list(coefs.index)
keepList.append('class')
del coefs

def getAccuracy(clf, scaler, testFile):
    test_set = pd.read_csv(testFile, index_col = 0)
    test_set = test_set[keepList]
    test_set = test_set.reindex(sorted(test_set.columns), axis = 1)
    test_x = test_set.drop('class', axis = 1)
    test_x = scaler.transform(test_x)
    test_y = test_set['class']
    pred = clf.predict(test_x)
    return float(accuracy_score(test_y, pred))

allFiles = os.listdir(pathToComparisons)

accuracyList = []

theLetter = 'R'

with open(pathToWorking + pathToModel + 'model' + theLetter + '.pkl', 'rb') as f:
    clf = pickle.load(f)
with open(pathToWorking + pathToModel + 'standardScaler' + theLetter + '.pkl', 'rb') as g:
    scaler = pickle.load(g)
with open(pathToWorking + pathToModel + 'trainingSet' + theLetter + '.txt', 'r') as h:
    trainList = [x.strip() for x in h.readlines() if '.csv' in x]

testList = [x for x in allFiles if x not in trainList]

def exeGetAccuracy(testFile):
    return getAccuracy(clf, scaler, pathToComparisons + testFile)

with Pool(28) as pool:
    accuracyList = list(pool.map(exeGetAccuracy, testList))

print(accuracyList)

with open(pathToWorking + pathToOutput + theLetter + 'performance.txt', 'w') as h:
    h.writelines('mean accuracy:' + str(np.mean(accuracyList)) + '\n')
    h.writelines('cumulative time:' + str((time() - toc) / 60 / 60) + ' hours\n\n' )
