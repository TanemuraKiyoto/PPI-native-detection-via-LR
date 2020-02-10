# 23 November 2019

# Kiyoto Aramis Tanemura

# Run a bunch of the scrips.

import os

inpath = 'src/coefSubset/evaluate/'

os.system('python ' + inpath + 'appendRMSD.py')
os.system('python ' + inpath + 'individualSR.py')
os.system('python ' + inpath + 'getSR.py')
os.system('python ' + inpath + 'nativeRank.py')
os.system('python ' + inpath + 'firstRMSD.py')
os.system('python ' + inpath + 'firstDecoyRMSD.py')
