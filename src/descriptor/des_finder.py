#!/bin/python

# 14 May 2019
# Kiyoto A. Tanemura
# Modification of the protein_folding-decoy-set codes to perform single point sampling of the KECSA2 database. This script is to test the modified script on a small test set.

# Modified 20 May 2019 by Kiyoto Aramis Tanemura
# My results have not agreed with Doris's results csv. I modified the single point calculation scripts and will reassess the results.

# Modified 6 June 2019 by Kiyoto Aramis Tanemura
# I am finding the torsion calculation to be time consuming and I lose a lot of the partial results when my job hits the time wall. To prevent to loss of partial results, I seek to modularize the code such that it saves partial results and can start near where it last finished.
# Specifically, I plan to increment the calculations to be every ten structures. In this manner, relatively small files are saved at each step. Once completed, the files can be appended together.

# Modified 16 October 2019 by Kiyoto Aramis Tanemura
# I will use the code as a template for new directory and decoys set. I will calculate the nonbonding energies solely. 

from __future__ import division
import os, sys
import json
import random
import pandas as pd

from nonb_calc_singlePoint import nonb_calc_singlePoint
from protein_info_finder import protein_info
from ref_des_build import ref_des_build
from function import delete_H
from change_key_to_standard import change_key_to_standard as ckts

outputPath = 'data/CASF-PPI-2017/raw_descriptors/'

# enter directory
pdbID = 'PDBID'

# enter the increment number by which the job was split
pathToDecoy = 'data/CASF-PPI-2017/structures/' + pdbID + '/'
[t, n, dictor, dicnon] = ref_des_build()

for theDecoy in [x for x in os.listdir(pathToDecoy) if x[-4:] == '.pdb']:
        p_dele_H = delete_H(pathToDecoy + theDecoy)
        lprotein = protein_info(p_dele_H)
        lprotein_tor, lprotein_nonb = lprotein
        lprotein_tor_energy, lprotein_nonb_energy = {}, {}
        lprotein_nonb_energy = nonb_calc_singlePoint(lprotein_nonb)
        lprotein_nonb_energy = ckts(dicnon, lprotein_nonb_energy)
        n[theDecoy] = n['Pair_name'].map(lprotein_nonb_energy)

with open(outputPath + pdbID + '.csv', 'w') as g:
        n.to_csv(g)
