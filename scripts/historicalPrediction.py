# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 11:10:19 2015

@author: jmf
"""

"""train an SVM, predict historical data"""

import numpy as np
import csv
from sklearn.svm import SVC


import numpy as np
import sklearn
from sklearn import svm
from os.path import isfile
import kaggle2scraped
import cPickle
import math
import sys

class predictor:
    
    def __init__(self,model,means,stds,pca):
        self.model = model
        self.means = means
        self.stds = stds
        self.pca = pca

def readPickles():
    with open("../data/allGames.pickle",'rb') as f:
        seasons = cPickle.load(f)
    with open("../data/allTeams.pickle",'rb') as f:
        teams = cPickle.load(f)
    return teams, seasons
    
#def SRSfactor(srs,npvec):
#    if srs < 0:
#        neg = True
#    else:
#        neg = False
#    s = np.sqrt()
    
def toData(teams,seasons,teamMap,gameList):
    data=[]
    labels = []
    tourneyCount=0
    for year,season in seasons.iteritems():
        for game in season:
            try:
                #print str(game.year)+" WTeam: " + str(game.winTeam) + "LTeam: "+ str(game.loseTeam)
                wTeam = teams[year][game.winTeam]
                wStat = game.getWStats(teams)
                wSRS  = wTeam.srs
#                print "game winner stats:" + str(wStat)
#                print "winning team srs: " + str(wSRS)
                lTeam = teams[year][game.loseTeam]
                lStat = game.getLStats(teams)
                lSRS  = lTeam.srs
#                print "losing team stats: "+str(lStat)
#                print "losing team srs: " + str(lSRS)

                tid = teamMap[game.loseTeam]
                tid2 = teamMap[game.winTeam]

                gameid = [year,tid,tid2]
                gameid2 = [year,tid2,tid]                                                                                                                                                                                   
                if (not (gameid in gameList)) & (not (gameid2 in gameList)):
                    if np.random.random() < 0.5: #scramble winning/losing team
                        l = [1]
                        r = []
                        r = np.append(r,wSRS)
                        r = np.append(r,wStat[0])
                        r = np.append(r,wStat[1])
                        r = np.append(r,lSRS)
                        r = np.append(r,lStat[0])
                        r = np.append(r,lStat[1])
                        r = np.array(r).flatten()
                        r = np.reshape(r,(1,r.shape[0]))
                        #print "both stats:" + str(r)                    
                    else:
                        l = [0]  
                        r = []
                        r = np.append(r,lSRS)
                        r = np.append(r,lStat[0])
                        r = np.append(r,lStat[1])
                        r = np.append(r,wSRS)
                        r = np.append(r,wStat[0])
                        r = np.append(r,wStat[1])
                        r = np.array(r).flatten()
                        r = np.reshape(r,(1,r.shape[0]))
                        #print "both stats: " +str(r)
                    if data == []:
                        data = np.array(r)
                        labels = np.array(l)
                    else:
                        data = np.append(data,r,axis=0)  
                        labels = np.append(labels,l,axis=0)
                else:
                    tourneyCount+=1
    
            except KeyError as e:
                pass
    print "tourney games skipped: "+ str(tourneyCount)
    return data, labels
    
def tourneyData(teams,tourneys,numMap):
    data=[]
    gameIDs=[]
    for x in tourneys:
        """need to set up a matrix of tournament games"""
        try:
            team1 = teams[x[0]][numMap[x[1]]]
            team2 = teams[x[0]][numMap[x[2]]]
            r = []
            r = np.append(r,team1.srs)
            r = np.append(r,team1.mu)
            r = np.append(r,team1.stds)
            r = np.append(r,team2.srs)
            r = np.append(r,team2.mu)
            r = np.append(r,team2.stds)
            r = np.array(r).flatten()
            r = np.reshape(r,(1,r.shape[0]))
            myID = "20"+x[0][2:4]+"_"+x[1]+"_"+x[2]
            print myID
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
#    cx=0
#    for x in data:
#        cy=0
#        for y in x:
#            try:
#                int(y)
##                print y
##                print type(y)
##                stop = raw_input("eee")
#            except ValueError:
#                data[cx,cy]=0
#            cy+=1
#        cx+=1
    return data, gameIDs
  
"""Read in the SRS for the teams for which I'm missing game data"""
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
    
