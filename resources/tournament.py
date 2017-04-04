import traceback
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

from models.tournament import TournamentModel

class TournamentByID(Resource):
    # (id,name,info)
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=False)
    parser.add_argument('info', type=str, required=False)

    def get(self,_id):
        tournament = TournamentModel.find_by_id(_id)
        if tournament:
            return tournament.json(), 200
        return {"message":"Tournament not found"}, 404

    def delete(self, _id):
        tournament = TournamentModel.find_by_id(_id)
        if tournament:
            try:
                tournament.delete_from_db()
                return { "message": "tournament deleted."} ,200
            except:
                traceback.print_exc()
                return { "message": "Internal server error, tournament deletion failed."} ,500
        return {"message":"tournament not found"}, 404

    def put(self, _id): # update existing club
        tournament = TournamentModel.find_by_id(_id)
        if tournament:
            try:
                data = self.parser.parse_args()
                tournament.name = data['name']
                tournament.info = data['info']
                tournament.save_to_db()
                return tournament.json(), 200
            except:
                traceback.print_exc()
                return { "message": "Internal server error, tournament info update failed."} ,500
        return {"message":"tournament not found"}, 404


class TournamentByName(Resource):
    # (id,name,info)

    def get(self,name):
        tournaments = TournamentModel.find_by_name(name)
        return {'tournaments':[tournament.json() for tournament in tournaments]}, 200


class Tournament(Resource):
    # (id,name,info)
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,help="Club name cannot be blank.")
    parser.add_argument('info', type=str, required=True, help="Please add some description about this club.")

    def post(self): # create a tournament
        data = self.parser.parse_args()
        tournament = TournamentModel(None,**data)

        try:
            tournament.save_to_db()
        except:
            traceback.print_exc()
            return {"message":"Internal server error, tournament creation failed."}, 500
        return { "message": tournament.json()} ,201   # echo the created tournament info

    def get(self):  # get all tournaments
        return { "tournaments": [tournament.json() for tournament in TournamentModel.find_all()]}, 200
