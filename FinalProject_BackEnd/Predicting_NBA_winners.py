#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 23:00:55 2018

@author: Reinhard
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

from collections import defaultdict
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.utils.fixes import signature
from sklearn.model_selection import GridSearchCV


def import_dataset(path_dataset = "csv/NBA_2017_2018_regularGames.csv", path_standing ="csv/ExapandedStanding2018.csv"):
    dataset = pd.read_csv(path_dataset,parse_dates=["Date"])
    standing = pd.read_csv(path_standing)    

    return dataset, standing


def clean_data(dataset,standing):
    dataset.columns = ["Date","Time","Visitor Team","Visitor Points","Home Team","Home Points","Score Type","OT?","Notes"]

    dataset["HomeWin"] = dataset["Visitor Points"] < dataset["Home Points"]
    
    #print("Home Win percentage: {0:.1f}%".format(100 * dataset["HomeWin"].sum() / dataset["HomeWin"].count()))
    
    y_true = dataset["HomeWin"].values
    
    dataset["HomeLastWin"] = False
    dataset["VisitorLastWin"] = False
    
    #### win last        
    won_last = defaultdict(int)
    
    for index, row in dataset.iterrows():
        home_team = row["Home Team"]
        visitor_team = row["Visitor Team"]
        row["HomeLastWin"] = won_last[home_team]
        row["VisitorLastWin"] = won_last[visitor_team]
        dataset.ix[index] = row
        #We then set our dictionary with the each team's result (from this row) for the next
        #time we see these teams.
        #Set current Win
        won_last[home_team] = row["HomeWin"]
        won_last[visitor_team] = not row["HomeWin"]
    
    

    ##### home team rank with standing     
    dataset["HomeTeamRanksHigher"] = 0
    for index , row in dataset.iterrows():
        home_team = row["Home Team"]
        visitor_team = row["Visitor Team"]
        home_rank = standing[standing["Team"] == home_team]["Rk"].values[0]
        visitor_rank = standing[standing["Team"] == visitor_team]["Rk"].values[0]
        row["HomeTeamRanksHigher"] = int(home_rank > visitor_rank)
        dataset.ix[index] = row
    
    
    #X_homehigher =  dataset[["HomeLastWin", "VisitorLastWin", "HomeTeamRanksHigher"]].values






    #### last win
    last_match_winner = defaultdict(int)
    dataset["HomeTeamWonLast"] = 0
    
    
    for index , row in dataset.iterrows():
        home_team = row["Home Team"]
        visitor_team = row["Visitor Team"]
    #We want to see who won the last game between these two teams regardless of which
    #team was playing at home. Therefore, we sort the team names alphabetically, giving
    #us a consistent key for those two teams:
        teams = tuple(sorted([home_team, visitor_team]))  # Sort for a consistent ordering
        # Set in the row, who won the last encounter
        row["HomeTeamWonLast"] = 1 if last_match_winner[teams] == row["Home Team"] else 0
        dataset.ix[index] = row
        # Who won this one?
        winner = row["Home Team"] if row["HomeWin"] else row["Visitor Team"]
        last_match_winner[teams] = winner
    
    
    
    X_home_higher =  dataset[["HomeTeamRanksHigher", "HomeTeamWonLast"]].values


    #### team auto encode
    
    encoding = LabelEncoder()
    #We will fit this transformer to the home teams so that it learns an integer
    #representation for each team
    encoding.fit(dataset["Home Team"].values)
    
    #We extract all of the labels for the home teams and visitor teams, and then join them
    #(called stacking in NumPy) to create a matrix encoding both the home team and the
    #visitor team for each game.
    home_teams = encoding.transform(dataset["Home Team"].values)
    visitor_teams = encoding.transform(dataset["Visitor Team"].values)
    X_teams = np.vstack([home_teams, visitor_teams]).T
    
    #we use the OneHotEncoder transformer to encode these
    #integers into a number of binary features. Each binary feature will be a single value
    #for the feature.
    
    onehot = OneHotEncoder()
    #We fit and transform on the same dataset, saving the results
    X_teams = onehot.fit_transform(X_teams).todense()
    
    
    
    
    
    X_all = np.hstack([X_home_higher, X_teams])
    return X_all,y_true




