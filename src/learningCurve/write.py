# 28 October 2019

# Kiyoto Aramis Tanemura

# Write twenty job scripts for each fraction of the learning curve.

import os

fractions = ['tenPercent', 'twentyPercent', 'thirtyPercent', 'fortyPercent', 'fiftyPercent', 'sixtyPercent', 'seventyPercent', 'eightyPercent', 'ninetyPercent', 'leaveOneOut']
fracVals = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '0.99']
theAlphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']

for i in range(len(fractions)):
#    os.system('mkdir src/learningCurve/' + fractions[i])
#    os.system('mkdir results/learningCurve/' + fractions[i])
#    os.system('mkdir results/learningCurve/' + fractions[i] + '/testAcc/')
    for theLetter in theAlphabet:
        command1 = 'sed "s/FRACTION/' + fractions[i] + '/g" src/learningCurve/lrClassifier.py '
        command2 = '| sed "s/FRACVAL/' + fracVals[i] + '/g" '
        command3 = '| sed "s/IDENTIFIER/' + theLetter + '/g" '
        command4 = '> src/learningCurve/' + fractions[i] + '/lrClassifier' + theLetter + '.py'
        os.system(command1 + command2 + command3 + command4)

#        command5 = 'sed "s/FRACTION/' + fractions[i] + '/g" src/LR/learningCurve/runLrClassifier.sb '
#        command6 = '| sed "s/TIME/' + str(int(40 * float(fracVals[i]))) + '/g" '
#        command7 = '| sed "s/MEM/' + str(int(500 * float(fracVals[i]))) + '/g" '
#        command8 = '> src/LR/learningCurve/' + fractions[i] + '/runLrClassifier' + theLetter + '.sb'
#        os.system(command5 + command6 + command7 + command3 + command8)
