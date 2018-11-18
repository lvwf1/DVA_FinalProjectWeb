from collections import defaultdict
import numpy as np
import csv
import matplotlib.pyplot as plt

results = defaultdict(list)

def plotWinShare(team):
    with open('csv/Seasons_Stats_Processed.csv') as csvfile:
        csvreader = csv.DictReader(csvfile)
        year_list=[2013,2014,2015,2016,2017]
        my_ws = [[] for i in year_list]
        my_ws48 = [[] for i in year_list]
        my_player = [[] for i in year_list]
        for row in csvreader:
            row['Year'] = int(row['Year'])
            row['MP'] = int(row['MP'])
            row['WS'] = float(row['WS'])
            row['WS/48'] = float(row['WS/48'])
            for j in range(len(year_list)):
                if row['Tm']=='OKC' and row['Year']==year_list[j]:
                    my_ws[j].append(row['WS'])
                    my_ws48[j].append(row['WS/48'])
                    my_player[j].append(row['Player'])
        for j in range(len(year_list)):
            my_player[j] = [x for _, x in sorted(zip(my_ws[j], my_player[j]))]
            my_ws[j].sort()

    for j in range(len(year_list)):
        current_height = 0
        colors = plt.cm.seismic(np.linspace(0, 1, len(my_player[j])))
        for i in range(len(my_player[j])):
            plt.bar(str(year_list[j]-1)+'-'+str(year_list[j]),my_ws[j][i], width=0.5, label=my_player[j][i]+'@'+str(year_list[j]-1)+'-'+str(year_list[j]), color=colors[i], bottom=current_height)
            plt.legend(loc='upper left', ncol=6, fancybox=True, shadow=True, fontsize='xx-small')
            current_height+=my_ws[j][i]


    plt.ylabel("Win Share")
    plt.yticks(np.arange(0, 101, 10))
    plt.xlabel("Year")
    plt.title(team+' Players Win Share')

    plt.show()

plotWinShare('BOS')