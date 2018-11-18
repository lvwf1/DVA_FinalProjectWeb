from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from MIP_Analyze import GetMIP
from PlayerWinShare_Analyze import getWinShare

app = Flask(__name__)
api = Api(app)

class MostImprovedPlayer(Resource):
    CORS(app)
    def get(self, p):
        return GetMIP(p)

class PlayerWinShare(Resource):
    CORS(app)
    def get(self, p):
        return getWinShare(p)

api.add_resource(MostImprovedPlayer, '/mostimprovedplayer/<int:p>')
api.add_resource(PlayerWinShare, '/playerwinshare/<string:p>')

app.run()