# Take 2-parsed.csv and transform it to 3-processed.csv by merging dupe player-seasons and adding columns containing diffs from last season

from collections import defaultdict
import csv

players = defaultdict(dict)

with open('csv/Playoffs_Stats.csv') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        row['Year'] = int(row['Year'])
        row['MP'] = int(row['MP'])
        row['WS'] = float(row['WS'])
        row['WS/48'] = float(row['WS/48'])
        if (row['Year'] in players[row['PlayerId']]):
            # Merge with existing row, must have been traded (weighted sum for ws48 might not be valid)
            players[row['PlayerId']][row['Year']]['WS/48'] = (row['MP'] * row['WS/48'] + players[row['PlayerId']][row['Year']]['MP'] * players[row['PlayerId']][row['Year']]['WS/48']) / (row['MP'] + players[row['PlayerId']][row['Year']]['MP']);
            players[row['PlayerId']][row['Year']]['WS'] += row['WS'];
            players[row['PlayerId']][row['Year']]['MP'] += row['MP'];
        else:
            players[row['PlayerId']][row['Year']] = row;

def ws_max(rows, current_season):
    ws_max = -float('inf')
    for row in rows:
        row['Year'] = int(row['Year'])
        row['MP'] = int(row['MP'])
        row['WS'] = float(row['WS'])
        row['WS/48'] = float(row['WS/48'])
        if (row['WS'] > ws_max and row['Year'] < current_season):
            ws_max = row['WS']
    return ws_max

# Fill in new values: num_seasons, mp_old, ws_old, ws48_old
rows = []
for i in players:
    seasons = players[i].keys()

    for s in seasons:
        row = players[i][s]
        row['WS_max'] = ws_max(players[i].values(), s)
        if (s - 1) in seasons:
            old = players[i][s - 1]
            row['MP_old'] = old['MP']
            row['WS_old'] = old['WS']
            row['WS/48_old'] = old['WS/48']
            rows.append(row)

with open('csv/Playoffs_Stats_Processed.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file,
                                 ['PlayerId', 'Year', 'Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'MP_old', 'MP', 'PER',
                                  'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%',
                                  'OWS', 'DWS', 'WS_old', 'WS', 'WS_max', 'WS/48_old', 'WS/48', 'OBPM', 'DBPM', 'BPM',
                                  'VORP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT',
                                  'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'MP/G',
                                  'ORB/G', 'DRB/G', 'TRB/G', 'AST/G',
                                  'STL/G', 'BLK/G', 'TOV/G', 'PF/G', 'PTS/G', 'Salary'])
    dict_writer.writeheader()
    dict_writer.writerows(rows)
