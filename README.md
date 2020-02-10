# PPI-native-detection-via-LR
The present directory contains a scoring function for protein quaternary structure prediction. The scoring function employs a logistic regression classifier applied to detect native PPI complexes from decoy structures.

The LR scoring function was trained on Critical Assessment of Scoring Function Protein Protein Interaction 2017 (CASF-PPI-2017) dataset (Li Han, Qifan Yang, Zhihai Liu, Yan Li, & Renxiao Wang. FutureMed.Chem. 2018, 10, 1555. DOI: 10.4155/fmc-2017-0261)

Note: many of the scripts were written to have several replicates run in parallel. If the script 'write.py' is present in the directory, we recommend you modify the write.py script into a submission script to execute the individual scripts written as an output of write.py .