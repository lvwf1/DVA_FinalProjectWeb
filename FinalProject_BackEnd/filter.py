from collections import defaultdict
import csv

results = defaultdict(list)
rows=[]

with open('csv/nba_salaries_1990_to_2018.csv') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        row['Year'] = int(row['Year'])
        if(row['Year']>1999):
            rows.append(row)

with open('csv/nba_salaries_1990_to_2018.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, ['Player','Salary','Year','Tm'])
    dict_writer.writeheader()
    dict_writer.writerows(rows)
