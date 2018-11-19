from collections import defaultdict
import numpy as np
import csv
import matplotlib.pyplot as plt

results = defaultdict(list)

def getPlayerStats(player):
    with open('csv/Seasons_Stats_Processed.csv') as csvfile:
        csvreader = csv.DictReader(csvfile)
        my_data = {}
        my_year = []
        for row in csvreader:
            row['Year'] = int(row['Year'])
            row['MP'] = int(row['MP'])
            row['WS'] = float(row['WS'])
            row['PER'] = float(row['PER'])
            if row['Player']==player:
                my_year.append(row['Year'])
                my_data[row['Year']] = {'WS':row['WS'],'MP':row['MP'],'PER':row['PER']}

        return my_data