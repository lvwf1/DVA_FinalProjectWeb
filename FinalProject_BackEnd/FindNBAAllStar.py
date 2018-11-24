import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from keras.layers import *
from keras.models import Sequential, Model
from collections import Counter
from sklearn import svm
from sklearn import neighbors
from sklearn import naive_bayes
from sklearn import tree

def selectData(dataset):
    if dataset=='d1':
        df_data = pd.read_csv("csv/Seasons_Stats_ML.csv",
                              usecols=['PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%',
                                       'STL%', 'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM',
                                       'BPM', 'VORP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%',
                                       'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV',
                                       'PF', 'PTS', 'MP/G', 'ORB/G', 'DRB/G', 'TRB/G', 'AST/G', 'STL/G', 'BLK/G',
                                       'TOV/G', 'PF/G', 'PTS/G', 'Salary'])
        df_label = pd.read_csv("csv/Seasons_Stats_ML.csv", usecols=['ID', 'Tm_Id', 'Player', 'AllStar', 'Year'])
    if dataset=='d2':
        df_data = pd.read_csv("csv/data.csv")
        df_label = pd.read_csv("csv/label.csv")
    return df_data,df_label

def LoadData(dataset):
    df_data, df_label = selectData(dataset)
    df_data_norm = (df_data - df_data.mean()) / (df_data.std() +np.spacing(0))

    if dataset=='d1':
        Year = 2018
    if dataset=='d2':
        Year = 2017
    df_data_train = df_data.loc[df_label.Year < Year]
    df_data_test = df_data.loc[df_label.Year == Year]

    df_data_norm_train = df_data_norm.loc[df_label.Year < Year]
    df_data_norm_test = df_data_norm.loc[df_label.Year == Year]

    df_label_test = df_label.loc[df_label.Year == Year]
    df_label_train = df_label.loc[df_label.Year < Year]
    return df_data_train,df_data_test,df_data_norm_train,df_data_norm_test,df_label_test,df_label_train

def PlotData(dataset):
    df_data_train, df_data_test, df_data_norm_train, df_data_norm_test, df_label_test, df_label_train=LoadData(dataset)
    plt.pie([len(df_label_train) - sum(df_label_train.AllStar), sum(df_label_train.AllStar)],
        explode=(0, 0.1), labels=["others", "all-star"], autopct='%1.1f%%',)
    plt.axis("equal")
    plt.show()

    plt.pie([len(set(df_label_train.ID)) - len(set(df_label_train.ID.loc[df_label_train.AllStar==1])),
         len(set(df_label_train.ID.loc[df_label_train.AllStar==1]))],
        explode=(0, 0.1), labels=["others", "all-star"], autopct='%1.1f%%',)
    plt.axis("equal")
    plt.show()

def getMostAllStarData(dataset, number=10):
    df_data_train, df_data_test, df_data_norm_train, df_data_norm_test, df_label_test, df_label_train = LoadData(dataset)
    allstar_times = Counter(df_label_train.Player.loc[df_label_train.AllStar==1])
    return allstar_times.most_common(number)

#SVM
def SVM(dataset):
    df_data_train, df_data_test, df_data_norm_train, df_data_norm_test, df_label_test, df_label_train = LoadData(dataset)
    svm_predict = svm.SVC().fit(df_data_norm_train,df_label_train.AllStar).predict(df_data_norm_test)
    return df_label_test.iloc[svm_predict == 1].to_dict()

#KNN
def KNN(dataset,norm):
    df_data_train, df_data_test, df_data_norm_train, df_data_norm_test, df_label_test, df_label_train = LoadData(
        dataset)
    knn_predict = neighbors.KNeighborsClassifier(n_neighbors=1).fit(df_data_norm_train,
                                                                df_label_train.AllStar).predict(df_data_norm_test)
    if norm:
        return df_label_test.iloc[knn_predict == 1].to_dict()

    df_data_train, df_data_test, df_data_norm_train, df_data_norm_test, df_label_test, df_label_train = LoadData(
        dataset)
    knn_predict = neighbors.KNeighborsClassifier(n_neighbors=1).fit(df_data_train,
                                                                df_label_train.AllStar).predict(df_data_test)
    if not norm:
        return df_label_test.iloc[knn_predict == 1].to_dict()

