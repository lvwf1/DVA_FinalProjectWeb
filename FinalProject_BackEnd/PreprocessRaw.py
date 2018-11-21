# Take 2-parsed.csv and transform it to 3-processed.csv by merging dupe player-seasons and adding columns containing diffs from last season

import pandas as pd
import csv

df = pd.read_csv('csv/Seasons_Stats.csv') #Read Excel file as a DataFrame
'''
df['PlayerId'] = df['Player']+' '+df['Tm']
#Display top 5 rows to check if everything looks good
print(df.head(5))

#To save it back as Excel
df.to_csv('csv/Seasons_Stats.csv') #Write DateFrame back as Excel file
'''
with open('csv/Seasons_Stats.csv') as csvfile:
    csvreader = csv.DictReader(csvfile)
    currentplayer=[]
    for row in csvreader:
        if row['Year']=='2018' or row['Year']=='2017':
            currentplayer.append(row['Player'])
    print('Current Player Loading..')
    #current_df = pd.DataFrame(columns=['PlayerId','Year','Player','Pos','Age','Tm','G','GS','MP','PER','TS%','3PAr','FTr','ORB%','DRB%','TRB%','AST%','STL%','BLK%','TOV%','USG%','OWS','DWS','WS','WS/48','OBPM','DBPM','BPM','VORP','FG','FGA','FG%','3P','3PA','3P%','2P','2PA','2P%','eFG%','FT','FTA','FT%','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS'])
    current_df = []
    for p in set(currentplayer):
        current_df.append(df[df['Player'].str.contains(p)])
    pd.concat(current_df).to_csv('csv/Seasons_Stats_Processed1.csv')
