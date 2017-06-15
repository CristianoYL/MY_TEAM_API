import traceback
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from datetime import date
from db import db

from models.player import PlayerModel
from models.member import MemberModel

class PlayerByEmail(Resource):
    #(id INTEGERPRIMARY KEY, email text, firstName text, lastName text, displayName text, age int, height real, weight real, phone text, leftFooted boolean, avatar int)
    parser = reqparse.RequestParser()
    parser.add_argument('role', type=str, required=True,help="The player's role cannot be blank.")
    parser.add_argument('firstName', type=str, required=True, help="The player's firtname cannot be blank.")
    parser.add_argument('lastName', type=str, required=True, help="The player's lastname cannot be blank.")
    parser.add_argument('displayName', type=str, required=False)
    parser.add_argument('age', type=int, required=False)
    parser.add_argument('height',type=float, required=False)
    parser.add_argument('weight',type=float, required=False)
    parser.add_argument('phone', type=str, required=False)
    parser.add_argument('leftFooted', type=bool, required=False)
    parser.add_argument('avatar', type=int, required=False)

    def get(self,email):
        player = PlayerModel.find_by_email(email)
        if player:
            return player.json(), 200

        return {'message': 'player not found'}, 404

    def post(self,email):     #create player
        player = PlayerModel.find_by_email(email)  # check if already exists
        if player:
            return {'message': 'player <{}> already exists'.format(email)}, 400
        # if not exist, proceed to create
        data = self.parser.parse_args()
        if not data['displayName']:
            data['displayName'] = data['firstName'] + ' ' + data['lastName']
        player = PlayerModel(None,email,**data)
        try:        # try to insert
            player.save_to_db()
        except:
            traceback.print_exc()
            return {'message':'Internal server error, player creation failed.'},500

        return player.json(),201 # echo the created player info

    def delete(self,email):     #delete player
        player = PlayerModel.find_by_email(email)  # check if already exists
        if player is None:
            return {'message': "player <{}> doesn't exist".format(email)}, 404
        # if exists, proceed to delete
        try:        # try to delete
            player.delete_from_db()
        except:
            traceback.print_exc()
            return {'message':'Internal server error, player deletion failed.'},500

        return {'message':'player deleted successfully!'.format(email)},200

    def put(self,email):     #update player
        data = self.parser.parse_args()
        is_new_player = False

        player = PlayerModel.find_by_email(email)  # check if already exists

        if player is None:  # if player doesn't exist
            player = PlayerModel(None,email,**data)    # create a player first
            is_new_player = True
        else:
            player.role = data['role']
            player.firstName = data['firstName']
            player.lastName = data['lastName']
            if data['displayName']:
                player.displayName = data['displayName']
            if data['age']:
                player.age = data['age']
            if data['height']:
                player.height = data['height']
            if data['weight']:
                player.weight = data['weight']
            if data['phone']:
                player.phone = data['phone']
            if data['leftFooted'] is not None:
                player.leftFooted = data['leftFooted']
            if data['avatar']:
                player.avatar = data['avatar']
        try:
            player.save_to_db()
        except:
            traceback.print_exc()
            return {'message':'Internal server error.'},500

        if is_new_player:
            return player.json(),201
        else:
            return player.json(),200


