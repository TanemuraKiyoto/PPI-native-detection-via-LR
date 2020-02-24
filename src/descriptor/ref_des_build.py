#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 14:13:33 2018

@author: peijun
"""
import numpy as np
import pandas as pd
import json
def ref_des_build():
    torsion = {}
    t = {}
    fpt = open('src/descriptor/KECSA2_potential/torsion_para_final.json','r')
    torsion = json.load(fpt)
    for key in torsion:
        if not key in t.keys():
#        if not t.has_key(key):
            t[key] = 1.0
    descriptort = pd.DataFrame(t.items(),columns=['Pair_name', 'ref'])
    
    nonb_file = open('src/descriptor/KECSA2_potential/parameterfullsummaryv1repsoft_allatomp.json','r')
    N_data = {}
    N_data = json.load(nonb_file)
    n = {}
    for key in N_data:
        if not key in n.keys():
#        if not n.has_key(key):
            n[key] = 1.0
    descriptorn = pd.DataFrame(n.items(), columns=['Pair_name', 'ref'])
    return descriptort, descriptorn,t,n
