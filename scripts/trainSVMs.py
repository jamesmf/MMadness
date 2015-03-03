# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 16:26:16 2015

@author: jmf
"""


"""

Train an SVM to decide which team wins a game, given the observed stats for 
team1 and team2

Train multiple SVMs to predict an "observed" variable from a team's prob dist
for each statistic (computed from the season)
"""

#import sklearn
import numpy as np
import cPickle

def readPickles():
    with open("../data/allGames.pickle",'rb') as f:
        seasons = cPickle.load(f)
    with open("../data/allTeams.pickle",'rb') as f:
        teams = cPickle.load(f)
    return teams, seasons
    
def toData(teams,seasons):
    data=[]
    z   =[]
    labels = []
    for year,season in seasons.iteritems():
        for game in season:
            try:
                wTeam = teams[year][game.winTeam]
                print wTeam
                wStat = game.getWStats(teams)
                print wStat
                lTeam = teams[year][game.loseTeam]
                print lTeam
                lStat = game.getLStats(teams)
                print lStat
                if np.random.random() < 0.5: #scramble winning/losing team
                    r = np.array([wStat[0],wStat[1],lStat[0],lStat[1]]).flatten()
                    r = np.reshape(r,(1,r.shape[0]))
                    print game.winStats
                    wmu = np.subtract(game.winStats,wStat[0])
                    print wmu
                else:
                    r = np.array([lStat,wStat]).flatten()
                    r = np.reshape(r,(1,r.shape[0]))
                    print game.loseStats
                    lmu = np.subtract(game.loseStats,lStat[0])
                    print lmu
                    
                a=raw_input("wait")
            except KeyError:
                pass
    return data
                
teams, seasons = readPickles()
data = toData(teams, seasons)