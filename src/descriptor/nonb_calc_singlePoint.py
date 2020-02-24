# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 14:22:50 2017

@author: peijun
"""

# Modified 20 May 2019 by Kiyoto Aramis Tanemura
# I suspect a bug to be present in torsion_calc_para_singlePoint.py toward the end of the script. I apply an analogous fix to the present file.

from __future__ import division
import json
from math import exp,log
import sys

from function import name

def nonb_calc_singlePoint(Interf):
    R = 1.987*10**(-3)
    T = 298
    nonb_file = open('src/descriptor/KECSA2_potential/parameterfullsummaryv1repsoft_allatomp.json','r')
    N_data = {}
    N_data = json.load(nonb_file)
    dicN_energy = {}
    for key in Interf:
        B = []
        B = name(key)
        if 'HIE' in B[0]:
            B[0] = B[0].replace('HIE','HID')
        if 'HIE' in B[1]:
            B[1] = B[1].replace('HIE','HID')
        if 'HIS' in B[0]:
            B[0] = B[0].replace('HIS','HID')
        if 'HIS' in B[1]:
            B[1] = B[1].replace('HIS','HID')
        if 'HIP' in B[0]:
            B[0] = B[0].replace('HIP','HID')
        if 'HIP' in B[1]:
            B[1] = B[1].replace('HIP','HID')
        if 'OXT' in B[0]:
            B[0] = B[0].replace('OXT','O')
        if 'OXT' in B[1]:
            B[1] = B[1].replace('OXT','O')
        ind1 = B[0].index('-')
        ind2 = B[1].index('-')
        if len(B[0][ind1+1:]) ==4 and (B[0][ind1+1]=='C' or B[0][ind1+1]=='N'):
            B[0] = B[0][:ind1+1]+B[0][ind1+2:]
        if len(B[1][ind2+1:]) ==4 and (B[1][ind2+1]=='C' or B[1][ind2+1]=='N'):
            B[1] = B[1][:ind2+1]+B[1][ind2+2:]
        key3 = B[1]+'__'+B[0]
        key4 = B[0]+'__'+B[1]
        dicN_energy[key] = []
        if key4 in N_data:
            E1 = float(N_data[key4]['E1'])
            E2 = float(N_data[key4]['E2'])
            a = float(N_data[key4]['a'])
            b = float(N_data[key4]['b'])
            sigma = float(N_data[key4]['sigma'])
            a1 = float(N_data[key4]['repa'][0])
            b1 = float(N_data[key4]['repa'][1])
            c1 = float(N_data[key4]['repa'][2])
            r_dist = float(N_data[key4]['x1'])
        elif key3 in N_data:
            E1 = float(N_data[key3]['E1'])
            E2 = float(N_data[key3]['E2'])
            a = float(N_data[key3]['a'])
            b = float(N_data[key3]['b'])
            sigma = float(N_data[key3]['sigma'])
            a1 = float(N_data[key3]['repa'][0])
            b1 = float(N_data[key3]['repa'][1])
            c1 = float(N_data[key3]['repa'][2])
            r_dist = float(N_data[key3]['x1'])
        elif not key4 in N_data and not key3 in N_data:
            print ('error! Cannot find nonb atom pair in database!', key4,key3, B[0], B[1], B[1][ind2+1])
        if key3 in N_data or key4 in N_data:
            for i in range(len(Interf[key])):
                r = 0
                r = float("{0:.3f}".format(Interf[key][i]))
                dist_vec_n_energy = []
                t = (E1*((sigma/r)**a)-E2*((sigma/r)**b))/(-R*T)
                prob = 0
                if r >=2 and r<=r_dist:
                    prob = a1*(r**2)+b1*r+c1
                elif r > r_dist:
                    if t <=500:
                        prob = exp((E1*((sigma/r)**a)-E2*((sigma/r)**b))/(-R*T))
                    elif t > 500:
                        prob = exp(500)
                elif r < 2:
                        prob = 10**(-30)
                if prob <= 10**(-30):
                        prob = 10**(-30)
                dist_vec_n_energy.append(prob)
                if dist_vec_n_energy != []:                
                    sum_dist_n_energy = 0
                    sum_dist_n_energy = sum(dist_vec_n_energy)
                    dicN_energy[key].append(sum_dist_n_energy)
                else:
                    dicN_energy[key].append(0)
    desn = {}
    for key in dicN_energy:
        sum2 = 0
        for i in range(len(dicN_energy[key])):
            sum2 += log(dicN_energy[key][i])
        desn[key] = sum2
    return desn