class PlayerByID(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('role', type=str, required=True,help="The player's role cannot be blank.")
    parser.add_argument('firstName', type=str, required=True, help="The player's firtname cannot be blank.")
    parser.add_argument('lastName', type=str, required=True, help="The player's lastname cannot be blank.")
    parser.add_argument('displayName', type=str, required=False)
    parser.add_argument('age', type=int, required=False)
    parser.add_argument('height',type=float, required=False)
    parser.add_argument('weight',type=float, required=False)
    parser.add_argument('phone', type=str, required=False)
    parser.add_argument('leftFooted', type=bool, required=False)
    parser.add_argument('avatar', type=int, required=False)

    def get(self,playerID):
        player = PlayerModel.find_by_id(playerID)
        if player:
            return player.json(), 200

        return {'message': 'player not found'}, 404

    def delete(self,playerID):     #delete player
        player = PlayerModel.find_by_id(playerID)  # check if already exists
        if player is None:
            return {'message': "player <id:{}> doesn't exist".format(playerID)}, 404
        # if exists, proceed to delete
        try:        # try to delete
            player.delete_from_db()
        except:
            traceback.print_exc()
            return {'message':'Internal server error, player deletion failed.'},500

        return {'message':'player <id:{}> deleted successfully!'.format(playerID)},200

    def put(self,playerID):     #update player
        data = self.parser.parse_args()
        is_new_player = False

        player = PlayerModel.find_by_id(playerID)  # check if already exists

        if player is None:  # if player doesn't exist
            player = PlayerModel(playerID,**data)    # create a player first
            is_new_player = True
        else:
            player.role = data['role']
            player.firstName = data['firstName']
            player.lastName = data['lastName']
            if data['displayName']:
                player.displayName = data['displayName']
            if data['age']:
                player.age = data['age']
            if data['height']:
                player.height = data['height']
            if data['weight']:
                player.weight = data['weight']
            if data['phone']:
                player.phone = data['phone']
            if data['leftFooted'] is not None:
                player.leftFooted = data['leftFooted']
            if data['avatar']:
                player.avatar = data['avatar']
        try:
            player.save_to_db()
        except:
            traceback.print_exc()
            return {'message':'Internal server error.'},500

        if is_new_player:
            return player.json(),201
        else:
            return player.json(),200


class PlayerList(Resource):
    def get(self):
        return {'players':[player.json() for player in PlayerModel.find_all()]}, 200
        # return {'players':list(map(lambda x: x.json(), PlayerModel.find_all()))}


class PlayerRegistration(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstName', type=str, required=True,help="The player's firstname cannot be blank.")
    parser.add_argument('lastName', type=str, required=True,help="The player's lastname cannot be blank.")
    parser.add_argument('displayName', type=str, required=True, help="The player's display name cannot be blank.")
    parser.add_argument('role', type=str, required=True,help="The player's role cannot be blank.")
    parser.add_argument('age', type=int, required=False)
    parser.add_argument('height',type=float, required=False)
    parser.add_argument('weight',type=float, required=False)
    parser.add_argument('phone', type=str, required=False)
    parser.add_argument('leftFooted', type=bool, required=False)
    parser.add_argument('avatar', type=int, required=False)

    def post(self,clubID): # create a new player in this club
        data = self.parser.parse_args()

        # check full name
        playersWithSameFullName = PlayerModel.find_by_fullname(data['firstName'],data['lastName'])
        if playersWithSameFullName.first(): # if players with same full name exists
            #   return these players to client and let them decide what to do next
            return {
                "players":[player.json() for player in playersWithSameFullName],
                "message" : "players with same full name already exist"}, 400

        player = PlayerModel(None,None,**data)
        # try to create player
        try:
            player.save_to_db()
        except:
            traceback.print_exc()
            return {'message':'Internal server error! Failed to create player'},500
        # player creation successful, try to create member
        try:
            current_date = date.today()
            member = MemberModel(clubID,player.id,current_date,True,1)
            member.save_to_db()
            # member creation also successful, return response
            return {
                'player' : player.json(),
                'member' : member.json()
                }, 201
        except: # member creation failed
            traceback.print_exc()
            db.session.rollback()
        # try to roll back, delete the just created player
        print("try to roll back, delete player")
        try:
            player.delete_from_db()
        except: # roll back error, failed to delete the just created player
            traceback.print_exc()
            return {'message':'Internal server error! Roll back error!.'},500
        # roll back successfully
        return {'message':'Internal server error! Failed to add player into club member.'},500

    def put(self,clubID):   # force to create a new player in this club, ignore full name redundancy
        data = self.parser.parse_args()
        player = PlayerModel(None,None,**data)
        try:
            player.save_to_db()
            try:
                current_date = date.today()
                member = MemberModel(clubID,player.id,current_date,True,1)
                member.save_to_db()
                return {
                    'player' : player.json(),
                    'member' : member.json()
                    }, 201
            except:
                try:
                    db.session.rollback()
                    player.delete_from_db()
                except:
                    traceback.print_exc()
                    return {'message':'Internal server error! Roll back error!.'},500
                traceback.print_exc()
                return {'message':'Internal server error! Failed to add player into club member.'},500
        except:
            traceback.print_exc()
            return {'message':'Internal server error! Failed to create player'},500
