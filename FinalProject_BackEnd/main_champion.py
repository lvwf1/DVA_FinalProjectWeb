#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 15:47:54 2018

@author: Reinhard
"""
import Predicting_NBA_winners as pred_win

def data_year(year):
    if year == 2017:
        dataset, standing = pred_win.import_dataset(path_dataset = "csv/NBA_2017_regularGames.csv", path_standing ="csv/ExapandedStanding2017.csv")
    elif year == 2018:
        # 2018
        dataset, standing = pred_win.import_dataset(path_dataset = "csv/NBA_2017_2018_regularGames.csv", path_standing ="csv/ExapandedStanding2018.csv")
    return dataset, standing

def main_champion():
    dataset, standing = data_year(year = 2018)
    
    X_all,y_true = pred_win.clean_data(dataset = dataset,standing = standing)
    clf_best, y_pred, prob_home_win = pred_win.train_classification(X_all = X_all, y_true = y_true)
    pred_win.validation(method = 'metrics', clf_best = clf_best, y_pred= y_pred, y_true= y_true, prob_home_win = prob_home_win)
    
    
    df = pred_win.game_win_prob(dataset = dataset, X_all = X_all, y_true = y_true,clf_best = clf_best)
    
    
    #p = ranking_p(plot = True)
    
    eastern_teams, western_teams = pred_win.teams_east_west(standing = standing)
    
    monte_carlo_n = 1000
    eastern_winner_dict, western_winner_dict, cham_dict = pred_win.monte_carlo(iter_team=monte_carlo_n, eastern_teams = eastern_teams,western_teams = western_teams,  df = df, standing =standing )
    
    
    
    
    print('cham_dict: with times ' + str(monte_carlo_n))
    print(cham_dict)
    '''
    print('eastern_winner_dict:')
    print(eastern_winner_dict)
    
    print('western_winner_dict:')
    print(western_winner_dict)
    '''
    return


if __name__ == "__main__":    
    main_champion()
    
    