# 25 September 2019

# Kiyoto Aramis Tanemura

# Obtain data from the ZDOCK rmsd files for calculating success rate (SR) and modified SR (Y) to compare across models.

import os
import pandas as pd
import numpy as np

#score_functions = ['ATTRACT', 'FASTCONTACT','ZRANK','dDFIRE']
thresholds = [0.0, 1.0, 5.0, 10.0]
subdirs = ['fivePercent', 'tenPercent', 'twentyPercent', 'thirtyPercent', 'fortyPercent', 'fiftyPercent']

for theDir in subdirs:
    inputPath = '/mnt/home/tanemur1/6May2019/2019-11-11/results/coefSubset/evaluate/' + theDir + '/appendRMSD/'
    outputPath = '/mnt/home/tanemur1/6May2019/2019-11-11/results/coefSubset/evaluate/' + theDir + '/individualROC/'
    os.system('mkdir ' + outputPath)
    fileList = os.listdir(inputPath)
    for theFile in fileList:
        for thres in thresholds:
            df = pd.read_csv(inputPath + theFile)
            # Assign true labels (near native or not) based on the given threshold

            trueLabs = np.zeros(df.shape[0])

            for i in range(df.shape[0]):
                if df.at[i, 'RMSD'] <= thres:
                    trueLabs[i] = 1.0

            TPRlist = []
            FPRlist = []
            # Iterate through N to assign predicted labels. Calculate paired true positive rate (TPR) and false positive rate (FPR).
            for N in range(df.shape[0]):
                TP = float(np.sum(trueLabs[:N + 1]))
                FN = float(np.sum(trueLabs[N + 1:]))
                FP = float(N + 1 - TP)
                TN = float(len(trueLabs[N + 1:]) - FN)
                TPR = TP / (TP + FN)
                FPR = FP / (TN + FP)
                TPRlist.append(TPR)
                FPRlist.append(FPR)

            # Output paired TPR and FPR
            myData = {'TPR': TPRlist, 'FPR': FPRlist}
            outputDf = pd.DataFrame(myData)
            with open(outputPath + theFile[:4] + str(int(thres)) + '.csv', 'w') as g:
                outputDf.to_csv(g)
