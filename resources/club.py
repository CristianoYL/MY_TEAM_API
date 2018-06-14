import traceback
from flask_restful import Resource,reqparse
from datetime import date

from models.club import ClubModel
from models.member import MemberModel
from utils.firebase import FireBase

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
        clubs = ClubModel.find_by_name_fuzzy(name)
        return {'clubs':[club.json() for club in clubs]}, 200


class Club(Resource):
    # (id,name,info)
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,help="Club name cannot be blank.")
    parser.add_argument('info', type=str, required=True, help="Please add some description about this club.")

    def post(self): # create a club
        data = self.parser.parse_args()

        clubs = ClubModel.find_by_name(data['name'])

        if clubs.first():   # if clubs with same name exists, let the user know
            return {
            "message" : "Club creation failed. Club with name <{}> already exists".format(data['name']),
            'clubs' : [club.json() for club in clubs]
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

    def post(self,playerID): # player creates a club
        data = self.parser.parse_args()

        clubs = ClubModel.find_by_name(data['name'])

        if clubs.first():
            return {
            "message" : "Club creation failed. Club with name <{}> already exists".format(data['name']),
            "clubs" : [club.json() for club in clubs]
            }, 400

        club = ClubModel(None,data['name'],data['info'])

        try:
            club.save_to_db()
            try:
                current_date = date.today()
                # priority=3 means leader
                member = MemberModel(club.id,playerID,current_date,True,3)
                member.save_to_db()
            except: # if member creation failed, delete this club
                club.delete_from_db()
                traceback.print_exc()
                return {"message":"Internal server error, club member creation failed."}, 500
        except:
            traceback.print_exc()
            return {"message":"Internal server error, club creation failed."}, 500

        if FireBase.add_player_to_club_chat(playerID,club.id):
            return club.json() ,201   # echo the created club info
        try:
            member.delete_from_db()
            club.delete_from_db()
            return {"message":"Internal server error, fail to add player to club chat, roll back..."}, 500
        except:
            traceback.print_exc()
            return {"message":"Internal server error, fail to add player to club chat, roll back error"}, 500
