# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 18:40:55 2015

@author: jmf
"""

class Team:
    """ 
    a team is defined by its mean statistics, its stdev statistics,
    its name, and its oppoenent name (as seen in other teams' game-logs)
    """
    
    def __init__(self,name,fields,mu,stds,season):
        self.name   = name.replace(' ','-')
        self.fields = fields
        self.mu     = mu
        self.stds   = stds
        self.season = season
        
        
class Game:
    """
    a game is defined by observed statistics relating to two teams.  Either team's
    game-log can be used to create a game, as both contain all the observed
    stats.  The Game SVM will be trained on Game objects.
    """