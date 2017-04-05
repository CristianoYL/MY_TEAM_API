import traceback
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

from models.squad import SquadModel

class Squad(Resource):
    # tid,cid,pid,number,isAdmin
    parser = reqparse.RequestParser()
    parser.add_argument('tournamentID', type=int, required=True, help="Tournament id cannot be blank")
    parser.add_argument('clubID', type=int, required=True,help="Club id cannot be blank.")
    parser.add_argument('playerID', type=int, required=True,help="Player id cannot be blank.")
    parser.add_argument('number', type=int, required=False)
    parser.add_argument('isAdmin', type=bool, required=False)

    def post(self): # create a squad row
        data = self.parser.parse_args()
        if not data['number']:  # number cannot be blank for registration
            return {'message':'Player kit number cannot be blank!'},400
        squad = SquadModel.find_player(data['tournamentID'],data['clubID'],data['playerID'])
        if squad:
            return {'message':'player already exists in squad!'},400
        if not SquadModel.is_number_available(data['tournamentID'],data['clubID'],data['number']):
            return {'message':'player with number {} already exists in squad!'.format(data['number'])},400
        try:
            if not data['isAdmin']:
                data['isAdmin'] = False
            squad = SquadModel(**data)
            squad.save_to_db()
            return squad.json(),201
        except:
            traceback.print_exc()
            return {'message':'Internal server error, squad registration failed!'},500

    def delete(self): # delete a squad row
        data = self.parser.parse_args()
        squad = SquadModel.find_player(data['tournamentID'],data['clubID'],data['playerID'])
        if not squad:
            return {'message':'player not found!'},404
        try:
            squad.delete_from_db()
            return {'message':'player deleted!'},200
        except:
            traceback.print_exc()
            return {'message':'Internal server error, squad deletion failed!'},500

    def put(self): # update a squad row
        data = self.parser.parse_args()
        squad = SquadModel.find_player(data['tournamentID'],data['clubID'],data['playerID'])
        if not squad:
            return {'message':'player not found!'},404
        try:
            if data['number']:
                squad.number = data['number']
            if data['isAdmin']:
                squad.isAdmin = data['isAdmin']
            squad.save_to_db()
            return squad.json(),200
        except:
            traceback.print_exc()
            return {'message':'Internal server error, squad update failed!'},500


class SquadPlayer(Resource):
    # tid,cid,pid,number,isAdmin

    def get(self,tournamentID,clubID):
        return {'squad':[player.json() for player in SquadModel.find_tournament_club_squad(tournamentID,clubID)]},200


class SquadTotal(Resource):
    # tid,cid,pid,number,isAdmin

    def get(self):
        return {'squad':[player.json() for player in SquadModel.find_all()]},200