from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from MostImprovedPlayer_Analyze import getMIP
from PlayerStats_Analyze import getPlayerStats
from TeamWinShare_Analyze import getAllWinShare

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

api.add_resource(MostImprovedPlayer, '/mostimprovedplayerseasons/<int:p>')
api.add_resource(MostImprovedPlayerPlayoff, '/mostimprovedplayerplayoffs/<int:p>')
api.add_resource(PlayerStats, '/playerseasons/<string:p>')
api.add_resource(PlayerStatsPlayoff, '/playerplayoffs/<string:p>')
api.add_resource(TeamWinShare, '/teamwinshareseasons/<int:y>')
api.add_resource(TeamWinSharePlayoff, '/teamwinshareplayoffs/<int:y>')

app.run()