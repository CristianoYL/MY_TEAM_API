import traceback
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from datetime import date,datetime

from models.teamsheet import TeamsheetModel

class Teamsheet(Resource):
    # (clubID,playerID,memberSince)
    parser = reqparse.RequestParser()
    parser.add_argument('memberSince', type=str, required=False)
    parser.add_argument('number', type=int, required=False)
    parser.add_argument('isActive', type=bool, required=False)

    def get(self,clubID,playerID):
        data = self.parser.parse_args()
        member = TeamsheetModel.find_club_player(clubID,playerID)
        if member:
            return member.json(), 200
        return {"message":"Member not found"}, 404

    def post(self,clubID,playerID): # create new club member
        data = self.parser.parse_args()
        member = TeamsheetModel.find_club_player(clubID,playerID)
        if not member:
            try:
                memberSince = date.today()
                if data['memberSince']:
                    try:
                        memberSince = datetime.strptime(data['memberSince'], '%Y-%m-%d')
                    except ValueError:
                        return { "message": "Incorrect data format, should be YYYY-MM-DD"} ,400
                if not data['isActive']:
                    data['isActive'] = True
                member = TeamsheetModel(clubID,playerID,memberSince,data['number'],data['isActive'])
                member.save_to_db()
                return member.json() ,201
            except:
                traceback.print_exc()
                return { "message": "Internal server error, create club member failed."} ,500
        return {"message":"Member already exists"}, 404

    def delete(self,clubID,playerID):
        data = self.parser.parse_args()
        member = TeamsheetModel.find_club_player(clubID,playerID)
        if member:
            try:
                member.delete_from_db()
                return { "message": "Club member deleted."} ,200
            except:
                traceback.print_exc()
                return { "message": "Internal server error, club member deletion failed."} ,500
        return {"message":"Member not found"}, 404

    def put(self,clubID,playerID): # update existing club member
        data = self.parser.parse_args()
        member = TeamsheetModel.find_club_player(clubID,playerID)
        if member:
            try:
                if data['memberSince']:
                    try:
                        member.memberSince = datetime.strptime(data['memberSince'], '%Y-%m-%d')
                    except ValueError:
                        return { "message": "Incorrect data format, should be YYYY-MM-DD"} ,400
                if data['number']:
                    member.number = data['number']
                if data['isActive']:
                    member.isActive = data['isActive']
                member.save_to_db()
                return member.json() ,200
            except:
                traceback.print_exc()
                return { "message": "Internal server error, club member update failed."} ,500
        return {"message":"Member not found"}, 404


class TeamsheetByPlayer(Resource):
    # (clubID,playerID,memberSince,number,isActive)
    def get(self,playerID):
        teams = TeamsheetModel.find_by_player(playerID)
        return {'teamsheet':[teamsheet.json() for teamsheet in teams]},200


class TeamsheetByClub(Resource):
    # (clubID,playerID,memberSince,number,isActive)
    parser = reqparse.RequestParser()
    parser.add_argument('isActive', type=bool, required=False)
    def get(self,clubID):
        data = self.parser.parse_args()
        if data['isActive'] and data['isActive'] == True:
            teams = TeamsheetModel.find_club_active_player(clubID)
        else:
            teams = TeamsheetModel.find_by_club(clubID)
        return {'teamsheet':[teamsheet.json() for teamsheet in teams]},200
