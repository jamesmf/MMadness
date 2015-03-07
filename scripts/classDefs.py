# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 18:40:55 2015

@author: jmf
"""
import numpy as np

class Team:
    """ 
    a team is defined by its mean statistics, its stdev statistics,
    its name, and its oppoenent name (as seen in other teams' game-logs)
    """
    
    def __init__(self,name,fields,mu,stds,season,srsScore):
        self.name   = name.replace(' ','-')
        self.fields = fields
        self.mu     = mu
        self.stds   = stds
        self.season = season
        self.srs    = srsScore
        
        
class Game:
    """
    a game is defined by observed statistics relating to two teams.  Either team's
    game-log can be used to create a game, as both contain all the observed
    stats.  The Game SVM will be trained on Game objects.
    
    Year is a 4 digit string of season years e. 1011, 1112...
    Score is the difference between the winning and losing team's scores
    """
    def __init__(self,year,winTeam,loseTeam,winStats,loseStats,score,oppSRS):
        self.year       = year
        self.winTeam    = winTeam
        self.loseTeam   = loseTeam
        self.winStats   = winStats
        self.loseStats  = loseStats
        self.score      = score
        self.oppSRS     = oppSRS
        
    def getWStats(self,teams):
        n = self.winTeam.replace(" ",'-')
        t = teams[str(self.year)][n]
        return [t.mu, t.stds]
#        for x in t.mu:
#            r.append(x)
#        for x in t.stds:
#            r.append(x)
#        return np.array(r)
        
    def getLStats(self,teams):
        n = self.loseTeam.replace(' ','-')
        t = teams[str(self.year)][n]
        return [t.mu, t.stds]
#        for x in t.mu:
#            r.append(x)
#        for x in t.stds:
#            r.append(x)
#        return np.array(r)