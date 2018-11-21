from collections import defaultdict
import numpy as np
import csv
import matplotlib.pyplot as plt

results = defaultdict(list)

def getTeamWinShare(team,year,game):
    if game=='season':
        filename='csv/Seasons_Stats.csv'
    if game=='playoff':
        filename='csv/Playoffs_Stats_All.csv'
    with open(filename) as csvfile:
        csvreader = csv.DictReader(csvfile)
        my_ws = []
        my_ows = []
        my_dws = []
        my_ws48 = []
        my_player = []
        my_per = []
        my_pos = []
        for row in csvreader:
            row['Year'] = int(row['Year'])
            row['MP'] = int(row['MP'])
            row['WS'] = float(row['WS'])
            row['OWS'] = float(row['OWS'])
            row['DWS'] = float(row['DWS'])
            row['WS/48'] = float(row['WS/48'])
            if row['Tm']==team and row['Year']==year:
                my_ws.append(row['WS'])
                my_ows.append(row['OWS'])
                my_dws.append(row['DWS'])
                my_ws48.append(row['WS/48'])
                my_player.append(row['Player'])
                my_per.append(row['PER'])
                my_pos.append(row['Pos'])
        my_ws, my_ows, my_dws, my_player, my_pos = zip(*sorted(zip(my_ws, my_ows, my_dws, my_player, my_pos)))

    my_data = {'Player':my_player,'WS':my_ws, 'OWS':my_ows, 'DWS':my_dws, 'Pos':my_pos}
    return my_data

def getAllWinShare(year,game):
    my_data = {}
    team = getAllTeam(year,game)
    for t in team:
        my_data[t]=getTeamWinShare(t,year,game)
    return my_data

def getAllTeam(year,game):
    if game=='season':
        filename='csv/Seasons_Stats.csv'
    if game=='playoff':
        filename='csv/Playoffs_Stats_All.csv'
    with open(filename) as csvfile:
        csvreader = csv.DictReader(csvfile)
        team_set = set()
        for row in csvreader:
            row['Year'] = int(row['Year'])
            if row['Year']==year:
                team_set.add(row['Tm'])
        return sorted(team_set)