def train_classification(X_all, y_true):
    '''
    clf = RandomForestClassifier()
    scores = cross_val_score(clf, X_all, y_true, scoring='accuracy')
    print("Accuracy: {0:.1f}%".format(np.mean(scores) * 100))
    '''    
    
    parameter_space = {
    "max_features": [2, 10, 'auto'],
    "n_estimators": [100,],
    "criterion": ["gini", "entropy"],
    "min_samples_leaf": [2, 4, 6],
    }
    clf = RandomForestClassifier()
    grid = GridSearchCV(clf, parameter_space)
    grid.fit(X_all, y_true)
    #print("Accuracy: {0:.1f}%".format(grid.best_score_ * 100))
    
    
    print(grid.best_estimator_)


    
    clf_best = grid.best_estimator_
    scores = cross_val_score(clf_best, X_all, y_true, scoring='accuracy')
    print("Accuracy: {0:.1f}%".format(np.mean(scores) * 100))
    
    clf_best.fit(X_all, y_true)
    y_pred = clf_best.predict(X_all)
    prob_home_win = clf_best.predict_proba(X_all)[:,1]
    
    return clf_best, y_pred, prob_home_win


def validation(method, clf_best , y_pred, y_true, prob_home_win):
    if method == 'feature':
        ###### feature importance #########
        importances = clf_best.feature_importances_
        std = np.std([tree.feature_importances_ for tree in clf_best.estimators_],
                     axis=0)
        indices = np.argsort(importances)[::-1]
        
        # Print the feature ranking
        print("Feature ranking:")
        
        for f in range(X_all.shape[1]):
            print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))
        
        # Plot the feature importances of the forest
        plt.figure()
        plt.title("Feature importances")
        plt.bar(range(X_all.shape[1]), importances[indices],
               color="r", yerr=std[indices], align="center")
        plt.xticks(range(X_all.shape[1]), indices)
        plt.xlim([-1, X_all.shape[1]])
        plt.show()
        
        
    elif method == 'metrics':
        
        roc_auc = metrics.roc_auc_score(y_true, prob_home_win)
        print('ROC_AUC score: {0:0.2f}'.format(roc_auc))
        
        # Compute ROC curve and ROC area for each class
        fpr, tpr, _ = metrics.roc_curve(y_true, prob_home_win)
        
        plt.plot([0, 1], [0, 1], 'k--')
        plt.plot(fpr, tpr, label='RF')
        plt.xlabel('False positive rate')
        plt.ylabel('True positive rate')
        plt.title('ROC curve')
        plt.legend(loc='best')
        plt.show()
        
        
        
        
        #roc_auc = metrics.roc_auc_score(y_true, y_pred)
        average_precision = metrics.average_precision_score(y_true, y_pred)
        #precision_recall_fscore = metrics.precision_recall_fscore_support(y_true, y_pred)
        #print('ROC_AUC score: {0:0.2f}'.format(roc_auc))
        #print('Average precision-recall score: {0:0.2f}'.format(average_precision))
        #print('precision-recall fscore: {0:0.2f}'.format(precision_recall_fscore))
        
        #print(metrics.confusion_matrix(y_true, y_pred))
        print(metrics.classification_report(y_true, y_pred))
        
        precision, recall, _ = metrics.precision_recall_curve(y_true, y_pred)
        
        # In matplotlib < 1.5, plt.fill_between does not have a 'step' argument
        step_kwargs = ({'step': 'post'}
                       if 'step' in signature(plt.fill_between).parameters
                       else {})
        plt.step(recall, precision, color='b', alpha=0.2,
                 where='post')
        plt.fill_between(recall, precision, alpha=0.2, color='b', **step_kwargs)
        
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title('2-class Precision-Recall curve: AP={0:0.2f}'.format(
                  average_precision))
        plt.show()
        
        return 




