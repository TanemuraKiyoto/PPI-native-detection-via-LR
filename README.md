# PPI-native-detection-via-LR
The present directory contains a scoring function for protein quaternary structure prediction. The scoring function employs a logistic regression classifier applied to detect native PPI complexes from decoy structures.

The LR scoring function was trained on Critical Assessment of Scoring Function Protein Protein Interaction 2017 (CASF-PPI-2017) dataset (Li Han, Qifan Yang, Zhihai Liu, Yan Li, & Renxiao Wang. FutureMed.Chem. 2018, 10, 1555. DOI: 10.4155/fmc-2017-0261). Please download structures from the PDBbind-CN Database (www.pdbbind.org.cn) to reproduce the training of LR classifier. Populate the directory "data/CASF-PPI-2017/structures/" with decoy set of individual PPI systems.

Descriptors were calculated using code from Jun Pei's GitHub repository (https://github.com/JunPei000/protein_folding-decoy-set). Pei's repository is associated with the following publication:

Random Forest Refinement of the KECSA2 Knowledge-Based Scoring Function for Protein Decoy Detection Jun Pei, Zheng Zheng, and Kenneth M. Merz, Jr. Journal of Chemical Information and Modeling Article ASAP DOI: 10.1021/acs.jcim.8b00734

Note: many of the scripts were written to have several replicates run in parallel. If the script 'write.py' is present in the directory, we recommend you modify the write.py script into a submission script to execute the individual scripts written as an output of write.py .

A LR classifier trained on the whole CASF-PPI-2017 dataset is located at the path, "results/LRclassifier/model.pkl", as a pickled file.