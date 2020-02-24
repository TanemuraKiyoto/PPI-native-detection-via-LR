# 13 November 2019

# Kiyoto Aramis Tanemura

# Checking the extrema of the sorted coefficients show charged interactions were notably salient in classifying PPI complexes. I will summarize the distribution of various types of interactions at residue level resolution. 

# Modified 2020-01-20 by KAT. Changed names of categories so that full names are used instead of abbreviations.

import pandas as pd
import numpy as np

inPath = 'results/characterizeCoefs/'
outPath = inPath

df = pd.read_csv(inPath, index_col = 0)
df['median'] = df.median(axis = 1)
df.sort_values(by = 'median', ascending = False, inplace = True)
sorted_coeffs = list(df.index)
del df

# Given the sorted feature names, will categorize them into groups of interactions. Map function to iterate over each feature may be most concise. Thus I write individual functions for identifying the residue pairs.
# Also, list is made for each residue for identification of interacting pair. The residue can appear multiple times.
 
cationic = ['ARG', 'LYS'] # HIS omitted
anionic = ['ASP', 'GLU']
polar = ['SER', 'THR', 'ASN', 'GLN', 'CYS', 'HIS']
nonpolar = ['GLY', 'PRO', 'ALA', 'VAL', 'ILE', 'LEU', 'MET', 'PHE', 'TYR', 'TRP']
aromatic = ['PHE', 'TYR', 'TRP', 'HIS']
flexible = ['ARG', 'LYS', 'GLU', 'GLN', 'ILE', 'LEU', 'MET'] # containing of three or more linear, free rotating side chains
small = ['GLY', 'CYS', 'ALA', 'SER'] # side chain contains one carbon or less
def getResPair(feature_name):
	splitName = feature_name.split('__')
	residue1 = splitName[0][-3:]
	residue2 = splitName[1][-3:]
	return residue1, residue2

def isCatCat(feature_name):
	residue1, residue2 = getResPair(feature_name)
	return int(residue1 in cationic and residue2 in cationic)

def isAniAni(feature_name):
	residue1, residue2 = getResPair(feature_name)
	return int(residue1 in anionic and residue2 in anionic)

def isCatAni(feature_name):
	residue1, residue2 = getResPair(feature_name)
	return int((residue1 in cationic and residue2 in anionic) or (residue1 in anionic and residue2 in cationic))

def isPolPol(feature_name):
	residue1, residue2 = getResPair(feature_name)
	return int(residue1 in polar and residue2 in polar)

def isNonNon(feature_name):
	residue1, residue2 = getResPair(feature_name)
	return int(residue1 in nonpolar and residue2 in nonpolar)

def isAroAro(feature_name):
	residue1, residue2 = getResPair(feature_name)
	return int(residue1 in aromatic and residue2 in aromatic)

def isFleFle(feature_name):
	residue1, residue2 = getResPair(feature_name)
	return int(residue1 in flexible and residue2 in flexible)

def isSmaSma(feature_name):
	residue1, residue2 = getResPair(feature_name)
	return int(residue1 in small and residue2 in small)

def isPolCha(feature_name):
	residue1, residue2 = getResPair(feature_name)
	if residue1 in polar or residue2 in polar:
		return int(residue1 in cationic or residue2 in cationic or residue1 in anionic or residue2 in anionic)
	return 0

def isAroSma(feature_name):
	residue1, residue2 = getResPair(feature_name)
	return int((residue1 in small and residue2 in aromatic) or (residue1 in aromatic and residue2 in small))

def isAroFle(feature_name):
	residue1, residue2 = getResPair(feature_name)
	return int((residue1 in flexible and residue2 in aromatic) or (residue1 in aromatic and residue2 in flexible))

def isNonCha(feature_name):
	residue1, residue2 = getResPair(feature_name)
	if residue1 in nonpolar or residue2 in nonpolar:
		return int(residue1 in cationic or residue2 in cationic or residue1 in anionic or residue2 in anionic)
	return 0

catCat = list(map(isCatCat, sorted_coeffs))
aniAni = list(map(isAniAni, sorted_coeffs))
catAni = list(map(isCatAni, sorted_coeffs))
polPol = list(map(isPolPol, sorted_coeffs))
nonNon = list(map(isNonNon, sorted_coeffs))
aroAro = list(map(isAroAro, sorted_coeffs))
fleFle = list(map(isFleFle, sorted_coeffs))
smaSma = list(map(isSmaSma, sorted_coeffs))
polCha = list(map(isPolCha, sorted_coeffs))
aroSma = list(map(isAroSma, sorted_coeffs))
aroFle = list(map(isAroFle, sorted_coeffs))
nonCha = list(map(isNonCha, sorted_coeffs))

outputDf = pd.DataFrame({'cationic_cationic': catCat, 'anionic_anionic': aniAni, 'cationic_anionic': catAni, 'polar_polar': polPol, 'nonpolar_nonpolar': nonNon, 'aromatic_aromatic': aroAro, 'flexible_flexible': fleFle, 'small_small': smaSma, 'polar_charged': polCha, 'aromatic_small': aroSma, 'aromatic_flexible': aroFle, 'nonpolar_charged': nonCha})
print(outputDf)
with open(outPath + 'coefficientsCategorized.csv', 'w') as f:
	outputDf.to_csv(f)

