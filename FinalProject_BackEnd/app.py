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
        return getMIP(p)

class PlayerStats(Resource):
    CORS(app)
    def get(self, p):
        return getPlayerStats(p)

class TeamWinShare(Resource):
    CORS(app)
    def get(self, y):
        return getAllWinShare(y)

api.add_resource(MostImprovedPlayer, '/mostimprovedplayer/<int:p>')
api.add_resource(PlayerStats, '/player/<string:p>')
api.add_resource(TeamWinShare, '/teamwinshare/<int:y>')

app.run()