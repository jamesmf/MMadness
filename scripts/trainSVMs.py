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
    labels = []
    for year,season in seasons.iteritems():
        for game in season:
            wTeam = teams[year][game.winTeam]
            wStat = game.getWStats(teams)
            lTeam = teams[year][game.loseTeam]
            lStat = game.getLStats(teams)
            if np.random.random() < 0.5: #scramble winning/losing team
                r = []
            a=raw_input("wait")
    return data
                
teams, seasons = readPickles()
data = toData(teams, seasons)