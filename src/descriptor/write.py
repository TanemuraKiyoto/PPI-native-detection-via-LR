# 16 October 2019

# Kiyoto Aramis Tanemura

# Write the scripts for individual descriptor finder jobs.

import os

pdbIDs = [x[:4] for x in os.listdir('data/CASF-PPI-2017/structures/')]

for thePDB in pdbIDs:
        command1 = 'sed "s/PDBID/' + thePDB + '/g" src/descriptor/des_finder.py '
        command3 = '> src/descriptor/finder/' + thePDB + '.py'
        os.system(command1 + command3)

#        command4 = 'sed "s/PDBID/' + thePDB + '/g" src/descriptor/run_des_finder.sb '
#        command5 = '> src/descriptor/finder/run' + thePDB + '.sb'
#        os.system(command4 + command5)
