from collections import defaultdict
import csv
import matplotlib.pyplot as plt
import numpy as np

results = defaultdict(list)

with open('csv/Seasons_Stats_Processed.csv') as csvfile:
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
        results[row['Year']].append(row)
    #print(results)

def plotMIP(year):
    for s in sorted(results.keys()):
        sorted_results = sorted(results[s], key=lambda row: row['score'], reverse=True)
        print()
        print("%d Year" % (s,))
        for i in range(len(sorted_results)):
            row = sorted_results[i]
            print("%2d. %s\n    Score: %.3f\n    WS %.1f -> %.1f, WS/48 %.3f -> %.3f, MP: %d -> %d" % (
            i + 1, row['Player'], row['score'], row['WS_old'], row['WS'], row['WS/48_old'], row['WS/48'], row['MP_old'],
            row['MP']))
            if (i >= 9):
                break

        if s == year:
            # set width of bar
            barWidth = 0.2

            MIP = [sorted_results[i]['Player'] for i in range(len(sorted_results))]
            # set height of bar
            bars1 = [sorted_results[i]['WS_old'] for i in range(len(sorted_results[:5]))]
            bars2 = [sorted_results[i]['WS'] for i in range(len(sorted_results[:5]))]
            bars3 = [sorted_results[i]['MP_old'] for i in range(len(sorted_results[:5]))]
            bars4 = [sorted_results[i]['MP'] for i in range(len(sorted_results[:5]))]

            # Set position of bar on X axis
            r1 = [x + barWidth / 2 for x in np.arange(len(bars1))]
            r2 = [x + barWidth for x in r1]
            r3 = [x + barWidth / 2 for x in np.arange(len(bars1))]
            r4 = [x + barWidth for x in r1]

            plt.subplot(2, 1, 1)
            plt.title('Most Improved Player in ' + str(year-1) + '-' + str(year))
            # Make the plot
            plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label=s - 1)
            plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label=s)
            # Add xticks on the middle of the group bars
            plt.xlabel('Most Improved Player', fontweight='bold')
            plt.ylabel('Win Share', fontweight='bold')
            plt.xticks([r + barWidth for r in range(len(bars1))], MIP[:5])
            # Create legend
            plt.legend()

            plt.subplot(2, 1, 2)
            # Make the plot
            plt.bar(r3, bars3, color='#7f6d5f', width=barWidth, edgecolor='white', label=s - 1)
            plt.bar(r4, bars4, color='#557f2d', width=barWidth, edgecolor='white', label=s)
            # Add xticks on the middle of the group bars
            plt.xlabel('Most Improved Player', fontweight='bold')
            plt.ylabel('Minites Played', fontweight='bold')
            plt.xticks([r + barWidth for r in range(len(bars1))], MIP[:5])

            # Create legend
            plt.legend()

            # Show graphic
            plt.show()

plotMIP(2018)