from collections import defaultdict
import numpy as np
import csv
import matplotlib.pyplot as plt

results = defaultdict(list)

def getPlayerList(player):
    with open('csv/Seasons_Stats_Processed.csv') as csvfile:
        csvreader = csv.DictReader(csvfile)
        my_player = set()
        for row in csvreader:
            my_player.add(row['Player'])

        print(my_player)