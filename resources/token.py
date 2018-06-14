import traceback
from flask_restful import Resource, reqparse

from models.token import TokenModel
from models.player import PlayerModel


class Token(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('instanceToken', type=str, required=True, help="This field cannot be blank.")

    @classmethod
    def get(cls, playerID):  # get token by playerID
        if playerID == 0:  # get all tokens
            return {"tokens": [token.json() for token in TokenModel.find_all()]}, 200
        # else get specified player token
        token = TokenModel.find_token_by_player_id(playerID)
        if token:  # if token already exists, means it's an update
            return {"token": token.json()}, 200
        return {"message": "token not found."}, 404

    def put(self, playerID):  # create or update a token
        data = self.parser.parse_args()
        player = PlayerModel.find_by_id(playerID)
        if not player:  # if player not found
            return {"message": "Player with ID:{} not found.".format(playerID)}, 404
        # else player found
        token = TokenModel.find_token_by_player_id(playerID)
        if token:  # if token already exists, means it's an update
            token.instanceToken = data["instanceToken"]
            try:
                token.save_to_db()
                return {"token": token.json()}, 200
            except:
                traceback.print_exc()
                return {"message": "Internal server error, failed to update token."}, 500
        # else token doesn't exist, then create a new token
        token = TokenModel(None, playerID, **data)
        try:
            token.save_to_db()
            return {"token": token.json()}, 201
        except:
            traceback.print_exc()
            return {"message": "Internal server error, failed to create token."}, 500

    def delete(self, playerID):  # delete an existing token
        token = TokenModel.find_token_by_player_id(playerID)
        if token:  # if token exists, try to delete it
            try:
                token.delete_from_db()
                return {"message": "token deleted!"}, 200
            except:
                traceback.print_exc()
                return {"token": "Internal server error, failed to delete token."}, 500
        # else token not found
        return {"token": "Token for player <ID:{}> not found.".format(playerID)}, 404
