# 25 September 2019

# Kiyoto Aramis Tanemura

# Obtain data from the ZDOCK rmsd files for calculating success rate (SR) and modified SR (Y) to compare across models.

import os
import pandas as pd

thresholds = [0.0, 1.0, 5.0, 10.0]
subdirs = ['fivePercent', 'tenPercent', 'twentyPercent', 'thirtyPercent', 'fortyPercent', 'fiftyPercent']

for theDir in subdirs:
    inputPath = '/mnt/home/tanemur1/6May2019/2019-11-11/results/coefSubset/evaluate/' + theDir + '/appendRMSD/'
    outputPath = '/mnt/home/tanemur1/6May2019/2019-11-11/results/coefSubset/evaluate/' + theDir + '/individualSR/'
    os.system('mkdir ' + outputPath)
    fileList = os.listdir(inputPath)
    for theFile in fileList:
        for thres in thresholds:
            SRi = []
            hits =[]
            HIT = 0
            counter = 1
            preFsoFar = 0
            preF = []
        
            df = pd.read_csv(inputPath + theFile)
            for i in range(df.shape[0]):
                if df.at[i, 'RMSD'] <= thres:
                    HIT += 1
                hits.append(float(HIT))
                SRi.append(int(HIT > 0))
                preFsoFar += (1 + 1 / counter) * int(df.at[i, 'RMSD'] <= thres)
                preF.append(preFsoFar)
                counter += 1
            if HIT > 0:
                K = [x / HIT for x in hits]
                F = [x / HIT for x in preF]
                myData = {'N': range(df.shape[0]), 'SRi': SRi, 'K': K, 'F': F}
                rowOutput = pd.DataFrame(myData)
                with open(outputPath + theFile[:5] + str(int(thres)) + '.csv', 'w') as g:
                    rowOutput.to_csv(g)
            else:
                print(theFile[:4] + ' yielded no hits.')
