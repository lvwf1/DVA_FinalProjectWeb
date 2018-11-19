from collections import defaultdict
import numpy as np
import csv
import matplotlib.pyplot as plt

results = defaultdict(list)

def getTeamWinShare(team,year):
    with open('csv/Seasons_Stats_Processed.csv') as csvfile:
        csvreader = csv.DictReader(csvfile)
        my_ws = []
        my_ws48 = []
        my_player = []
        my_per = []
        for row in csvreader:
            row['Year'] = int(row['Year'])
            row['MP'] = int(row['MP'])
            row['WS'] = float(row['WS'])
            row['WS/48'] = float(row['WS/48'])
            if row['Tm']==team and row['Year']==year:
                my_ws.append(row['WS'])
                my_ws48.append(row['WS/48'])
                my_player.append(row['Player'])
                my_per.append(row['PER'])
        my_player = [x for _, x in sorted(zip(my_ws, my_player))]
        my_ws.sort()

    my_data = {'Player':my_player,'WS':my_ws}
    return my_data

def getAllWinShare(year):
    my_data = {}
    team = getAllTeam(year)
    for t in team:
        my_data[t]=getTeamWinShare(t,year)
    return my_data

def getAllTeam(year):
    with open('csv/Seasons_Stats_Processed.csv') as csvfile:
        csvreader = csv.DictReader(csvfile)
        team_set = set()
        for row in csvreader:
            row['Year'] = int(row['Year'])
            if row['Year']==year:
                team_set.add(row['Tm'])
        return sorted(team_set)

print(getAllTeam(2017))