from collections import defaultdict
import csv
import matplotlib.pyplot as plt
import numpy as np

def getMIP(year,game):
    results = defaultdict(list)
    if game=='season':
        filename='csv/Seasons_Stats_Processed.csv'
    if game=='playoff':
        filename='csv/Playoffs_Stats_Processed.csv'
    with open(filename) as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            row['Year'] = int(row['Year'])
            row['MP'] = int(row['MP'])
            row['MP_old'] = int(row['MP_old'])
            row['WS_old'] = float(row['WS_old'])
            row['WS'] = float(row['WS'])
            row['WS_max'] = float(row['WS_max'])
            row['WS/48'] = float(row['WS/48'])
            row['WS/48_old'] = float(row['WS/48_old'])
            # Increasing WS by 5 is equal weight to increasing WS/48 by 0.1
            row['score'] = 0.02 * (row['WS'] - row['WS_old']) + (row['WS/48'] - row['WS/48_old'])
            # Penalty - lose 0.05 for every MPg last season under 15 (assuming 82 games)
            if row['MP_old'] < 82 * 15:
                row['score'] -= 0.05 * (15 - row['MP_old'] / 82)
            # Penalty - lose additional 0.05 for every MPg last season under 10 (assuming 82 games)
            if row['MP_old'] < 82 * 15:
                row['score'] -= 0.05 * (15 - row['MP_old'] / 82)
            # Penalty - lose 0.01 for every MPg this season under 30 (assuming 82 games)
            if row['MP'] < 82 * 30:
                row['score'] -= 0.01 * (30 - row['MP'] / 82)
            # Penalty - baseline required is 125% of previous best season. Lose 0.01 for every 1% below that.
            if row['WS'] < 1.25 * row['WS_max']:
                ratio = 1
                if row['WS_max'] != 0.0:
                    ratio = row['WS'] / row['WS_max']
                # Sanity check... don't want two negative numbers blowing up the ratio
                if ratio < 0 or (row['WS'] < 0 and row['WS_max'] < 0):
                    ratio = 0.0
                row['score'] -= 1.25 - ratio
            if row['Year']==year:
                results[row['Year']].append(row)
        for s in sorted(results.keys()):
            sorted_results = sorted(results[s], key=lambda row: row['score'], reverse=True)
        return sorted_results