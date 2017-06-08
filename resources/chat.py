import traceback
from flask_restful import Resource,reqparse

from models.player import PlayerModel
from models.chat import ChatModel
from datetime import datetime

class TournamentChat(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('senderID', type=int, required=True,help="The sender ID cannot be null")
    parser.add_argument('messageType', type=str)
    parser.add_argument('messageContent', type=str, required=True,help="The message content cannot be null")

    # post club tournament chat
    def post(self,tournamentID,clubID):
        data = self.parser.parse_args()
        data['time'] = datetime.utcnow()
        # (id, tournamentID, clubID, receiverID, senderID, messageType, messageContent, time)
        chat = ChatModel(None,tournamentID,clubID,None,**data)
        try:
            chat.save_to_db()
        except:
            traceback.print_exc()
            return {'message':'failed to store chat message'},500
        return {'chat':chat.json()},201


class ClubChat(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('senderID', type=int, required=True,help="The sender ID cannot be null")
    parser.add_argument('messageType', type=str)
    parser.add_argument('messageContent', type=str, required=True,help="The message content cannot be null")

    # post club chat
    def post(self,clubID):
        data = self.parser.parse_args()
        data['time'] = datetime.utcnow()
        # (id, tournamentID, clubID, receiverID, senderID, messageType, messageContent, time)
        chat = ChatModel(None,None,clubID,None,**data)
        try:
            chat.save_to_db()
        except:
            traceback.print_exc()
            return {'message':'failed to store chat message'},500
        return {'chat':chat.json()},201


class PrivateChat(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('senderID', type=int, required=True,help="The sender ID cannot be null")
    parser.add_argument('messageType', type=str)
    parser.add_argument('messageContent', type=str, required=True,help="The message content cannot be null")

    # post private chat
    def post(self,receiverID):
        data = self.parser.parse_args()
        data['time'] = datetime.utcnow()
        # (id, tournamentID, clubID, receiverID, senderID, messageType, messageContent, time)
        chat = ChatModel(None,None,None,receiverID,**data)
        try:
            chat.save_to_db()
        except:
            traceback.print_exc()
            return {'message':'failed to store chat message'},500
        return {'chat':chat.json()},201


class Chat(Resource):

    def get(self,tournamentID,clubID,receiverID,senderID,limit,offset):

        if tournamentID is not None and tournamentID != 0:  # tournamentID specified
            if clubID is not None and clubID != 0:  # clubID specified
                #find the club tournament chat
                print("find tour chat!")
                tournament_chat = ChatModel.find_tournament_chat(tournamentID,clubID,limit,offset)
                return { "chat" : [chat.json() for chat in tournament_chat] }, 200
            # else: clubID unspecified
            return { "message" : "club ID unspecified!" }, 400

        # else: tournamentID not specified
        if clubID is not None and clubID != 0:  # clubID specified
            # find the club chat
            print("find club chat!")
            club_chat = ChatModel.find_club_chat(clubID,limit,offset)
            return { "chat" : [chat.json() for chat in club_chat] }, 200

        # else: clubID unspecified
        if receiverID is not None and receiverID != 0:  # receiverID specified
            if senderID is not None and senderID != 0:  # senderID specified
                print("find private chat!")
                private_chat = ChatModel.find_private_chat(receiverID,senderID,limit,offset)
                return { "chat" : [chat.json() for chat in private_chat] }, 200
            # else: senderID unspecified
            return { "message" : "sender ID unspecified!" }, 400

        # else: receiverID unspecified
        return { "message" : "receiver ID unspecified!" }, 400


class ChatManager(Resource):

    def delete(self,id):
        chat = ChatModel.find_by_id(id)
        if chat is None:
            return {"message" : "Chat <id:{}> not found".format(id)}, 404

        try:
            chat.delete_from_db()
        except:
            traceback.print_exc()
            return {"message" : "Delete chat <id:{}> failed!".format(id)}, 500
        return {"message" : "Chat <id:{}> deleted!".format(id)}, 200
