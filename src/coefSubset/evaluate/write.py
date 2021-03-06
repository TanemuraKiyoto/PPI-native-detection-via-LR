# 28 October 2019

# Kiyoto Aramis Tanemura

# Write twenty job scripts for each fraction of the learning curve.

import os

subdirs = ['fivePercent', 'tenPercent', 'twentyPercent', 'thirtyPercent', 'fortyPercent', 'fiftyPercent']
thresholds = ['0.05', '0.1', '0.2', '0.3', '0.4', '0.5']
theAlphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']

for i in range(len(subdirs)):
    os.system('mkdir src/coefSubset/evaluate/testAcc/' + subdirs[i])
    os.system('mkdir src/coefSubset/evaluate/ranks/' + subdirs[i])
    for theLetter in theAlphabet:
        command1 = 'sed "s/SUBDIR/' + subdirs[i] + '/g" src/coefSubset/evaluate/testAcc.py '
        command2 = '| sed "s/THRESHOLD/' + thresholds[i] + '/g" '
        command3 = '| sed "s/IDENTIFIER/' + theLetter + '/g" '
        command4 = '> src/coefSubset/evaluate/testAcc/' + subdirs[i] + '/testAcc' + theLetter + '.py'
        os.system(command1 + command2 + command3 + command4)

        command5 = 'sed "s/SUBDIR/' + subdirs[i] + '/g" src/coefSubset/evaluate/runTestAcc.sb '
        command6 = '> src/coefSubset/evaluate/testAcc/' + subdirs[i] +  '/runTestAcc' + theLetter + '.sb'
        os.system(command5 + command3 + command6)

        if 'trainingSet' + theLetter + '.txt' not in os.listdir('results/coefSubset/' + subdirs[i]):
            continue
        with open('results/coefSubset/' + subdirs[i] + '/trainingSet' + theLetter + '.txt', 'r') as f:
            trainFiles = [x.strip() for x in f.readlines() if '.csv' in x]
        testFiles = [x for x in os.listdir('/mnt/scratch/tanemur1/CASF-PPI/nonb_descriptors/complete/') if x not in trainFiles]
        for theFile in testFiles:
            command7 = 'sed "s/FILENAME/' + theFile + '/g" src/coefSubset/evaluate/rank.py '
            command8 = '| sed "s/SUBDIR/' + subdirs[i] + '/g" '
            command9 = '> src/coefSubset/evaluate/ranks/' + subdirs[i] + '/rank_' + theFile[:4] + '_' + theLetter + '.py'
            os.system(command7 + command3 + command8 + command2 + command9)

            command10 = 'sed "s/FILENAME/' + theFile[:4] + '/g" src/coefSubset/evaluate/runRank.sb '
            command11 = '> src/coefSubset/evaluate/ranks/' + subdirs[i] + '/runRank_' + theFile[:4] + '_' + theLetter + '.sb'
            os.system(command10 + command8 + command3 + command11)

            
