# 9 July 2019

# Kiyoto Aramis Tanemura

# Several metrics are used to assess the performance of the trained RF model, notably native ranking. This script returns a ranking of the native protein-protein complex among a decoy set. For convenience, I will define as a function and will call in a general performance assessment script.

# Modified 11 July 2019 by Kiyoto Aramis Tanemura. To parallelize the process, I will replace the for loop for the testFileList to a multiprocessing pool. 

# Modified 9 September 2019 by Kiyoto Aramis Tanemura. I will use the function to perform the calculation on one CSV file only. Thus instead of a function to import in other scripts, they will be individual jobs parallelized as individual jobs in the queue. 

import os
import pandas as pd
import numpy as np
import pickle

os.chdir('/mnt/scratch/tanemur1/')

# Read the model and trainFile

testFile = '3kr3.csv'
identifier = 'D'
coefFrac = 0.4

testFilePath = '/mnt/scratch/tanemur1/CASF-PPI/nonb_descriptors/complete/'
modelPath = '/mnt/home/tanemur1/6May2019/2019-11-11/results/coefSubset/fortyPercent/'
outputPath = '/mnt/home/tanemur1/6May2019/2019-11-11/results/coefSubset/evaluate/fortyPercent/ranks/'

pdbID = testFile[:4]

with open(modelPath + 'model' + identifier + '.pkl', 'rb') as f:
    clf = pickle.load(f)

result = pd.DataFrame()
scoreList = []
df1 = pd.read_csv(testFilePath + testFile)
dropList = ['Unnamed: 0', 'Unnamed: 0.1', 'ref']
df1 = df1.drop(dropList, axis = 1)
df1 = df1.set_index('Pair_name')
df1 = pd.DataFrame(df1.values.T, columns = df1.index, index = df1.columns)
df1.fillna(0.0, inplace = True)
#df1 = df1.reindex(sorted(df1.columns), axis = 1)
# Keep coefficients within the given fraction when ordered by decreasing order of coefficient magnitude
coefs = pd.read_csv('/mnt/home/tanemur1/6May2019/2019-11-11/results/medianCoefs.csv', index_col = 0, header = None, names = ['coefficients'])
coefs['absVal'] = np.abs(coefs['coefficients'])
coefs.sort_values(by = 'absVal', ascending = False, inplace = True)
coefs = coefs[:int(14028 * coefFrac + 0.5)]
keepList = list(coefs.index)
del coefs
df1 = df1[keepList]
df1 = df1.reindex(sorted(df1.columns), axis = 1)
with open(modelPath + 'standardScaler' + identifier + '.pkl', 'rb') as g:
    scaler = pickle.load(g)
for i in range(len(df1)):
    # subtract from one row each row of the dataframe, then remove the trivial row[[i]] - row[[i]]. Also some input files have 'class' column. This is erroneous and is removed.
    df2 = pd.DataFrame(df1.iloc[[i]].values - df1.values, index = df1.index, columns = df1.columns)
    df2 = df2.drop(df1.iloc[[i]].index[0], axis = 0)

    # Standardize inut DF using the standard scaler used for training data.
    df2 = scaler.transform(df2)

    # Predict class of each comparison descriptor and sum the classes to obtain score. Higher score corresponds to more native-like complex 
    predictions = clf.predict(df2)
    score = sum(predictions)
    scoreList.append(score)

# Make a new DataFrame to store the score and corresponding descriptorID. Add rank as column. Note: lower rank corresponds to more native-like complex
result = pd.DataFrame(data = {'score': scoreList}, index = df1.index.tolist()).sort_values(by = 'score', ascending = False)
result['rank'] = range(1, len(result) + 1)

with open(outputPath + pdbID + identifier + '.csv', 'w') as h:
    result.to_csv(h)