def fixMissingData(guessfilename,gamesfilename,srs,numMap):
    print numMap
    with open(gamesfilename,'rb') as f:
        mycsv = csv.reader(f)
        games=[]
        for row in mycsv:
            games.append(row[0])
    with open(guessfilename) as f2:
        mycsv = csv.reader(f2)
        guess=[]
        guessedGames=[]
        for row in mycsv:
            guess.append(row)
            guessedGames.append(row[0])
    guess2=[]
    count=0
    sigmoid = lambda x: 1/(1.+np.exp(-x))
    for x in games:
        if not x in guessedGames:
            if not x == "id":
                print x
                year = str(int(x[2:4])-1) + str(int(x[2:4]))
                try:
                    n1 = numMap[x[5:9]]
                    n2 = numMap[x[10:]]
                    srs1 = srs[year][n1]
                    print n2
                    srs2 = srs[year][n2]
                    diff = float(srs1) - float(srs2)
                    diff = diff/8.
                    print srs1, srs2, diff
                    g = sigmoid(diff)
                    guess2.append([x, g])
                except KeyError:
                    guess2.append([x, .5])
        else:
            guess2.append(guess[count])
            count+=1
    with open("../data/guess2.csv",'wb') as f3:
        csv2 = csv.writer(f3)
        for row in guess2:
            csv2.writerow(row)
    
if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        infile = sys.argv[1]
        outfile = sys.arv[2]
    else:
        infile = "../data/kaggle/sample_submission.csv"
        outfile = "../data/historicalPredictions.csv"
    # read in team objects and game objects
    teams, seasons = readPickles() 
    #read in the tournament games from Kaggle data
    tourneys = kaggle2scraped.getKaggleGames(infile)
    #read in the map to/from Kaggle/scraped data
    teamMap, numMap = kaggle2scraped.readCSV(outfile)
    #get SRS values for missing gamelog teams
    srs = processSRS()
     
    fixMissingData(outfile,infile,srs,numMap)
    stop = raw_input("wait")
       
    
    filename = "../data/modelwPCA.pickle"
    if isfile(filename):
        print "Found Model"
        with open(filename,'rb') as f:
            model = cPickle.load(f)
            
        clf = model.model
        means = model.means
        stDev = model.stds
        pca  = model.pca
        
        d, gameIDs = tourneyData(teams,tourneys,numMap)
        data = np.divide(np.subtract(d,means),stDev)
        
        print data[0]
        pred = clf.predict_proba(data)
        
        count = 0
        with open(outfile,'wb') as f:
            mycsv = csv.writer(f)
            for p in pred:
                mycsv.writerow([gameIDs[count],p[1]])
                count+=1
            
            
    
#    else:
#        print "creating model"
#        #convert the data into a matrix for training
#        data,labels = toData(teams, seasons,teamMap,tourneys)
#        with open("../data/alldataNoTourney.pickle",'wb') as f:
#            cp = cPickle.Pickler(f)
#            cp.dump(data)
#        with open("../data/alllabelsNoTourney.pickle",'wb') as f:
#            cp = cPickle.Pickler(f)
#            cp.dump(labels)
#        means = np.mean(data,axis=0)
#        stDev = np.std(data,axis=0)
#        data = np.divide(np.subtract(data,means),stDev)
#        
#        
#        
#        
#        clf = SVC(probability=True)
#        clf.fit(data, labels) 
#        
#        model = predictor(clf,means,stDev)
#        
#        with open("../data/modelA.pickle",'wb') as f:
#            cp = cPickle.Pickler(f)
#            cp.dump(model)
