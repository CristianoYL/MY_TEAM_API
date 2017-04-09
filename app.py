import os

from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

from resources.user import User,UserUpdate
from resources.player import Player,PlayerList
from resources.club import Club,ClubByID,ClubByName
from resources.tournament import Tournament,TournamentByID,TournamentByName
from resources.squad import Squad,SquadPlayer,SquadTotal
from resources.stats import Stats,StatsList,StatsByPlayer
from resources.teamsheet import Teamsheet,TeamsheetByPlayer,TeamsheetByClub,TeamsheetList
from resources.result import Result,ResultByClub

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///myteam.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'myteam'
api = Api(app)

# comment this following section if running on Heroku
###############################
# @app.before_first_request
# def create_tables():
#     db.create_all()
###############################
jwt = JWT(app,authenticate,identity)    #/auth

api.add_resource(User,'/user')
api.add_resource(UserUpdate,'/user/<string:email>')

api.add_resource(Player,'/player/<string:email>')
api.add_resource(PlayerList,'/player')

api.add_resource(Club,'/club')
api.add_resource(ClubByID,'/club/id/<string:_id>')
api.add_resource(ClubByName,'/club/name/<string:name>')

api.add_resource(Tournament,'/tournament')
api.add_resource(TournamentByID,'/tournament/id/<string:_id>')
api.add_resource(TournamentByName,'/tournament/name/<string:name>')

api.add_resource(Squad,'/squad')
api.add_resource(SquadPlayer,'/squad/<string:tournamentID>,<string:clubID>')
api.add_resource(SquadTotal,'/squad')

api.add_resource(Stats,'/stats/<string:tournamentID>,<string:clubID>,<string:playerID>')
api.add_resource(StatsByPlayer,'/stats/player/<string:playerID>')
api.add_resource(StatsList,'/stats')

api.add_resource(Teamsheet,'/teamsheet/<string:clubID>,<string:playerID>')
api.add_resource(TeamsheetByPlayer,'/teamsheet/player/<string:playerID>')
api.add_resource(TeamsheetByClub,'/teamsheet/club/<string:clubID>')
api.add_resource(TeamsheetList,'/teamsheet')

api.add_resource(Result,'/result')
api.add_resource(ResultByClub,'/result/club/<string:clubID>')

if __name__ == '__main__' :
    from db import db
    db.init_app(app)
    app.run(host = '192.168.1.3',port = 5000,debug=True)
