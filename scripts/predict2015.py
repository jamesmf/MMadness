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
    wTeam = teams[15][t1]
    lTeam = teams[15][t2]
    game = classDefs.Game(15,t1,t2,0,0,0)
    try:  
        
        wStat = game.getWStats(teams)
        wSRS  = wTeam.srs
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
            
        srs1 = wSRS
        oppS = wTeam.avgOppSRS
        srs2 = lSRS
        opp2 = lTeam.avgOppSRS
        diff = srs1*(1+oppS/50.) - srs2*(1+opp2/50.)
        diff = diff/3.5

        if diff > 0:
            calc = 1-np.exp(-diff)
        else:
            calc = np.exp(diff)

    except KeyError as e:
        print "No game or team: " + str(e) 
    return data[0], calc
    
    
def tourneyData(teams,tourneys,numMap):
    data=[]
    gameIDs=[]
    for x in tourneys:
        """need to set up a matrix of tournament games"""
        try:
            team1 = teams[int(x[0][2:])][numMap[x[1]]]
            team2 = teams[int(x[0][2:])][numMap[x[2]]]
            r = []
            r = np.append(r,team1.srs)
            r = np.append(r,team1.avgOppSRS)
            r = np.append(r,team1.mu)
            r = np.append(r,team1.stds)
            r = np.append(r,team2.srs)
            r = np.append(r,team2.avgOppSRS)
            r = np.append(r,team2.mu)
            r = np.append(r,team2.stds)
            r = np.array(r).flatten()
            r = np.reshape(r,(1,r.shape[0]))
            myID = "20"+x[0][2:4]+"_"+x[1]+"_"+x[2]
            #print myID
            gameIDs.append(myID)
            if data == []:
                data = np.array(r,dtype=np.float)
            else:
                try:
                    data = np.append(data,r,axis=0) 
                except ValueError:
                    print r
                    stop=raw_input("whoops")
        except KeyError:
            pass
    return data, gameIDs


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
                #print row
                strongTeamid = seedMap[row[2]]
                weakTeamid = seedMap[row[3]]
                print strongTeamid, weakTeamid
                inp, calc = toData(teams,strongTeamid,weakTeamid)
                inp = inp[0]
                norm = np.subtract(inp,mu)          
                norm = np.divide(np.array(norm),var)
                tr = pca.transform(norm)
                prob = model.predict_proba(tr)
                prob = prob[0][1]
                if prob > 0.5:
                    seedMap[row[1]] = strongTeamid
                elif prob < 0.5:
                    seedMap[row[1]] = weakTeamid
                else:
                    print calc
                    if calc > .5:
                        seedMap[row[1]]= strongTeamid
                    else:
                        seedMap[row[1]]= weakTeamid
                print model.predict(tr)
                print model.predict_proba(tr)
                mycsv2.writerow([row[1], strongTeamid, weakTeamid, seedMap[row[1]]])
                #stop=raw_input(" ")
            title=False
 

data2,gameIDs = tourneyData(teams,tourneys,numMap)           
with open("../data/2015guess.csv",'wb') as f:
    mycsv = csv.writer(f)
    mycsv.writerow(["id","pred"])
    count=0
    l=len(data2[0])
    s2 = int(l/2.)
    guess2=[]
    for row in data2:
        gid = gameIDs[count]
        n1 = np.subtract(row,mu)
        n2 = np.divide(n1,var)
        tr = pca.transform(n2)
        p  = model.predict_proba(tr)
        srs1 = row[0]
        oppS = row[1]
        srs2 = row[s2]
        opp2 = row[s2+1]
        diff = srs1*(1+oppS/50.) - srs2*(1+opp2/50.)
        diff = diff/3.5

        if diff > 0:
            calc = 1-np.exp(-diff)
            if p[0][1] == .5:
                p[0][1] = calc
        else:
            calc = np.exp(diff)
            if p[0][1] == .5:
                p[0][1] = calc
        guess2.append(calc)

#            print row[0], row[1]
#            print row[s2], row[s2+1]
#            print model.predict(tr)
#            print model.predict_log_proba(tr)
        mycsv.writerow([gid,p[0][1]])
        count+=1
with open("../data/2015guess2.csv",'wb') as f:
    csv2 = csv.writer(f)
    csv2.writerow(["id","pred"])
    count=0
    for gid in gameIDs:
        csv2.writerow([gid,guess2[count]])
        count+=1
        
    