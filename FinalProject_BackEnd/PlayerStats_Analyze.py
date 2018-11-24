from collections import defaultdict
import csv

results = defaultdict(list)

def getPlayerStats(player,game):
    if game=='season':
        filename='csv/Seasons_Stats.csv'
    if game=='playoff':
        filename='csv/Playoffs_Stats.csv'
    with open(filename) as csvfile:
        csvreader = csv.DictReader(csvfile)
        my_data = {}
        my_year = []
        for row in csvreader:
            if row['Player']==player:
                my_year.append(row['Year'])
                my_data[row['Year']] = {'G': row['G'],
                                        'GS':row['GS'] ,
                                        'MP':row['MP'],
                                        'PER':row['PER'],
                                        'TS%':row['TS%'],
                                        '3PAr':row['3PAr'],
                                        'FTr':row['FTr'],
                                        'ORB%':row['ORB%'],
                                        'DRB%':row['DRB%'],
                                        'TRB%':row['TRB%'],
                                        'AST%':row['AST%'],
                                        'STL%':row['STL%'],
                                        'BLK%':row['BLK%'],
                                        'TOV%':row['TOV%'],
                                        'USG%':row['USG%'],
                                        'OWS':row['OWS'],
                                        'DWS':row['DWS'],
                                        'WS':row['WS'],
                                        'WS/48':row['WS/48'],
                                        'OBPM':row['OBPM'],
                                        'DBPM':row['DBPM'],
                                        'BPM':row['BPM'],
                                        'VORP':row['VORP'],
                                        'FG':row['FG'],
                                        'FGA':row['FGA'],
                                        'FG%':row['FG%'],
                                        '3P':row['3P'],
                                        '3PA':row['3PA'],
                                        '3P%':row['3P%'],
                                        '2P':row['2P'],
                                        '2PA':row['2PA'],
                                        '2P%':row['2P%'],
                                        'eFG%':row['eFG%'],
                                        'FT':row['FT'],
                                        'FTA':row['FTA'],
                                        'FT%':row['FT%'],
                                        'ORB':row['ORB'],
                                        'DRB':row['DRB'],
                                        'TRB':row['TRB'],
                                        'AST':row['AST'],
                                        'STL':row['STL'],
                                        'BLK':row['BLK'],
                                        'TOV':row['TOV'],
                                        'PF':row['PF'],
                                        'PTS':row['PTS'],
                                        'MP/G': row['MP/G'],
                                        'ORB/G': row['ORB/G'],
                                        'DRB/G': row['DRB/G'],
                                        'TRB/G': row['TRB/G'],
                                        'AST/G': row['AST/G'],
                                        'STL/G': row['STL/G'],
                                        'BLK/G': row['BLK/G'],
                                        'TOV/G': row['TOV/G'],
                                        'PF/G': row['PF/G'],
                                        'PTS/G': row['PTS/G'],
                                        'Salary':row['Salary']}

        return my_data