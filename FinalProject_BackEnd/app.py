from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from MostImprovedPlayer_Analyze import getMIP
from PlayerStats_Analyze import getPlayerStats
from TeamWinShare_Analyze import getAllWinShare
from FindNBAAllStar import getMostAllStarData,SVM,KNN,NaiveBayes,DecisionTree,DNN
from PlayerStats_Sort import sortPlayerStats

app = Flask(__name__)
api = Api(app)

class MostImprovedPlayer(Resource):
    CORS(app)
    def get(self, p):
        return getMIP(p,'season')

class MostImprovedPlayerPlayoff(Resource):
    CORS(app)
    def get(self, p):
        return getMIP(p,'playoff')

class PlayerStats(Resource):
    CORS(app)
    def get(self, p):
        return getPlayerStats(p,'season')

class PlayerStatsPlayoff(Resource):
    CORS(app)
    def get(self, p):
        return getPlayerStats(p,'playoff')

class TeamWinShare(Resource):
    CORS(app)
    def get(self, y):
        return getAllWinShare(y,'season')

class TeamWinSharePlayoff(Resource):
    CORS(app)
    def get(self, y):
        return getAllWinShare(y,'playoff')

class getAllStar(Resource):
    CORS(app)
    def get(self, m, d, n):
        if m=='SVM':
            return SVM(d)
        if m=='KNN':
            return KNN(d, n)
        if m=='NaiveBayes':
            return NaiveBayes(d)
        if m=='DecisionTree':
            return DecisionTree(d,n)
        if m=='DNN1':
            return DNN(d,1,n)
        if m=='DNN2':
            return DNN(d,2,n)
        if m=='DNN3':
            return DNN(d,3,n)

class getAllStarMost(Resource):
    CORS(app)
    def get(self, d):
        return getMostAllStarData(d)

class sortStats(Resource):
    CORS(app)
    def get(self, y, g):
        return sortPlayerStats(y,g)

api.add_resource(MostImprovedPlayer, '/mostimprovedplayerseasons/<int:p>')
api.add_resource(MostImprovedPlayerPlayoff, '/mostimprovedplayerplayoffs/<int:p>')
api.add_resource(PlayerStats, '/playerseasons/<string:p>')
api.add_resource(PlayerStatsPlayoff, '/playerplayoffs/<string:p>')
api.add_resource(TeamWinShare, '/teamwinshareseasons/<int:y>')
api.add_resource(TeamWinSharePlayoff, '/teamwinshareplayoffs/<int:y>')
api.add_resource(getAllStar, '/allstar/<string:m>/<string:d>/<string:n>')
api.add_resource(getAllStarMost, '/allstar/<string:d>')
api.add_resource(sortStats, '/sortstats/<int:y>/<string:g>')

app.run()