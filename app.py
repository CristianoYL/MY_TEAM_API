import os

from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

from resources.user import User,UserUpdate
from resources.player import Player,PlayerList,PlayerRegistration
from resources.playerInfo import PlayerInfoByEmail,PlayerInfoByID,PlayerClubInfo
from resources.clubInfo import ClubInfoByID
from resources.club import Club,ClubByID,ClubByName,ClubRegistration
from resources.tournament import Tournament,TournamentByID,TournamentByName,TournamentByClub,TournamentRegistration
from resources.squad import Squad,SquadByClub,SquadTotal
from resources.stats import Stats,StatsList,StatsByPlayer,StatsByClubPlayer,StatsByTournamentClub
from resources.teamsheet import Teamsheet,TeamsheetByPlayer,TeamsheetByClub,TeamsheetList
from resources.result import Result,ResultByClub, ResultByHome, ResultByAway,ResultByTournamentClub

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
jwt = JWT(app,authenticate,identity)    #set up '/auth'

api.add_resource(User,'/user')
api.add_resource(UserUpdate,'/user/<string:email>')

api.add_resource(Player,'/player/<string:email>')
api.add_resource(PlayerRegistration,'/player/club/<string:clubID>')
api.add_resource(PlayerList,'/player')

api.add_resource(PlayerInfoByEmail, '/player_info/email/<string:email>')
api.add_resource(PlayerInfoByID, '/player_info/id/<string:playerID>')
api.add_resource(PlayerClubInfo, '/player_info/<string:playerID>/club/<string:clubID>')

api.add_resource(ClubInfoByID, '/club_info/id/<string:clubID>')

api.add_resource(Club,'/club')
api.add_resource(ClubRegistration,'/club/player/<string:playerID>')
api.add_resource(ClubByID,'/club/id/<string:_id>')
api.add_resource(ClubByName,'/club/name/<string:name>')

api.add_resource(Tournament,'/tournament')
api.add_resource(TournamentByID,'/tournament/id/<string:_id>')
api.add_resource(TournamentByName,'/tournament/name/<string:name>')
api.add_resource(TournamentByClub,'/tournament/club/<string:clubID>')
api.add_resource(TournamentRegistration,'/tournament/club/<string:clubID>/player/<string:playerID>')

api.add_resource(Squad,'/squad')
api.add_resource(SquadByClub,'/squad/tournament/<string:tournamentID>/club/<string:clubID>')
api.add_resource(SquadTotal,'/squad')

api.add_resource(Stats,'/stats/tournament/<string:tournamentID>/club/<string:clubID>/player/<string:playerID>')
api.add_resource(StatsByPlayer,'/stats/player/<string:playerID>')
api.add_resource(StatsByClubPlayer,'/stats/club/<string:clubID>/player/<string:playerID>')
api.add_resource(StatsByTournamentClub,'/stats/tournament/<string:tournamentID>/club/<string:clubID>')
api.add_resource(StatsList,'/stats')

api.add_resource(Teamsheet,'/teamsheet/club/<string:clubID>/player/<string:playerID>')
api.add_resource(TeamsheetByPlayer,'/teamsheet/player/<string:playerID>')
api.add_resource(TeamsheetByClub,'/teamsheet/club/<string:clubID>')
api.add_resource(TeamsheetList,'/teamsheet')

api.add_resource(Result,'/result')
api.add_resource(ResultByClub,'/result/club/<string:clubID>')
api.add_resource(ResultByHome,'/result/home/<string:clubID>')
api.add_resource(ResultByAway,'/result/away/<string:clubID>')
api.add_resource(ResultByTournamentClub,'/result/tournament/<string:tournamentID>/club/<string:clubID>')

if __name__ == '__main__' :
    from db import db
    db.init_app(app)
    app.run(host = '192.168.1.9',port = 5000,debug=True)
