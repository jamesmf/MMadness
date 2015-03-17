# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 19:57:23 2015

@author: jmf
"""

import csv
import historicalPrediction
import kaggle2scraped
import numpy as np
import classDefs
import cPickle

'''2015 bracket'''
class predictor:
    
    def __init__(self,model,means,stds,pca):
        self.model = model
        self.means = means
        self.stds = stds
        self.pca = pca
    
def toData(teams,t1,t2):
    data=[]
    print teams.keys()
    wTeam = teams[15][t1]
    lTeam = teams[15][t2]
    game = classDefs.Game(15,t1,t2,0,0,0)
    try:  
        
        wStat = game.getWStats(teams)
        print len(wStat)
        wSRS  = wTeam.srs
        print len(wStat[0]), len(wStat[1])
        lStat = game.getLStats(teams)
        lSRS  = lTeam.srs

        """IF USING OPP AVG SRS, ADD HERE AND IN TRAINSVMS"""
        r = []
        r = np.append(r,wSRS)
        r = np.append(r,wTeam.avgOppSRS)
        r = np.append(r,wStat[0])
        r = np.append(r,wStat[1])
        r = np.append(r,lSRS)
        r = np.append(r,lTeam.avgOppSRS)
        r = np.append(r,lStat[0])
        r = np.append(r,lStat[1])
        r = np.array(r).flatten()
        r = np.reshape(r,(1,r.shape[0]))
        if data == []:
            data = np.array(r)

    except KeyError as e:
        print "No game or team: " + str(e) 
    return data


# read in team objects and game objects
teams, seasons = historicalPrediction.readPickles() 
print teams.keys()  
#read in the tournament games from Kaggle data
tourneys = kaggle2scraped.getKaggleGames("../data/kaggle/sample_submission_2015.csv")
#read in the map to/from Kaggle/scraped data
teamMap, numMap = kaggle2scraped.readCSV("../data/team_conversions_fixed.csv")
#get SRS values for missing gamelog teams
srs = historicalPrediction.processSRS()

with open("../data/modelwPCA.pickle",'rb') as eff:
    pred = cPickle.load(eff)

model = pred.model
mu    = pred.means
var   = pred.stds
pca   = pred.pca



with open("../data/kaggle/tourney_seeds_2015.csv",'rb') as f:
    seedMap = {}
    mycsv = csv.reader(f)
    title = True
    for row in mycsv:
        if not title:
            #print row
            seedMap[row[1]] = numMap[row[2]]
        title= False                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
print seedMap

        
with open("../data/kaggle/tourney_slots_2015.csv",'rb') as f:
    mycsv = csv.reader(f)
    year = 15
    title=True
    with open("../data/my_bracket.csv",'wb') as f2:
        mycsv2 = csv.writer(f2)
        mycsv2.writerow(["Game ID","StrongSeed","WeakSeed","Winner"])
        for row in mycsv:
            if not title:
                print row
                strongTeamid = seedMap[row[2]]
                weakTeamid = seedMap[row[3]]
                print strongTeamid, weakTeamid
                inp = toData(teams,strongTeamid,weakTeamid)[0]
                print inp.shape
                print mu.shape
                print var.shape
                norm = np.subtract(inp,mu)          
                norm = np.divide(np.array(norm),var)
                tr = pca.transform(norm)
                prob = model.predict_proba(tr)
                prob = prob[0][1]
                if prob > 0.51:
                    seedMap[row[1]] = strongTeamid
                else:
                    seedMap[row[1]] = weakTeamid
                print tr
                print model.predict(tr)
                print model.predict_proba(tr)
                mycsv2.writerow([row[1], strongTeamid, weakTeamid, seedMap[row[1]]])
                stop=raw_input("whoa")
            title=False