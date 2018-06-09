from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_migrate import Migrate

from db import db
from resources.user import User, UserUpdate
from resources.player import PlayerByUser, PlayerByToken, PlayerByID, PlayerList, PlayerRegistration
from resources.playerInfo import PlayerInfoByToken, PlayerInfoByID, PlayerClubInfo
from resources.clubInfo import ClubInfoByID
from resources.club import Club, ClubByID, ClubByName, ClubRegistration
from resources.tournament import Tournament, TournamentByID, TournamentByName, TournamentByClub, \
    TournamentRegistration, TournamentManagement
from resources.squad import Squad, SquadByClub, SquadTotal
from resources.stats import Stats, StatsList, StatsByPlayer, StatsByClubPlayer, StatsByTournamentClub
from resources.member import Member, MemberByPlayer, MemberByClub, MemberList, MemberRequest, MemberPriority
from resources.result import Result, ResultByClub, ResultByHome, ResultByAway, ResultByTournamentClub
from resources.chat import TournamentChat, ClubChat, PrivateChat, Chat, ChatManager
from resources.location import Location, LocationByClub
from resources.token import Token
from resources.event import Event, EventByID, EventByClub
from resources.avatar import Avatar

app = Flask(__name__)
load_dotenv()   # load env
app.config.from_object("default_config")  # load default configs from default_config.py
app.config.from_envvar(
    "APPLICATION_SETTINGS"
)  # override with config.py (APPLICATION_SETTINGS points to config.py)
migrate = Migrate(app, db)  # enable db migration

api = Api(app)

jwt = JWTManager(app)

api.add_resource(User, '/user')
api.add_resource(UserUpdate, '/user/password')

api.add_resource(PlayerByUser, '/player/user/<int:userID>')
api.add_resource(PlayerByToken, '/player/token')
api.add_resource(PlayerByID, '/player/id/<string:playerID>')
api.add_resource(PlayerRegistration, '/player/club/<string:clubID>')
api.add_resource(PlayerList, '/player')

api.add_resource(PlayerInfoByToken, '/player_info/token')
api.add_resource(PlayerInfoByID, '/player_info/id/<string:playerID>')
api.add_resource(PlayerClubInfo, '/player_info/<string:playerID>/club/<string:clubID>')

api.add_resource(ClubInfoByID, '/club_info/id/<string:clubID>')

api.add_resource(Club, '/club')
api.add_resource(ClubRegistration, '/club/player/<string:playerID>')
api.add_resource(ClubByID, '/club/id/<string:_id>')
api.add_resource(ClubByName, '/club/name/<string:name>')

api.add_resource(Tournament, '/tournament')
api.add_resource(TournamentByID, '/tournament/id/<string:_id>')
api.add_resource(TournamentByName, '/tournament/name/<string:name>')
api.add_resource(TournamentByClub, '/tournament/club/<string:clubID>')
api.add_resource(TournamentRegistration, '/tournament/club/<int:clubID>/player/<int:playerID>')
api.add_resource(TournamentManagement, '/tournament/<string:tournamentID>/club/<string:clubID>')

api.add_resource(Squad, '/squad')
api.add_resource(SquadByClub, '/squad/tournament/<string:tournamentID>/club/<string:clubID>')
api.add_resource(SquadTotal, '/squad')

api.add_resource(Stats, '/stats/tournament/<string:tournamentID>/club/<string:clubID>/player/<string:playerID>')
api.add_resource(StatsByPlayer, '/stats/player/<string:playerID>')
api.add_resource(StatsByClubPlayer, '/stats/club/<string:clubID>/player/<string:playerID>')
api.add_resource(StatsByTournamentClub, '/stats/tournament/<string:tournamentID>/club/<string:clubID>')
api.add_resource(StatsList, '/stats')

api.add_resource(Member, '/member/club/<string:clubID>/player/<string:playerID>')
api.add_resource(MemberByPlayer, '/member/player/<string:playerID>')
api.add_resource(MemberByClub, '/member/club/<string:clubID>')
api.add_resource(MemberList, '/member')
api.add_resource(MemberRequest, '/member/request/<int:clubID>')
api.add_resource(MemberPriority, '/member/manage/club/<int:clubID>/player/<int:playerID>/promote/<string:isPromotion>')

api.add_resource(Result, '/result')
api.add_resource(ResultByClub, '/result/club/<string:clubID>')
api.add_resource(ResultByHome, '/result/home/<string:clubID>')
api.add_resource(ResultByAway, '/result/away/<string:clubID>')
api.add_resource(ResultByTournamentClub, '/result/tournament/<string:tournamentID>/club/<string:clubID>')

api.add_resource(TournamentChat, '/chat/tournament/<string:tournamentID>/club/<string:clubID>')
api.add_resource(ClubChat, '/chat/club/<string:clubID>')
api.add_resource(PrivateChat, '/chat/private/<string:receiverID>')
api.add_resource(Chat,
                 '/chat/tournament/<int:tournamentID>/club/<int:clubID>/receiver/<int:receiverID>/sender/<int:senderID>/limit/<int:limit>/before/<int:beforeID>/after/<int:afterID>')
api.add_resource(ChatManager, '/chat/<int:id>')

api.add_resource(Location, '/location/club/<int:clubID>/player/<int:playerID>')
api.add_resource(LocationByClub, '/location/club/<int:clubID>')

api.add_resource(Token, '/token/player/<int:playerID>')

api.add_resource(Event, '/event')
api.add_resource(EventByID, '/event/<int:id>')
api.add_resource(EventByClub, '/event/club/<int:clubID>')

api.add_resource(Avatar, '/avatar/player/<int:playerID>')


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=8001, debug=True)
