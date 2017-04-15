from flask_restful import Resource


from models.player import PlayerModel
from models.teamsheet import TeamsheetModel
from models.stats import StatsModel
from models.result import ResultModel
from models.squad import SquadModel
from models.club import ClubModel

class PlayerInfoByID(Resource):
    def get(self, playerID):    # get player info by playerID
        player = PlayerModel.find_by_id(playerID)
        if not player:
            return {'message': 'Player info not found'}, 404

        teamsheets = TeamsheetModel.find_by_player(playerID)
        if not teamsheets:
            return {'message': 'Player teamsheet info not found'}, 404
        clubs = []
        for teamsheet in teamsheets:
            club = ClubModel.find_by_id(teamsheet.clubID)
            if not club:
                return {'message': 'Player club info not found'}, 404
            clubs.append(club.json())

        totalStats = StatsModel.find_player_total_stats(playerID)
        if not totalStats:
            return {'message': 'Player stats info not found'}, 404

        gamePerformance = {
                "win" : 0,
                "draw" : 0,
                "loss" : 0,
        }

        playerSquad = SquadModel.find_by_player_id(playerID)
        if not playerSquad:
            return {'message': 'Player squad info not found'}, 404

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
                "player" : player.json(),
                "clubs" : clubs,
                "totalStats" : totalStats,
                "gamePerformance" : gamePerformance,
                }

        return playerInfo, 200


class PlayerInfoByEmail(Resource):
    def get(self, email):    # get player info by email
        player = PlayerModel.find_by_email(email)
        if not player:
            return {'message': 'Player info not found'}, 404

        playerID = player.id

        teamsheets = TeamsheetModel.find_by_player(playerID)
        if not teamsheets:
            return {'message': 'Player teamsheet info not found'}, 404

        clubs = []
        for teamsheet in teamsheets:
            club = ClubModel.find_by_id(teamsheet.clubID)
            if not club:
                return {'message': 'Player club info not found'}, 404
            clubs.append(club.json())

        totalStats = StatsModel.find_player_total_stats(playerID)
        if not totalStats:
            return {'message': 'Player stats info not found'}, 404

        gamePerformance = {
                "win" : 0,
                "draw" : 0,
                "loss" : 0,
        }

        playerSquad = SquadModel.find_by_player_id(playerID)
        if not playerSquad:
            return {'message': 'Player squad info not found'}, 404

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
                "player" : player.json(),
                "clubs" : clubs,
                "totalStats" : totalStats,
                "gamePerformance" : gamePerformance,
                }

        return playerInfo, 200
