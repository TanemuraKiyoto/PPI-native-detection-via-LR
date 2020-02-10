# 1 November 2019

# Kiyoto Aramis Tanemura

# Append test accuracy to train/dev accuracy results.

import pandas as pd
import numpy as np

trainDevDf = pd.read_csv('results/learningCurve/trainValAcc.csv', index_col = 0)
testDf = pd.read_csv('results/learningCurve/testAcc.csv', index_col = 0)

trainDevDf = pd.merge(trainDevDf.reset_index(), testDf.reset_index(), on =['fraction', 'index'], how = 'outer').set_index('index')

print(trainDevDf)

with open('results/learningCurve/results.csv', 'w') as f:
    trainDevDf.to_csv(f)
