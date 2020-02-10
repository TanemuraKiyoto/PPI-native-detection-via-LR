# 9 September 2019

# Kiyoto Aramis Tanemura

# I modified the rfClassifier.py script to implement a logistic regression classifier. This classifier runs faster than the random forest classifier and Jun previously observed comparable results between logistic regression and random forest classifiers for the protein folding system. Due to the lesser time cost, I may sample a greater hyperparameter space using the logistic regression classifier. If the sampling yields a region in which overfitting is not observed, then I can refine the search. If the results are similar to that of the random forest classifier, then I may have exhausted the dataset for generalizability. 

# Modified 26 October 2019 by Kiyoto Aramis Tanemura. Apply logistic regression classifier to CASF-PPI dataset.

# Modified 18 November 2019 by Kiyoto Aramis Tanemura. Calculation for inclusion of near-native decoy comparison was taking long. I modify the code in the following ways.
# 1. Parallelize reading dataframes. This increases the CPU requirement but will substantially decrease time reservation
# 2. Omit five-fold cross validation. Performing CV on the training set upon inclusion of near-native decoy is undesirable since the ligand RMSD varies between systems. This will reduce the training to one model, not six.

import pandas as pd
import numpy as np
import os
import json
import pickle
from multiprocessing import Pool
from time import time
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from random import shuffle, random

os.chdir('/mnt/scratch/tanemur1/')

toc = time()

# Randomize input file orders
pathToInput = '/mnt/scratch/tanemur1/CASF-PPI/descriptors/nonb/'
pathToOutput = '/mnt/home/tanemur1/6May2019/2019-11-11/results/coefSubset/fiftyPercent/'
fileNames = [x for x in os.listdir(pathToInput) if '.csv' in x]
shuffle(fileNames) # note: shuffle is in-place. Do not assign to variable

# Specify training set fraction

train_fraction = 0.9

train_file_number = int(len(fileNames) * train_fraction + 0.5)

trainFiles = fileNames[:train_file_number]

x_train = pd.DataFrame()
y_train = pd.DataFrame()

# Read individual csv for comparison descriptors, append to train_data, and partition to x_train, y_train
fileNamesWithPath = [pathToInput + x for x in trainFiles]
#for i in subdirs[:RELAX + 1]:
#    fileNamesWithPath += [pathToInput + i + fileName for fileName in trainFiles]

# Debug 19 November 2019. The map function executed by workers is incompatible with the large size of the list of dataframes for certain jobs. I break the list into three regardless of length of list to circumvent the size limit.

coefFrac = 0.5
coefs = pd.read_csv('/mnt/home/tanemur1/6May2019/2019-11-11/results/medianCoefs.csv', index_col = 0, header = None, names = ['coefficients'])
coefs['absVal'] = np.abs(coefs['coefficients'])
coefs.sort_values(by = 'absVal', ascending = False, inplace = True)
coefs = coefs[:int(14028 * coefFrac + 0.5)]
keepList = list(coefs.index)
keepList.append('class')
del coefs

def read_csv(filePath):
    df = pd.read_csv(filePath, index_col = 0)
    df = df[keepList]
    return df

print('begin read training set')
with Pool(np.min([train_file_number, 28])) as p:
    train_dataList = list(p.map(read_csv, fileNamesWithPath))

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

# Define a random forest classifier, and parameters by which grid search CV is performed
clf = LogisticRegression(penalty='l2', verbose = 0, solver = 'lbfgs')

print('begin training | ' + str((time() - toc)/60) + ' mins')

clf.fit(x_train, y_train)

print('begin output | ',  (time() - toc) / 60 / 60, ' hours')

tic = time()

with open(pathToOutput + 'modelF.pkl', 'wb') as h:
    pickle.dump(clf, h)

with open(pathToOutput + 'trainingSetF.txt', 'w') as i:
    i.write('Training set:\n')
    for pdbID in trainFiles:
        i.write(pdbID + '\n')
    i.write('\nJob time: ' + str((tic - toc) / 60 / 60) + ' hours')

with open(pathToOutput + 'standardScalerF.pkl', 'wb') as j:
    pickle.dump(scaler, j)

bestCoefficient = clf.coef_
coefDf = pd.DataFrame(bestCoefficient, columns = feature_names)

with open(pathToOutput + 'coefficientsF.csv', 'w') as f:
    coefDf.to_csv(f)

