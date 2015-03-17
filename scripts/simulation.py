# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 11:52:00 2015

@author: jmf
"""
import numpy as np
import operator

avgFGA = 50. #Field Goal Attemps per game 
avgTPA = 20. #Three Point Attempts per game
expectations = [avgFGA, avgTPA]
rates = [1/avgFGA, 1/avgTPA] # rate of each attempt

eventExp = np.mean(expectations)

u = np.random.random(1000)
exponential = np.mean(-eventExp*np.log(u))


class gameSim:
    
    def __init__(self,t1rates,t2rates,t1percs,t2percs):
        self.t1score=0
        self.percs = [t1percs,t2percs]
        self.t2score=0
        self.time = 0
        self.rates=[t1rates,t2rates]
        self.poss=int(np.round(np.random.random()))
        
    def __str__(self):
        return  "Team1: "+str(self.t1score) + "  Team2: "+str(self.t2score)
        
    def oneStep(self):
        #assume poisson processes for shots, threes, turnovers
        e = np.random.random(3)
        u = np.random.random()
        print self.rates[self.poss]
        sr = np.sum(self.rates[self.poss])
        l = -np.log(e)
        ts = np.multiply(self.rates[self.poss],l)
        return np.argmin(ts),min(ts)
        
    def runGame(self):
        actioncounts=[0,0,0]
        while self.time < 1:
            action,t = self.oneStep()
            self.time += t
            print self.time
            actioncounts[action]+=1
            a=raw_input(".")
        print actioncounts
        return self.t1score, self.t2score
        
    def take2(self):
        
        
    

def simulate(Team1,Team2):
    gameSim=initTeams(Team1,Team2)
    print gameSim.runGame() 
    return gameSim
    
def initTeams(Team1,Team2):
    f = Team1.fields
    FGAn = f["fga"]
    TPAn = f["fg3"]
    OPPBLKn = f["opp_blk"]
    OPPSTLn = f["opp_stl"]
    TOVn    = f["tov"]
    OPPTOVn = f["opp_tov"]
    
    t1fga = srsAdjust(Team1.srs,Team1.mu[FGAn],"up")
    t1fg3 = srsAdjust(Team1.srs,Team1.mu[TPAn],"up")
    t1oppblk = srsAdjust(Team1.srs,Team1.mu[OPPBLKn],"down")
    t1oppstl = srsAdjust(Team1.srs,Team1.mu[OPPSTLn],"up")
    t1tov = srsAdjust(Team1.srs,Team1.mu[TOVn],"down")
    t1opptov = srsAdjust(Team1.srs,Team1.mu[OPPTOVn],"up")
    t1Rates = [1./t1fga, 1./t1fg3, 1./(np.mean(t1tov+t1opptov)+t1oppstl+t1oppblk)]
    t1percs = []
    
    t2fga = srsAdjust(Team2.srs,Team2.mu[FGAn],"up")
    t2fg3 = srsAdjust(Team2.srs,Team2.mu[TPAn],"up")
    t2oppblk = srsAdjust(Team2.srs,Team2.mu[OPPBLKn],"down")
    t2oppstl = srsAdjust(Team2.srs,Team2.mu[OPPSTLn],"up")
    t2tov = srsAdjust(Team2.srs,Team2.mu[TOVn],"down")
    t2opptov = srsAdjust(Team2.srs,Team2.mu[OPPTOVn],"up")
    t2Rates = [1./t2fga, 1./t2fg3, 1./(np.mean(t2tov+t2opptov)+t2oppstl+t2oppblk)]
    
    gameS = gameSim(t1Rates,t2Rates)
    return gameS
    
    
def srsAdjust(srs,stat,direction):
    s = srs/100.
    if direction == "up":
        return np.add(np.multiply(s,stat),stat)
    elif direction == "down":
        return np.add(np.multiply(-s,stat),stat)
    else:
        return stat
        


        
    