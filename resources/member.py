import traceback
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from datetime import date,datetime

from models.member import MemberModel
from models.club import ClubModel
from models.player import PlayerModel

class Member(Resource):
    # (clubID,playerID,memberSince)
    parser = reqparse.RequestParser()
    parser.add_argument('memberSince', type=str, required=False)
    parser.add_argument('priority', type=int, required=False)
    parser.add_argument('isActive', type=bool, required=False)

    def get(self,clubID,playerID):
        data = self.parser.parse_args()
        member = MemberModel.find_club_player(clubID,playerID)
        if member:
            return member.json(), 200
        return {"message":"Member not found"}, 404

    def post(self,clubID,playerID): # create new club member
        data = self.parser.parse_args()
        member = MemberModel.find_club_player(clubID,playerID)
        if member:
            return {"message":"Member already exists"}, 400
        # else try to create new member
        try:
            # if no date specified, use today's date
            memberSince = date.today()
            if data['memberSince']:
                try:
                    memberSince = datetime.strptime(data['memberSince'], '%Y-%m-%d')
                except ValueError:
                    return { "message": "Incorrect data format, should be YYYY-MM-DD"} ,400
            # new member is active by default
            if data['isActive'] is None:
                data['isActive'] = True

            # member is regular member (priority=1) by default
            if data['priority'] is None:
                data['priority'] = 1
            member = MemberModel(clubID,playerID,memberSince,data['isActive'],data['priority'])
            member.save_to_db()
            return member.json() ,201
        except:
            traceback.print_exc()
            return { "message": "Internal server error, create club member failed."} ,500

    def delete(self,clubID,playerID):
        data = self.parser.parse_args()
        member = MemberModel.find_club_player(clubID,playerID)
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
        member = MemberModel.find_club_player(clubID,playerID)
        if member:
            try:
                if data['memberSince']:
                    try:
                        member.memberSince = datetime.strptime(data['memberSince'], '%Y-%m-%d')
                    except ValueError:
                        return { "message": "Incorrect data format, should be YYYY-MM-DD"} ,400

                if data['isActive'] is not None:
                    member.isActive = data['isActive']

                if data['priority'] is not None:
                    member.priority = data['priority']

                member.save_to_db()
                return member.json() ,200
            except:
                traceback.print_exc()
                return { "message": "Internal server error, club member update failed."} ,500
        return {"message":"Member not found"}, 404


class MemberByPlayer(Resource):

    def get(self,playerID): # get player's all club member info
        members = MemberModel.find_by_player(playerID)
        member_list = []
        for member in members:
            club = ClubModel.find_by_id(member.clubID)
            if club is None:
                return {"message" : "Error when finding player club"},500
            member_list.append({
                "club" : club.json(),
                "member" : member.json()
            })
        return {"members" : member_list},200


class MemberByClub(Resource):
    # (clubID,playerID,memberSince,number,isActive)
    parser = reqparse.RequestParser()
    parser.add_argument('isActive', type=bool, required=False)

    def get(self,clubID):   # get club's all player and member info
        data = self.parser.parse_args()
        # check if only want to find active players
        if data['isActive']:
            members = MemberModel.find_club_active_player(clubID)
        else:
            members = MemberModel.find_by_club(clubID)

        member_list = []
        for member in members:
            player = PlayerModel.find_by_id(member.playerID)
            if player:
                member_list.append({
                    "player" : player.json(),
                    "member" : member.json()
                })
        return {"members" : member_list},200


class MemberList(Resource):
    # (clubID,playerID,memberSince,number,isActive)
    def get(self):
        teams = MemberModel.find_all()
        return {'members':[member.json() for member in teams]},200


class MemberRequest(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('playerID', type=int, required=True, help="This field cannot be empty")
    def post(self,clubID):  # request to join club
        data = self.parser.parse_args()
        member = MemberModel.find_club_player(clubID,data["playerID"])
        if member:
            if member.priority > 0:
                return {"message":"You are already a member in this club!"}, 400
            else:
                return {"message":"Request already sent, please wait for club admins to process request."}, 400

        # else try to create new member
        try:
            # use today's date
            data["memberSince"] = date.today()
            # new member is active by default
            data['isActive'] = True
            # priority = 0 means applicant
            data['priority'] = 0
            member = MemberModel(clubID,**data)
            member.save_to_db()
            return { "member" : member.json() }, 201
        except:
            traceback.print_exc()
            return { "message": "Internal server error, create club member failed."} ,500
