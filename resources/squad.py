import traceback
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

from models.squad import SquadModel
from models.player import PlayerModel
from utils.firebase import FireBase

class Squad(Resource):
    # tid,cid,pid,number
    parser = reqparse.RequestParser()
    parser.add_argument('tournamentID', type=int, required=True, help="Tournament id cannot be blank")
    parser.add_argument('clubID', type=int, required=True,help="Club id cannot be blank.")
    parser.add_argument('playerID', type=int, required=True,help="Player id cannot be blank.")
    parser.add_argument('number', type=int, required=False)

    def post(self): # create a squad row
        data = self.parser.parse_args()
        if not data['number']:  # number cannot be blank for registration
            return {'message':'Player kit number cannot be blank!'},400
        squad = SquadModel.find_by_tournament_club_player(data['tournamentID'],data['clubID'],data['playerID'])
        if squad:
            return {'message':'player already exists in squad!'},400
        if not SquadModel.is_number_available(data['tournamentID'],data['clubID'],data['number']):
            return {'message':'player with number {} already exists in squad!'.format(data['number'])},400
        try:
            squad = SquadModel(**data)
            squad.save_to_db()
            if FireBase.add_player_to_tournament_chat(data['playerID'],data['clubID'],data['tournamentID']):
                return { "squad": squad.json()}, 201
            else:
                squad.delete_from_db()
                return { "message": "Squad creation failed due to error while adding player to rounament chat."}, 500
        except:
            traceback.print_exc()
            return {'message':'Internal server error, squad registration failed!'},500

    def delete(self): # delete a squad row
        data = self.parser.parse_args()
        squad = SquadModel.find_player(data['tournamentID'],data['clubID'],data['playerID'])
        if not squad:
            return {'message':'player not found!'},404
        try:
            if FireBase.remove_player_from_tournament_chat(data['playerID'],data['clubID'],data['tournamentID']):
                squad.delete_from_db()
                return {'message':'player deleted!'},200
            return {'message':'Squad deletion failed due to cannot unsubscribe player from tournament chat!'},500
        except:
            traceback.print_exc()
            return {'message':'Internal server error, squad deletion failed!'},500

    def put(self): # update a squad row
        data = self.parser.parse_args()
        squad = SquadModel.find_by_tournament_club_player(data['tournamentID'],data['clubID'],data['playerID'])
        if not squad:
            return {'message':'player not found!'},404
        try:
            if data['number']:
                squad.number = data['number']
            squad.save_to_db()
            return squad.json(),200
        except:
            traceback.print_exc()
            return {'message':'Internal server error, squad update failed!'},500


class SquadByClub(Resource):
    # tid,cid,pid,number

    def get(self,tournamentID,clubID):
        squad = []
        info = {
            "playerID" : 0,
            "displayName" : None,
            "number" : 0,
            "role" : None,
        }
        for squadPlayer in SquadModel.find_tournament_club_squad(tournamentID,clubID):
            player = PlayerModel.find_by_id(squadPlayer.playerID)
            if player:
                info["playerID"] = player.id
                info["displayName"] = player.displayName
                info["number"] = squadPlayer.number
                info["role"] = player.role
                squad.append(info.copy())
            else:
                traceback.print_exc()
                return {'message':'Internal server error, retrieve squad failed!'},500
        return {'squad':squad},200


class SquadTotal(Resource):
    # tid,cid,pid,number

    def get(self):
        return {'squad':[player.json() for player in SquadModel.find_all()]},200
