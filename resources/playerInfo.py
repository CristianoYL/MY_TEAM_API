from flask_restful import Resource


from models.player import PlayerModel
from models.teamsheet import TeamsheetModel
from models.stats import StatsModel

class PlayerInfo(Resource):
    def get(self, playerID):    # 
        if not PlayerModel.find_by_id(playerID):
            return {'message': 'Player info not found'}, 404

        if not TeamsheetModel.find_by_player(playerID):
            return {'message': 'Player club info not found'}, 404

        if not  StatsModel.find_player_total_stats(playerID):
            return {'message': 'Player stats info not found'}, 404

        playerInfo = {
                "player" : PlayerModel.find_by_id(playerID).json(),
                "clubs" : [res.json() for res in TeamsheetModel.find_by_player(playerID)],
                "totalStats" : StatsModel.find_player_total_stats(playerID)
                }

        return { "playerInfo" : playerInfo }, 200
