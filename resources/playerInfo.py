from flask_restful import Resource


from models.player import PlayerModel
from models.teamsheet import TeamsheetModel
from models.stats import StatsModel

class PlayerInfo(Resource):
    def get(self, playerID):
        errorMsg = {'message': 'Player doest not exist'}
        if not PlayerModel.find_by_id(playerID):
            return errorMsg, 404
        if not TeamsheetModel.find_by_player(playerID):
            return errorMsg, 404
        if not  Stats.model.find_player_total_stats(playerID):
            return errorMsg, 404
        playerSelfInfo = {"player" : PlayerModel.find_by_id(playerID).json()}
        clubInfo = {"clubs" : [res.json() for res in TeamsheetModel.find_by_player(playerID)]}
        statsInfo = {"totalStats" : Stats.model.find_player_total_stats(playerID)}

        return {"playerInfo" : [playerSelfInfo, clubInfo, statsInfo]}