def game_win_prob(dataset, X_all, y_true,clf_best):

    clf_best.fit(X_all, y_true)
    #prob_home_win = list(clf_best.predict_proba(X_all)[:,1])
    
    df = dataset[['Home Team','Visitor Team']]
    df['prob'] = clf_best.predict_proba(X_all)[:,1]
    
    df.loc[:,'prob'] = clf_best.predict_proba(X_all)[:,1]
    
    df.drop_duplicates(subset = ['Home Team','Visitor Team'],keep='last',inplace=True) 
    return df




############## play off teams

def teams_east_west(standing):
    eastern_teams =  pd.DataFrame(data=
    {'Team':['Toronto Raptors',
    'Milwaukee Bucks',
    'Indiana Pacers',
    'Boston Celtics',
    'Philadelphia 76ers',
    'Charlotte Hornets',
    'Detroit Pistons',
    'Miami Heat',
    'Brooklyn Nets',
    'New York Knicks',
    'Atlanta Hawks',
    'Orlando Magic',
    'Chicago Bulls',
    'Washington Wizards',
    'Cleveland Cavaliers']})
    
    western_teams = pd.DataFrame(data=
    {'Team':['Golden State Warriors',
    'Denver Nuggets',	
    'San Antonio Spurs',	
    'Memphis Grizzlies',
    'Portland Trail Blazers',	
    'Sacramento Kings',
    'Los Angeles Clippers',	
    'Oklahoma City Thunder',	
    'Minnesota Timberwolves',
    'Utah Jazz',
    'New Orleans Pelicans',	
    'Los Angeles Lakers',	
    'Houston Rockets',
    'Dallas Mavericks',
    'Phoenix Suns']})
    
    
    ############################# added new code #############################
        
    eastern_teams = pd.merge(eastern_teams,standing[['Rk','Team']], on = 'Team', how = 'left')  
    eastern_teams = eastern_teams.sort_values('Rk').reset_index(drop = True)
    eastern_teams = list(eastern_teams['Team'])
    
    
    western_teams = pd.merge(western_teams,standing[['Rk','Team']], on = 'Team', how = 'left')  
    western_teams = western_teams.sort_values('Rk').reset_index(drop = True)
    western_teams = list(western_teams['Team'])
    
    #teams = sorted(eastern_teams + western_teams)
    return eastern_teams, western_teams





#p = tuple(p) # create probability for tuple
def number_sample(plot = False):    
    prob = 0.05
    N = 15
    p = np.zeros(N)
    d = np.zeros(N)
    for k in range(1,N+1):
        p[k-1] = (1-prob)**(k-1)*prob
    
    
    multiplier = 1/sum(p)
    p = p*multiplier
    if plot == True:
        plt.bar(range(1,16),p, color = 'gray')
        plt.xlim(1,16)
        plt.xlabel('ranking')
        plt.ylabel('p(n)')
        plt.title('Playoff Prob at ranking n')
        plt.show()
    ######
    p = tuple(p)    
    y = (np.random.multinomial(8, p))   
    while max(y) > 1 :
        y = list(np.random.multinomial(8, p))
    #print(y)
    return y

#ns = number_sample()
#conference = eastern_teams
def team_sample(ns, conference):
    ts = []
    for i in range(len(ns)):
        if ns[i] == 1:
            ts.append(conference[i])
    return ts


def round_pairs(standing, teams):
    sample_round = []
    pair_num = len(teams)
    for i in range(int(pair_num/2)):
        if standing[standing['Team'] == teams[i]]['Rk'].iloc[0] < standing[standing['Team'] == teams[pair_num-1-i]]['Rk'].iloc[0]:
            sample_round.append([teams[i],teams[pair_num-1-i]])
        else:
            sample_round.append([teams[pair_num-1-i],teams[i]])
    return sample_round
        
