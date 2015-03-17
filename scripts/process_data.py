# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 20:33:08 2015

@author: jmf
"""
import numpy as np
import re
import os
import classDefs
import cPickle
#import simulation

def read_in_team(txt,year,srs):
    with open(txt,'rb') as f:
        lines = f.readlines()
        
    fieldnames = lines[0][:-2]
    f = {}
    count = 0
    standardize = re.compile("[()]")
    x = fieldnames.split("|")
    topop = 1000000
    for name in x:
        if not name.strip() == 'x':
            f[name]=count
            count+=1
        else:
            topop = count
    
    try:
        a = f["year_min"]
        print a
        os.remove(txt)
        return ''
    except KeyError:
        print txt
        first_col = f["fg"]
        last_col = f["tov"]
        #last_col = f["opp_pf"]
        f2={}
        for x,y in f.iteritems():
            if y <= last_col:
                f2[x] = int(y)-int(first_col)
        stats = []
        #print lines
        srssum=0
        gamecount=0
        for row in lines[1:]:
            spl = row.split("|")
            oname = spl[f["opp_id"]]
            oname = re.sub(standardize,'',oname)
            oname = oname.replace(" ",'-').lower()
            try:
                s = srs[year][oname]
            except KeyError:
                s = -5.
            try:
                srssum+=float(s)
                gamecount+=1
            except ValueError:
                pass
            if len(spl) > topop:
                spl.pop(topop)
            out = spl[first_col:last_col+1]
            stats.append(out)
        
        try:
            n = np.array(stats,dtype =np.float32)
        except ValueError:
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
        name = re.sub(standardize,'',name)
        name = name.replace(" ",'-')
        srsScore = srs[year][name]
        avgsrs = srssum/gamecount
        t    = classDefs.Team(name,f2,mu,stds,year,srsScore,avgsrs)
    return t
    
def readOppStats(txt,year,teams):
    #figure out the %change in opposing team's stats per game
    with open(txt,'rb') as f:
        lines = f.readlines()
        
    fieldnames = lines[0][:-2]
    f = {}
    count = 0
    standardize = re.compile("[()]")
    x = fieldnames.split("|")
    topop = 1000000
    for name in x:
        if not name.strip() == 'x':
            f[name]=count
            count+=1
        else:
            topop = count
    
    try:
        a = f["year_min"]
        print a
        os.remove(txt)
        return ''
    except KeyError:
        print txt
        first_col = f["opp_fg"]
        last_col = f["opp_tov"]
        #last_col = f["opp_pf"]
        f2={}
        for x,y in f.iteritems():
            if y <= last_col:
                f2[x] = int(y)-int(first_col)
        stats = []
        #print lines
        for row in lines[1:]:

            spl = row[:-1].split("|")
            oname = spl[f["opp_id"]]
            oname = re.sub(standardize,'',oname)
            oname = oname.replace(" ",'-').lower()
            try:
                oppon = teams[oname]
                om = oppon.mu
                ost = oppon.stds
                if len(spl) > topop:
                    spl.pop(topop)
                out = spl[first_col:last_col+1]
                out = [x if not x=='' else 0.0001 for x in out]
                out = np.subtract(np.array(out,dtype=np.float),np.array(om))
                out = np.divide(np.array(out),np.array(ost))
                out = np.multiply(np.array(out),(1.-oppon.avgOppSRS))
                stats.append(out)
            except KeyError:
                pass
        
        try:
            n = np.array(stats,dtype =np.float32)
        except ValueError:
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
        name = re.sub(standardize,'',name)
        name = name.replace(" ",'-')
        old = teams[name]
        oldf=old.fields.copy()
        oldf.update(f2)
        oldmu = np.multiply(old.mu,(1+old.avgOppSRS))
        mu2 = np.append(oldmu,mu,axis=0)
        stds2 = np.append(old.stds,stds,axis=0)
        t    = classDefs.Team(name,oldf,mu2,stds2,year,old.srs,old.avgOppSRS)
    return t
    


  
#t = "../data/1011/city-college-of-new-york.txt"
#read_in_team(t)
    
def processSRS():
    with open("../data/srs.txt", 'rb') as f:
        l = f.read().split("\n")
    seasons={}
    for x in l:
        if not x == '':
            y=x.split("|")
            team = y[1]
            s = y[2]
            year2 = int(y[0][2:])
            year1 = year2-1
            ystring = str(year1)+str(year2)
            if not seasons.has_key(ystring):
                seasons[ystring]={}
            seasons[ystring][team] = float(s.strip())
    return seasons
            
            

def processTeams(srs):
    seasons={}
    seasons2={}
    for year in range(11,16):
        ystring = str(year-1)+str(year)
        teams = {}
        x = os.listdir("../data/"+ystring+"/")
        for y in x:
            p = "../data/"+ystring+"/"+y
            if p.find(".txt") >-1:
                team = read_in_team(p,ystring,srs) 
                if not team == '':
                    teams[team.name] = team
                
        seasons[ystring] = teams
    for year in range(11,16):
        ystring = str(year-1)+str(year)
        newteams = {}
        x = os.listdir("../data/"+ystring+"/")
        for y in x:
            p = "../data/"+ystring+"/"+y
            if p.find(".txt") >-1:
                team = readOppStats(p,ystring,seasons[ystring]) 
                if not team == '':
                    newteams[team.name] = team
        seasons2[year] = newteams
            
    return seasons2
    
    
def processGames():
    seasonsGames = {}
    for year in range(11,16):
            ystring = str(year-1)+str(year)
            games = []
            x = os.listdir("../data/"+ystring+"/")
            for y in x:
                p = "../data/"+ystring+"/"+y
                if p.find(".txt") >-1:
                    with open(p,'rb') as f:
                        lines = f.readlines()
                        
                    fieldnames = lines[0][:-2]
                    lines.pop(0)
                    f = {}
                    count = 0
                    x = fieldnames.split("|")
                    for name in x:
                        f[name]=count
                        count+=1
                    for row in lines:
                        spl = row[:-1].split("|")
                        spl.pop(f["x"])
                        oid = f["opp_id"]
                        tname = y.split(".")[0].lower().replace(' ','-').replace(")",'').replace("(",'')
                        oname = spl[oid].lower().replace(' ','-').replace(")",'').replace("(",'')
                        t1score = int(spl[f["pts"]])
                        t1game  = spl[f["fg"]:f["pf"]]
                        t2score = int(spl[f["opp_pts"]])
                        t2game  = spl[f["opp_fg"]:f["opp_pf"]]
                        if spl[f["game_result"]][0] == "W":
                            #team1 wins
                            game = classDefs.Game(ystring,tname,oname,t1game,t2game,t1score-t2score)
                        elif spl[f["game_result"]][0] == "L":
                            game = classDefs.Game(ystring,oname,tname,t2game,t1game,t2score-t1score)
                            #print game.winTeam, game.winStats,game.loseStats
                        games.append(game)
            seasonsGames[ystring] = games
    return seasonsGames
         
srs = processSRS()

s = processTeams(srs)   
sg = processGames()

#t1 = s["1213"]["butler"]
#t2 = s["1213"]["xavier"]
#simulation.simulate(t1,t2)


with open("../data/allTeams.pickle",'wb') as f:
    cp = cPickle.Pickler(f)
    cp.dump(s)   
with open("../data/allGames.pickle",'wb') as f:
    cp = cPickle.Pickler(f)
    cp.dump(sg)  

            