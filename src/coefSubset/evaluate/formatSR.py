# 20 October 2019

# Kiyoto Aramis Tanemura

# Individual SR csv were calculated. I will tidy and aggregate these csv files for visualization using ggplot2 on R on my local machine.

import pandas as pd
import os

os.chdir('/mnt/home/tanemur1/6May2019/2019-11-11/')

subdirs = ['fivePercent', 'tenPercent', 'twentyPercent', 'thirtyPercent', 'fortyPercent', 'fiftyPercent']

for theDir in subdirs:
    inputPath = 'results/coefSubset/evaluate/' + theDir + '/'
    outputPath = inputPath

    fileList = [x for x in os.listdir(inputPath) if x[:2] == 'SR']

    outputDf = pd.DataFrame()

    for theFile in fileList:
    # Idenfity the corresponding scoring function from file name.
        name = 'LR'
        # Get threshold value from filename as well.
        print(theFile)
        thres = int(theFile[2:-4])

        df = pd.read_csv(inputPath + theFile)
        df['SF'] = name
        df['threshold'] = thres

        outputDf = outputDf.append(df)

    with open(outputPath + 'SR.csv', 'w') as f:
        outputDf.to_csv(f)