from collections import defaultdict
import numpy as np
import csv
import matplotlib.pyplot as plt

results = defaultdict(list)

def getWinShare(player):
    with open('csv/Seasons_Stats_Processed.csv') as csvfile:
        csvreader = csv.DictReader(csvfile)
        my_data = {}
        my_year = []
        for row in csvreader:
            row['Year'] = int(row['Year'])
            row['MP'] = int(row['MP'])
            row['WS'] = float(row['WS'])
            row['WS/48'] = float(row['WS/48'])
            if row['Player']==player:
                my_year.append(row['Year'])
                my_data[row['Year']] = {'WinShare':row['WS'],'MinutesPlay':row['MP']}

        return my_data

getWinShare('LeBron James')