#Naive Bayes
def NaiveBayes(dataset):
    df_data_train, df_data_test, df_data_norm_train, df_data_norm_test, df_label_test, df_label_train = LoadData(
        dataset)
    nb_predict = naive_bayes.GaussianNB().fit(df_data_train,
                                          df_label_train.AllStar).predict(df_data_test)
    return df_label_test.iloc[nb_predict == 1].to_dict()

#Decision Tree
def DecisionTree(dataset,norm):
    df_data_train, df_data_test, df_data_norm_train, df_data_norm_test, df_label_test, df_label_train = LoadData(
        dataset)
    dt_predict = tree.DecisionTreeClassifier().fit(df_data_train,
                                               df_label_train.AllStar).predict(df_data_test)
    if not norm:
        return df_label_test.iloc[dt_predict == 1].to_dict()

    df_data_train, df_data_test, df_data_norm_train, df_data_norm_test, df_label_test, df_label_train = LoadData(
        dataset)
    dt_predict = tree.DecisionTreeClassifier().fit(df_data_norm_train,
                                               df_label_train.AllStar).predict(df_data_norm_test)
    if norm:
        return df_label_test.iloc[dt_predict == 1].to_dict()

#Neural Network

def DNN(dataset,dnn_type, norm):
    if dataset=='d1':
        Year = 2018
    if dataset=='d2':
        Year = 2017

    df_data, df_label = selectData(dataset)
    df_data_train, df_data_test, df_data_norm_train, df_data_norm_test, df_label_test, df_label_train = LoadData(
        dataset)

    dim = df_data_train.shape[1]

    model1 = Sequential()
    model1.add(Dense(100, input_dim=dim, activation="tanh"))
    model1.add(Dropout(0.5))
    model1.add(Dense(2, activation="softmax"))

    model1.compile(loss="sparse_categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"])

    idx = list(range(df_data_train.shape[0]))
    np.random.shuffle(idx)

    hist = model1.fit(df_data_train.iloc[idx],
                      df_label_train.iloc[idx].AllStar,
                      validation_split=0.2, epochs=30, shuffle=True)
    dnn_predict = model1.predict_classes(df_data_test)

    if dnn_type==1 and not norm:
        return df_label_test.iloc[dnn_predict == 1].to_dict()

    model1 = Sequential()
    model1.add(Dense(100, input_dim=dim, activation="tanh"))
    model1.add(Dropout(0.5))
    model1.add(Dense(2, activation="softmax"))

    model1.compile(loss="sparse_categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"])

    hist = model1.fit(df_data_norm_train.iloc[idx],
                      df_label_train.iloc[idx].AllStar,
                      validation_split=0.2, epochs=30, shuffle=True)
    dnn_predict = model1.predict_classes(df_data_norm_test)

    if dnn_type == 1 and norm:
        return df_label_test.iloc[dnn_predict == 1].to_dict()

    team2idx = {v: i for i, v in enumerate(set(df_label.Tm_Id))}
    player2idx = {v: i for i, v in enumerate(set(df_label.ID))}

    idx2team = {i: v for i, v in enumerate(set(df_label.Tm_Id))}
    idx2player = {i: v for i, v in enumerate(set(df_label.ID))}

    df_label["Tm_IdX"] = [team2idx[i] for i in df_label.Tm_Id]
    df_label["IDX"] = [player2idx[i] for i in df_label.ID]

    df_label_test = df_label.loc[df_label.Year == Year]
    df_label_train = df_label.loc[df_label.Year < Year]

    dim = df_data_train.shape[1]

    in_team = Input(shape=(1,))
    emb_team = Embedding(len(idx2team), 10)(in_team)

    emb_team = Flatten()(emb_team)
    in_real = Input(shape=(dim,))

    in_all = concatenate([in_real, emb_team])

    dense1 = Dense(200, activation="tanh")(in_all)
    dense1 = Dropout(0.5)(dense1)
    out = Dense(2, activation="softmax")(dense1)

    model2 = Model(inputs=[in_team, in_real], outputs=out)

    model2.compile(loss="sparse_categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"])

    hist = model2.fit([df_label_train.Tm_IdX, df_data_train.iloc[idx]],
                      df_label_train.iloc[idx].AllStar,
                      validation_split=0.2, epochs=30, shuffle=True)
    dnn_predict = model2.predict([df_label_test.Tm_IdX, df_data_test]).argmax(axis=1)

    if dnn_type==2 and not norm:
        return df_label_test.iloc[dnn_predict == 1].to_dict()

    dim = df_data_train.shape[1]

    in_team = Input(shape=(1,))
    emb_team = Embedding(len(idx2team), 10)(in_team)

    emb_team = Flatten()(emb_team)
    in_real = Input(shape=(dim,))

    in_all = concatenate([in_real, emb_team])

    dense1 = Dense(200, activation="tanh")(in_all)
    dense1 = Dropout(0.5)(dense1)
    out = Dense(2, activation="softmax")(dense1)

    model2 = Model(inputs=[in_team, in_real], outputs=out)

    model2.compile(loss="sparse_categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"])

    hist = model2.fit([df_label_train.Tm_IdX, df_data_norm_train.iloc[idx]],
                      df_label_train.iloc[idx].AllStar,
                      validation_split=0.2, epochs=30, shuffle=True)
    dnn_predict = model2.predict([df_label_test.Tm_IdX, df_data_norm_test]).argmax(axis=1)

    if dnn_type==2 and norm:
        return df_label_test.iloc[dnn_predict == 1].to_dict()

    dim = df_data_train.shape[1]

    in_team = Input(shape=(1,))
    emb_team = Embedding(len(idx2team), 10)(in_team)
    emb_team = Flatten()(emb_team)

    in_player = Input(shape=(1,))
    emb_player = Embedding(len(idx2player), 10)(in_player)
    emb_player = Flatten()(emb_player)

    in_real = Input(shape=(dim,))

    in_all = concatenate([in_real, emb_team, emb_player])

    dense1 = Dense(200, activation="tanh")(in_all)
    dense1 = Dropout(0.5)(dense1)
    out = Dense(2, activation="softmax")(dense1)

    model3 = Model(inputs=[in_team, in_player, in_real], outputs=out)

    model3.compile(loss="sparse_categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"])

    hist = model3.fit([df_label_train.Tm_IdX, df_label_train.IDX, df_data_train.iloc[idx]],
                      df_label_train.iloc[idx].AllStar,
                      validation_split=0.2, epochs=30, shuffle=True)
    model3.predict([df_label_test.Tm_IdX, df_label_test.IDX, df_data_test]).argmax(axis=1)

    if dnn_type==3 and not norm:
        return df_label_test.iloc[dnn_predict == 1].to_dict()

    dim = df_data_train.shape[1]

    in_team = Input(shape=(1,))
    emb_team = Embedding(len(idx2team), 10)(in_team)
    emb_team = Flatten()(emb_team)

    in_player = Input(shape=(1,))
    emb_player = Embedding(len(idx2player), 10)(in_player)
    emb_player = Flatten()(emb_player)

    in_real = Input(shape=(dim,))

    in_all = concatenate([in_real, emb_team, emb_player])

    dense1 = Dense(200, activation="tanh")(in_all)
    dense1 = Dropout(0.5)(dense1)
    out = Dense(2, activation="softmax")(dense1)

    model3 = Model(inputs=[in_team, in_player, in_real], outputs=out)

    model3.compile(loss="sparse_categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"])

    hist = model3.fit([df_label_train.Tm_IdX, df_label_train.IDX, df_data_norm_train.iloc[idx]],
                      df_label_train.iloc[idx].AllStar,
                      validation_split=0.2, epochs=30, shuffle=True)
    dnn_predict = model3.predict([df_label_test.Tm_IdX, df_label_test.IDX, df_data_norm_test]).argmax(axis=1)

    if dnn_type==3 and norm:
        return df_label_test.iloc[dnn_predict == 1].to_dict()