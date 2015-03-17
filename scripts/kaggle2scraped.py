# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 08:20:12 2015

@author: jmf
"""
import csv
import numpy as np
import cPickle

"""getting pickled team/season files"""
def getPickle(tPick):
    with open(tPick,'rb') as f:
        return cPickle.load(f)




"""Mapping Kaggle teams to scraped data"""

""" return a dictionary of """
def readCSV(filename):
    with open(filename,'rb') as f:
        mycsv = csv.reader(f)
        d={}
        d2={}
        for row in mycsv:
            d[row[2]] = row[0]
            d2[row[0]] = row[2]
    return d, d2
    
def getKaggleGames(filename):
    with open(filename,'rb') as f:
        mycsv = csv.reader(f)
        games=[]
        for row in mycsv:
            if row[0].find("20") > -1:
                y = int(row[0][2:4])
                ystring = str(y-1)+str(y)
                t1=row[0][5:9]
                t2=row[0][10:14]
                games.append([ystring,t1,t2])
    return games
    
   
def toData(teams,gameList,numMap):
    data=[]
    for game in gameList:
        year = game[0]
        t1 = numMap[game[1]]
        t2 = numMap[game[2]]
        try:
            #print str(game.year)+" WTeam: " + str(game.winTeam) + "LTeam: "+ str(game.loseTeam)
            wTeam = teams[year][t1]
            wStat = [wTeam.mu,wTeam.stds]
            wSRS  = wTeam.srs
            lTeam = teams[year][t2]
            lStat = [lTeam.mu,lTeam.stds]
            lSRS  = lTeam.srs

            r = []
            r = np.append(r,wSRS)
            r = np.append(r,wStat[0])
            r = np.append(r,wStat[1])
            r = np.append(r,lSRS)
            r = np.append(r,lStat[0])
            r = np.append(r,lStat[1])
            r = np.array(r).flatten()
            r = np.reshape(r,(1,r.shape[0]))
            if data == []:
                data = np.array(r)
            else:
                data = np.append(data,r,axis=0)  

        except KeyError as e:
            #print "No game or team: " + str(e) 
            pass
    return data
    
def toCSV(data):
    with open("historical_pred.csv",'wb') as f:
        mycsv = csv.writer(f)
        for r in data:
            mycsv.writerow(r)
    
teams = getPickle("../data/allTeams.pickle")            
teamMap, numMap = readCSV("../data/team_conversions_fixed.csv")
tourneys = getKaggleGames("../data/kaggle/sample_submission.csv")
data = toData(teams,tourneys,numMap)
toCSV(data)


