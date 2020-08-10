# PPI-native-detection-via-LR
## Last updated 2020-08-09 by Kiyoto Aramis Tanemura

The present directory contains a scoring function for protein quaternary structure prediction. The scoring function employs a logistic regression classifier applied to detect native PPI complexes from decoy structures.

This repository accompanies the research article under the following reference. Please use this reference if you use any portion of this repository.

Tanemura, K. A.; Pei, J.; Merz Jr., K. M. Proteins. 2020; 1-10. https://doi.org/10.1002/prot.25973

The LR scoring function was trained on Critical Assessment of Scoring Function Protein Protein Interaction 2017 (CASF-PPI-2017) dataset (Li Han, Qifan Yang, Zhihai Liu, Yan Li, & Renxiao Wang. FutureMed.Chem. 2018, 10, 1555. DOI: 10.4155/fmc-2017-0261). Please download structures from the PDBbind-CN Database (www.pdbbind.org.cn) to reproduce the training of LR classifier. Populate the directory "data/CASF-PPI-2017/structures/" with decoy set of individual PPI systems.

Descriptors were calculated using code from Jun Pei's GitHub repository (https://github.com/JunPei000/protein_folding-decoy-set). Pei's repository is associated with the following publication:

Random Forest Refinement of the KECSA2 Knowledge-Based Scoring Function for Protein Decoy Detection Jun Pei, Zheng Zheng, and Kenneth M. Merz, Jr. Journal of Chemical Information and Modeling 2019, 59, 5, 1919-1929. DOI: 10.1021/acs.jcim.8b00734

Note: many of the scripts were written to have several replicates run in parallel. If the script 'write.py' is present in the directory, we recommend you modify the write.py script into a submission script to execute the individual scripts written as an output of write.py .

A LR classifier trained on the whole CASF-PPI-2017 dataset is located at the path, "results/LRclassifier/model.pkl", as a pickled file.

## Presentations on the project

We posted a video explaining the work in English and in Japanese.

### Spoken Abstract: "Refinement of pairwise potentials ... to score protein-protein interactions"
<a href="https://youtu.be/Np98yvXiPaQ" target="_blank"><img src="http://img.youtube.com/vi/Np98yvXiPaQ/0.jpg" 
alt="Presentation of the project in English" width="240" height="180" border="10" /></a>

### Spoken Abstract: 「タンパク質間相互作用のスコアリング関数である力場のロジスティック回帰による精密化」
<a href="https://youtu.be/oJqzEIQ-99A" target="_blank"><img src="http://img.youtube.com/vi/oJqzEIQ-99A/0.jpg"
alt="Presentation of the project in Japanese" width="240" height="180" border="10" /></a>