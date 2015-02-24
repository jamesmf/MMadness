# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 20:33:08 2015

@author: jmf
"""
import numpy as np
import os
import classDefs
import cPickle

def read_in_team(txt,year):
    with open(txt,'rb') as f:
        lines = f.readlines()
        
    fieldnames = lines[0][:-2]
    f = {}
    count = 0
    x = fieldnames.split("|")
    for name in x:
        f[name]=count
        count+=1
    
    try:
        a = f["year_min"]
        print a
        os.remove(txt)
        return ''
    except KeyError:
        print txt
        first_col = f["pts"]
        stats = []
        #print lines
        for row in lines[1:]:
            spl = row[:-1].split("|")
            spl.pop(f["x"])
            out = spl[first_col:]
            stats.append(out)
        
        try:
            n = np.array(stats,dtype =np.float32)
        except ValueError as e:
            count1=0
            for a in stats:
                count2=0
                for b in a:
                    if (b.replace(' ','')=='') | (b==' '):
                        print b  
                        stats[count1][count2] = 0.
                    count2+=1
                count1+=1
            n = np.array(stats,dtype = np.float32)
        stds = np.std(n,axis=0)
        mu   = np.mean(n,axis=0)
        name = txt.split("/")[-1].replace(".txt",'')
        t    = classDefs.Team(name,f,mu,stds,year)
    return t
    
    
    
#    
#t = "../data/1011/city-college-of-new-york.txt"
#read_in_team(t)

def processTeams():
    seasons={}
    for year in range(11,16):
        ystring = str(year-1)+str(year)
        teams = {}
        x = os.listdir("../data/"+ystring+"/")
        for y in x:
            p = "../data/"+ystring+"/"+y
            if p.find(".txt") >-1:
                team = read_in_team(p,ystring) 
                if not team == '':
                    teams[team.name] = team
                
        seasons[ystring] = teams
    return seasons
             
s = processTeams()   
print s["1011"]["kansas-state"].mu
print s["1011"]["kansas-state"].stds 
print s["1011"]["kansas-state"].name
with open("../data/allTeams.pickle",'wb') as f:
    cp = cPickle.Pickler(f)
    cp.dump(s)   

            