import traceback
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from datetime import date

from models.club import ClubModel
from models.teamsheet import TeamsheetModel

class ClubByID(Resource):
    # (id,name,info)
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=False)
    parser.add_argument('info', type=str, required=False)

    def get(self,_id):
        club = ClubModel.find_by_id(_id)
        if club:
            return club.json(), 200
        return {"message":"Club not found"}, 404

    def delete(self, _id):
        club = ClubModel.find_by_id(_id)
        if club:
            try:
                club.delete_from_db()
                return { "message": "Club deleted."} ,200
            except:
                traceback.print_exc()
                return { "message": "Internal server error, club deletion failed."} ,500
        return {"message":"Club not found"}, 404

    def put(self, _id): # update existing club
        club = ClubModel.find_by_id(_id)
        if club:
            try:
                data = self.parser.parse_args()
                club.name = data['name']
                club.info = data['info']
                club.save_to_db()
                return club.json(), 200
            except:
                traceback.print_exc()
                return { "message": "Internal server error, club info update failed."} ,500
        return {"message":"Club not found"}, 404


class ClubByName(Resource):
    # (id,name,info)

    def get(self,name):
        clubs = ClubModel.find_by_name(name)
        return {'clubs':[club.json() for club in clubs]}, 200


class Club(Resource):
    # (id,name,info)
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,help="Club name cannot be blank.")
    parser.add_argument('info', type=str, required=True, help="Please add some description about this club.")

    def post(self): # create a club
        data = self.parser.parse_args()

        club = ClubModel.find_by_name(data['name'])

        if club:
            return {
            "message":"Club creation failed. Club with name <{}> already exists".format(data['name'])
            }, 400

        club = ClubModel(None,**data)

        try:
            club.save_to_db()
        except:
            traceback.print_exc()
            return {"message":"Internal server error, club creation failed."}, 500
        return club.json() ,201   # echo the created club info

    def get(self):  # get all clubs
        return { "clubs": [club.json() for club in ClubModel.find_all()]}, 200


class ClubRegistration(Resource):
    # (id,name,info)
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,help="Club name cannot be blank.")
    parser.add_argument('info', type=str, required=True, help="Please add some description about this club.")
    parser.add_argument('playerID', type=int, required=True, help="Please include player's ID when creating a club")

    def post(self): # create a club
        data = self.parser.parse_args()

        club = ClubModel.find_by_name(data['name'])

        if club:
            return {
            "message":"Club creation failed. Club with name <{}> already exists".format(data['name'])
            }, 400

        club = ClubModel(None,data['name'],data['info'])

        try:
            club.save_to_db()
            current_date = date.today()
            teamsheet = TeamsheetModel(club.id,data['playerID'],current_date,0,True)
            teamsheet.save_to_db()
        except:
            traceback.print_exc()
            return {"message":"Internal server error, club creation failed."}, 500
        return club.json() ,201   # echo the created club info
