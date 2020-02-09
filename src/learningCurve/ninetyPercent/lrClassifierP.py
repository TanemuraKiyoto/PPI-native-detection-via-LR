# 9 September 2019

# Kiyoto Aramis Tanemura

# I modified the rfClassifier.py script to implement a logistic regression classifier. This classifier runs faster than the random forest classifier and Jun previously observed comparable results between logistic regression and random forest classifiers for the protein folding system. Due to the lesser time cost, I may sample a greater hyperparameter space using the logistic regression classifier. If the sampling yields a region in which overfitting is not observed, then I can refine the search. If the results are similar to that of the random forest classifier, then I may have exhausted the dataset for generalizability. 

# Modified 26 October 2019 by Kiyoto Aramis Tanemura. Apply logistic regression classifier to CASF-PPI dataset.

# Modified 2020-02-09 by KAT. Code generalized for public use on GitHub.

import pandas as pd
import numpy as np
import os
import json
import pickle
#from multiprocessing import Pool
from time import time
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from random import shuffle, random

#os.chdir('/mnt/scratch/tanemur1/')

toc = time()

# Randomize input file orders
pathToInput = 'data/comparison_descriptors/'
pathToOutput = 'results/learningCurve/'
fileNames = [x for x in os.listdir(pathToInput) if '.csv' in x]
shuffle(fileNames) # note: shuffle is in-place. Do not assign to variable

# Specify training set fraction

train_fraction = 0.9

if len(fileNames) * train_fraction == int(len(fileNames) * train_fraction):
    train_file_number = int(len(fileNames) * train_fraction)
else:
    train_file_number = int(len(fileNames) * train_fraction + 1)

x_train = pd.DataFrame()
y_train = pd.DataFrame()

# Read individual csv for comparison descriptors, append to train_data, and partition to x_train, y_train

fileNamesWithPath = [pathToInput + fileName for fileName in fileNames]

def read_csv(filePath):
    return pd.read_csv(filePath, index_col = 0)

print('begin read training set')
#with Pool(np.min([train_file_number, 28])) as p:
#    train_dataList = list(p.map(read_csv, fileNamesWithPath[:train_file_number]))

train_dataList = list(map(read_csv, fileNamesWithPath[:train_file_number]))

print('begin append DF | ', (time() - toc) / 60, ' min')

# Append DataFrames into one. While loop used to reduce append operations. Iteratively, DFs in a list are appended
# to the following DF.

while len(train_dataList) != 1:
    number = int(len(train_dataList) / 2)
    for i in range(number):
        train_dataList[2 * i] = train_dataList[2 * i].append(train_dataList[2 * i + 1], sort = True)
    for j in range(number):
        del train_dataList[j + 1]
x_train = train_dataList[0]
del train_dataList

print('train_data dimensions', x_train.shape, ' | ',  (time() - toc) / 60, ' min')

y_train = x_train['class']
x_train = x_train.drop('class', axis = 1) # x_train contains only nonbonding descriptors
feature_names = x_train.columns

scaler = StandardScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
y_train = y_train.values

print('Dimensions x_train ', x_train.shape, ' | y_train', y_train.shape)

# Define a logistic regression classifier along with pertinent hyperparameters. Here, default values are used.
clf = LogisticRegression(penalty='l2', verbose = 1)

def sampleRationalVals(minVal, maxVal):
    return 2 ** (random() * (np.log2(maxVal) - np.log2(minVal)) + np.log2(minVal))

def sampleRationalList(minVal, maxVal):
    theList = []
    for i in range(int(2 * np.log2(maxVal - minVal) + 1)):
        theVal = sampleRationalVals(minVal, maxVal)
        theList.append(theVal)
    return theList

parameters = {
#    include any hyperparameters to sample. Otherwise, leave empty to perform five fold cross validation with default values. For example:
#    'C': sampleRationalList(0.001, 1000),
#    'solver': ['newton-cg', 'lbfgs', 'sag','saga']
}

print('begin RandomizedSearchCV | ' + str((time() - toc)/60) + ' mins')

randomized_search = RandomizedSearchCV(estimator = clf, param_distributions = parameters, n_iter = 1, scoring = 'accuracy', refit = True, cv = 5, verbose = 1, n_jobs = 1, pre_dispatch = 'n_jobs', return_train_score=True)
randomized_search.fit(x_train, y_train)

print('begin output | ',  (time() - toc) / 60 / 60, ' hours')

tic = time()

with open(pathToOutput + 'bestParamP.json', 'w') as g:
    json.dump(randomized_search.best_estimator_.get_params(), g)

with open(pathToOutput + 'modelP.pkl', 'wb') as h:
    pickle.dump(randomized_search, h)

with open(pathToOutput + 'trainingSetP.txt', 'w') as i:
    i.write('Training set:\n')
    for pdbID in fileNames[:train_file_number]:
        i.write(pdbID + '\n')
    i.write('\nJob time: ' + str((tic - toc) / 60 / 60) + ' hours')

with open(pathToOutput + 'standardScalerP.pkl', 'wb') as j:
    pickle.dump(scaler, j)

bestCoefficient = randomized_search.best_estimator_.coef_
coefDf = pd.DataFrame(bestCoefficient, columns = feature_names)

with open(pathToOutput + 'coefficientsP.csv', 'w') as f:
    coefDf.to_csv(f)
