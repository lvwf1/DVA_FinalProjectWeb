from collections import defaultdict
import csv

players = defaultdict(dict)
new_rows = []

with open('csv/Playoffs_Stats_ML.csv') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        row['MP/G'] = int(row['MP'])/int(row['G'])
        row['ORB/G'] = int(row['ORB']) / int(row['G'])
        row['DRB/G'] = int(row['DRB']) / int(row['G'])
        row['TRB/G'] = int(row['TRB']) / int(row['G'])
        row['AST/G'] = int(row['AST']) / int(row['G'])
        row['STL/G'] = int(row['STL']) / int(row['G'])
        row['BLK/G'] = int(row['BLK']) / int(row['G'])
        row['TOV/G'] = int(row['TOV']) / int(row['G'])
        row['PF/G'] = int(row['PF']) / int(row['G'])
        row['PTS/G'] = int(row['PTS']) / int(row['G'])
        new_rows.append(row)

with open('csv/Playoffs_Stats_ML_new.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file,
                                 ['PlayerId', 'Year', 'Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'MP', 'PER',
                                  'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%',
                                  'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP', 'FG', 'FGA', 'FG%', '3P',
                                  '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB',
                                  'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'MP/G','ORB/G', 'DRB/G', 'TRB/G', 'AST/G',
                                  'STL/G', 'BLK/G', 'TOV/G', 'PF/G', 'PTS/G', 'Salary', 'ID', 'Tm_Id', 'AllStar'])
    dict_writer.writeheader()
    dict_writer.writerows(new_rows)