def next_round_teams(df, conference_round):
    next_round = []
    for x in conference_round:
        #print(x)
        # 4 Home 3 Visitor
        p1 = df[(df['Home Team']== x[0]) &  (df['Visitor Team']== x[1])]['prob'].values[0]
        #print(p1)
        p2 = 1-df[(df['Home Team']== x[1]) &  (df['Visitor Team']== x[0])]['prob'].values[0]
        #print(p2)
        
    
        s1 = list(np.random.binomial(1, p1, 4))
        s2 = list(np.random.binomial(1, p2, 3))
        s = s1 + s2
        #print(s)
        win_id = 1*(1-sum(s)/len(s) > 0.5)
        #print(win_id)
        next_round.append(x[win_id])
    
    return next_round




def monte_carlo(eastern_teams,western_teams, df, standing,iter_team=10000):
    eastern_winner_list = []
    western_winner_list = []
    champion_list = []

    for i in range(iter_team):
        # playoff teams
        sample_eastern_teams = team_sample(ns = number_sample(), conference = eastern_teams)
        sample_western_teams = team_sample(ns = number_sample(), conference = western_teams)
        
        
        # round1 teams
        eastern_round1 = round_pairs(standing,sample_eastern_teams)
        western_round1 = round_pairs(standing,sample_western_teams)
        
        # round1 winner
        eastern_round1_winner = next_round_teams(df, eastern_round1)
        western_round1_winner = next_round_teams(df, western_round1)
        
        # round2 teams
        eastern_round2 = round_pairs(standing,eastern_round1_winner)
        western_round2 = round_pairs(standing,western_round1_winner)
        
        # round2 winner
        eastern_round2_winner = next_round_teams(df, eastern_round2)
        western_round2_winner = next_round_teams(df, western_round2)
        
        # round3 teams
        eastern_round3 = round_pairs(standing,eastern_round2_winner)
        western_round3 = round_pairs(standing,western_round2_winner)
        
        
        # round3 winner
        eastern_winner = next_round_teams(df, eastern_round3)
        western_winner = next_round_teams(df, western_round3)
        
        
        
        # champion
        champion_round = round_pairs(standing,[eastern_winner[0] , western_winner[0]])
        champion =  next_round_teams(df, champion_round)
        #print(champion_round)
        
        
        ####### winner #######
        eastern_winner_list.append(eastern_winner[0])
        western_winner_list.append(western_winner[0])
        champion_list.append(champion[0])
        
    cham_dict = Counter(champion_list)
        
    eastern_winner_dict = Counter(eastern_winner_list)
    
    western_winner_dict = Counter(western_winner_list)

    return eastern_winner_dict, western_winner_dict, cham_dict


'''

dataset, standing = import_dataset(path_dataset = "csv/NBA_2017_2018_regularGames.csv", path_standing ="csv/ExapandedStanding2018.csv")

X_all,y_true = clean_data(dataset = dataset,standing = standing)
clf_best, y_pred, prob_home_win = train_classification(X_all = X_all, y_true = y_true)
validation(method = 'metrics', clf_best = clf_best, y_pred= y_pred, y_true= y_true, prob_home_win = prob_home_win)


df = game_win_prob(X_all = X_all, y_true = y_true,clf_best = clf_best)


#p = ranking_p(plot = True)

eastern_teams, western_teams = teams_east_west()

eastern_winner_dict, western_winner_dict, cham_dict = monte_carlo(iter_team=100, eastern_teams = eastern_teams,western_teams = western_teams)




print('cham_dict:')
print(cham_dict)

print('eastern_winner_dict:')
print(eastern_winner_dict)

print('western_winner_dict:')
print(western_winner_dict)

'''


