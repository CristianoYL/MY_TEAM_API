from models.player import PlayerModel
from models.club import ClubModel
from models.squad import SquadModel
from models.result import ResultModel

class GamePerformance:

    @classmethod
    def get_player_total_performance(cls,playerID):
        # try to locate player
        player = PlayerModel.find_by_id(playerID)
        if not player:
            return None

        gamePerformance = {
                "win" : 0,
                "draw" : 0,
                "loss" : 0,
        }

        # try to find all squads that player is in
        playerSquad = SquadModel.find_by_player_id(playerID)

        for squad in playerSquad:
            tourID = squad.tournamentID
            clubID = squad.clubID
            # try to find all result for each squad the player is in
            for result in ResultModel.find_club_tournament_result(tourID, clubID):
                # analyze the game result
                finalScore = result.penScore
                if not finalScore:
                    finalScore = result.extraScore
                    if not finalScore:
                        finalScore = result.ftScore

                if not finalScore:
                    return {"message" : "Internal server error"}, 500

                scores = finalScore.split(":")
                if result.homeID == clubID:
                    selfScore = scores[0]
                    opponentScore = scores[1]
                else:
                    selfScore = scores[1]
                    opponentScore = scores[0]

                if selfScore > opponentScore:
                    gamePerformance["win"] += 1
                elif selfScore < opponentScore:
                    gamePerformance["loss"] += 1
                else:
                    gamePerformance["draw"] += 1
        return gamePerformance


    @classmethod
    def get_player_club_performance(cls,clubID,playerID):
        # try to locate player
        player = PlayerModel.find_by_id(playerID)
        if not player:
            return None

        gamePerformance = {
                "win" : 0,
                "draw" : 0,
                "loss" : 0,
        }

        # try to find all squads that player is in
        playerSquad = SquadModel.find_by_club_player(clubID,playerID)

        for squad in playerSquad:
            tourID = squad.tournamentID
            # try to find all result for each squad the player is in
            for result in ResultModel.find_club_tournament_result(tourID, clubID):
                # analyze the game result
                finalScore = result.penScore
                if not finalScore:
                    finalScore = result.extraScore
                    if not finalScore:
                        finalScore = result.ftScore

                if not finalScore:
                    return {"message" : "Internal server error"}, 500

                scores = finalScore.split(":")
                if result.homeID == clubID:
                    selfScore = scores[0]
                    opponentScore = scores[1]
                else:
                    selfScore = scores[1]
                    opponentScore = scores[0]

                if selfScore > opponentScore:
                    gamePerformance["win"] += 1
                elif selfScore < opponentScore:
                    gamePerformance["loss"] += 1
                else:
                    gamePerformance["draw"] += 1
        return gamePerformance


    @classmethod
    def get_player_tournament_performance(cls,tournamentID,clubID,playerID):
        # try to locate player
        player = PlayerModel.find_by_id(playerID)
        if not player:
            return None

        gamePerformance = {
                "win" : 0,
                "draw" : 0,
                "loss" : 0,
        }

        # try to see if player has signed up for this tournament
        squad = SquadModel.find_by_tournament_club_player(tournamentID,clubID,playerID)

        if squad:
            # try to find all result for the player's club in this tournament
            for result in ResultModel.find_club_tournament_result(tournamentID, clubID):
                # analyze the game result
                finalScore = result.penScore
                if not finalScore:
                    finalScore = result.extraScore
                    if not finalScore:
                        finalScore = result.ftScore

                if not finalScore:
                    return {"message" : "Internal server error"}, 500

                scores = finalScore.split(":")
                if result.homeID == clubID:
                    selfScore = scores[0]
                    opponentScore = scores[1]
                else:
                    selfScore = scores[1]
                    opponentScore = scores[0]

                if selfScore > opponentScore:
                    gamePerformance["win"] += 1
                elif selfScore < opponentScore:
                    gamePerformance["loss"] += 1
                else:
                    gamePerformance["draw"] += 1
        return gamePerformance


    @classmethod
    def get_club_total_performance(cls,clubID):
        # try to locate club
        club = ClubModel.find_by_id(clubID)
        if not club:
            return None

        gamePerformance = {
                "win" : 0,
                "draw" : 0,
                "loss" : 0,
        }

        for result in ResultModel.find_by_club(clubID):
            # analyze the game result
            finalScore = result.penScore
            if not finalScore:
                finalScore = result.extraScore
                if not finalScore:
                    finalScore = result.ftScore

            if not finalScore:
                return {"message" : "Internal server error"}, 500

            scores = finalScore.split(":")
            if result.homeID == clubID:
                selfScore = scores[0]
                opponentScore = scores[1]
            else:
                selfScore = scores[1]
                opponentScore = scores[0]

            if selfScore > opponentScore:
                gamePerformance["win"] += 1
            elif selfScore < opponentScore:
                gamePerformance["loss"] += 1
            else:
                gamePerformance["draw"] += 1
        return gamePerformance
