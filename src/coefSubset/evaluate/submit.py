# 28 October 2019

# Kiyoto Aramis Tanemura

# Write twenty job scripts for each fraction of the learning curve.

import os

subdirs = ['fivePercent', 'tenPercent', 'twentyPercent', 'thirtyPercent', 'fortyPercent', 'fiftyPercent']
thresholds = ['0.05', '0.1', '0.2', '0.3', '0.4', '0.5']
theAlphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']

for i in range(len(subdirs)):
#    os.system('mkdir results/coefSubset/evaluate/' + subdirs[i])
#    os.system('mkdir results/coefSubset/evaluate/' + subdirs[i] + '/testAcc/')
#    os.system('mkdir results/coefSubset/evaluate/' + subdirs[i] + '/ranks/')
    for theLetter in theAlphabet:
        if theLetter + 'performance.txt' in os.listdir('results/coefSubset/evaluate/' + subdirs[i] + '/testAcc/'):
            continue
        os.system('sbatch src/coefSubset/evaluate/testAcc/' + subdirs[i] +  '/runTestAcc' + theLetter + '.sb')

    scrs = [x for x in os.listdir('src/coefSubset/evaluate/ranks/' + subdirs[i]) if x[:3] == 'run']
    for theScr in scrs:
        vals = theScr.split('_')
        if vals[1] + vals[2][0] + '.csv' in os.listdir('results/coefSubset/evaluate/' + subdirs[i] + '/ranks/'):
            continue
        os.system('sbatch src/coefSubset/evaluate/ranks/' + subdirs[i] + '/' + theScr)
