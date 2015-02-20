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
    
    def __init__(self,name,o_name,mu,stds):
        self.mu = mu