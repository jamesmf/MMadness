# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 20:33:08 2015

@author: jmf
"""
import numpy as np

def read_in_team(txt):
    with open(txt,'rb') as f:
        lines = f.readlines()
        
    fieldnames = lines[0][:-2]
    f = {}
    count = 0
    x = fieldnames.split("|")
    for name in x:
        f[name]=count
        count+=1
    print f["x"]
    
    first_col = f["pts"]
    stats = []
    print lines
    for row in lines[1:]:
        spl = row[:-1].split("|")
        spl.pop(f["x"])
        out = spl[first_col:]
        stats.append(out)
    n = np.array(stats,dtype =np.float32)
    stds = np.std(n,axis=0)
    mu   = np.mean(n,axis=0)
    
    
    
    
t = "../data/1011/air-force.txt"
read_in_team(t)