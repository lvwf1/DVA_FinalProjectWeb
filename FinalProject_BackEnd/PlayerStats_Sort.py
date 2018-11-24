from collections import defaultdict
import csv

results = defaultdict(list)

def sortPlayerStats(year, game):
    if game=='seasons':
        filename='csv/Seasons_Stats.csv'
    if game=='playoffs':
        filename='csv/Playoffs_Stats.csv'
    my_fg_rank = []
    my_ft_rank = []
    my_3p_rank = []
    my_pts_rank = []
    my_trb_rank = []
    my_ast_rank = []
    my_blk_rank = []
    my_stl_rank = []
    my_player = []
    with open(filename) as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            if int(row['Year'])==year:
                my_player.append(row['Player'])
                my_fg_rank.append(float(row['FG%']))
                my_ft_rank.append(float(row['FT%']))
                my_3p_rank.append(float(row['3P%']))
                my_pts_rank.append(float(row['PTS/G']))
                my_trb_rank.append(float(row['TRB/G']))
                my_ast_rank.append(float(row['AST/G']))
                my_blk_rank.append(float(row['BLK/G']))
                my_stl_rank.append(float(row['STL/G']))

        my_player_sort_fg = list(reversed([x for _, x in sorted(zip(my_fg_rank, my_player))]))
        my_player_sort_ft = list(reversed([x for _, x in sorted(zip(my_ft_rank, my_player))]))
        my_player_sort_3p = list(reversed([x for _, x in sorted(zip(my_3p_rank, my_player))]))
        my_player_sort_pts = list(reversed([x for _, x in sorted(zip(my_pts_rank, my_player))]))
        my_player_sort_trb = list(reversed([x for _, x in sorted(zip(my_trb_rank, my_player))]))
        my_player_sort_ast = list(reversed([x for _, x in sorted(zip(my_ast_rank, my_player))]))
        my_player_sort_blk = list(reversed([x for _, x in sorted(zip(my_blk_rank, my_player))]))
        my_player_sort_stl = list(reversed([x for _, x in sorted(zip(my_stl_rank, my_player))]))

    return {'FG%': my_player_sort_fg, 'FT%': my_player_sort_ft, '3P%': my_player_sort_3p,
            'PTS/G': my_player_sort_pts, 'TRB/G': my_player_sort_trb, 'AST/G': my_player_sort_ast,
            'BLK/G': my_player_sort_blk, 'STL/G': my_player_sort_stl}