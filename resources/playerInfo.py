from flask_restful import Resource


from models.player import PlayerModel
from models.teamsheet import TeamsheetModel
from models.stats import StatsModel
from models.result import ResultModel
from models.squad import SquadModel

class PlayerInfo(Resource):
    def get(self, playerID):
        if not PlayerModel.find_by_id(playerID):
            return {'message': 'Player info not found'}, 404

        if not TeamsheetModel.find_by_player(playerID):
            return {'message': 'Player club info not found'}, 404

        if not StatsModel.find_player_total_stats(playerID):
            return {'message': 'Player stats info not found'}, 404

        if not SquadModel.find_by_player_id(playerID):
            return {'message': 'Player squad info not found'}, 404

        gamePerformance = {
                "win" : 0,
                "draw" : 0,
                "loss" : 0,
        }

        playerSquad = SquadModel.find_by_player_id(playerID)
        if not playerSquad:
            return {'message': 'Player squad info not found'}, 404

        gamePerformance = {
                "win" : 0,
                "draw" : 0,
                "loss" : 0,
        }

        for squad in playerSquad:
            tourID = squad.tournamentID
            clubID = squad.clubID
            for result in ResultModel.find_club_tournament_result(tourID, clubID):
                finalScore = result.penScore
                if not finalScore:
                    finalScore = result.extraScore
                    if not extraScore:
                        finalScore = result.ftScore

                if not finalScore:
                    return {"message" : "Internal server error"}, 500

                scores = finalScore.split(":")
                if scores[0] > scores[1]:
                    gamePerformance["win"] += 1
                elif scores[0] < scores[1]:
                    gamePerformance["loss"] += 1
                else:
                    gamePerformance["draw"] += 1



        playerInfo = {
                "player" : PlayerModel.find_by_id(playerID).json(),
                "clubs" : [res.json() for res in TeamsheetModel.find_by_player(playerID)],
                "totalStats" : StatsModel.find_player_total_stats(playerID),
                "gamePerformance" : gamePerformance,
                }

        return { "playerInfo" : playerInfo }, 200
