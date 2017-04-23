from models.player import PlayerModel
from models.club import ClubModel
from models.squad import SquadModel
from models.result import ResultModel

class GamePerformance:

    # return None if something is wrong
    @classmethod
    def calculate_performance(cls,results,clubID):
        gamePerformance = {
                "win" : 0,
                "draw" : 0,
                "loss" : 0,
                "cleanSheet" : 0,
                "goalsConceded" : 0,
        }
        try:
            for result in results:
                isHome = False
                if result.homeID == int(clubID):
                    isHome = True

                finalScore = result.penScore    # try pk shootout score

                if not finalScore:  # no pk shootout, try extra-time scores
                    finalScore = result.extraScore

                    if not finalScore:  # no extra time, use fulltime score
                        finalScore = result.ftScore
                        # use fulltime score to decide cleanSheet
                        ftScores = result.ftScore.split(":")
                        if isHome:
                            if int(ftScores[1]) == 0:
                                gamePerformance['cleanSheet'] += 1
                            else:
                                gamePerformance['goalsConceded'] += int(ftScores[1])
                        else:
                            if int(ftScores[0]) == 0:
                                gamePerformance['cleanSheet'] += 1
                            else:
                                gamePerformance['goalsConceded'] += int(ftScores[0])

                    else:   # game decided by extra time
                        # use extra time score to decide cleanSheet, goalsConceded
                        extraScores = result.extraScore.split(":")
                        if isHome:
                            if int(extraScores[1]) == 0:
                                gamePerformance['cleanSheet'] += 1
                            else:
                                gamePerformance['goalsConceded'] += int(extraScores[1])
                        else:
                            if int(extraScores[0]) == 0:
                                gamePerformance['cleanSheet'] += 1
                            else:
                                gamePerformance['goalsConceded'] += int(extraScores[0])

                else:   # game decided by pk shootout
                    # use extra time score to decide cleanSheet, goalsConceded
                    extraScores = result.extraScore.split(":")
                    if isHome:
                        if int(extraScores[1]) == 0:
                            gamePerformance['cleanSheet'] += 1
                        else:
                            gamePerformance['goalsConceded'] += int(extraScores[1])
                    else:
                        if int(extraScores[0]) == 0:
                            gamePerformance['cleanSheet'] += 1
                        else:
                            gamePerformance['goalsConceded'] += int(extraScores[0])

                scores = finalScore.split(":")
                if isHome:
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
                print('result: {}'.format(finalScore))
            print('cleansheet:{}'.format(gamePerformance['cleanSheet']))
            return gamePerformance
        except:
            return None

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
            results = ResultModel.find_club_tournament_result(tourID, clubID)
            tournamentPerformance = cls.calculate_performance(results,clubID)
            if tournamentPerformance:
                gamePerformance['win'] += tournamentPerformance['win']
                gamePerformance['draw'] += tournamentPerformance['draw']
                gamePerformance['loss'] += tournamentPerformance['loss']
            else:
                return None
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
            results = ResultModel.find_club_tournament_result(tourID, clubID)
            tournamentPerformance = cls.calculate_performance(results,clubID)
            if tournamentPerformance:
                gamePerformance['win'] += tournamentPerformance['win']
                gamePerformance['draw'] += tournamentPerformance['draw']
                gamePerformance['loss'] += tournamentPerformance['loss']
            else:
                return None
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
            results = ResultModel.find_club_tournament_result(tournamentID, clubID)
            tournamentPerformance = cls.calculate_performance(results,clubID)
            if tournamentPerformance:
                gamePerformance['win'] += tournamentPerformance['win']
                gamePerformance['draw'] += tournamentPerformance['draw']
                gamePerformance['loss'] += tournamentPerformance['loss']
            else:
                return None
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
                "cleanSheet" : 0,
                "goalsConceded" : 0,
        }

        results = ResultModel.find_by_club(clubID)
        tournamentPerformance = cls.calculate_performance(results,clubID)
        if tournamentPerformance:
            gamePerformance['win'] += tournamentPerformance['win']
            gamePerformance['draw'] += tournamentPerformance['draw']
            gamePerformance['loss'] += tournamentPerformance['loss']
            gamePerformance['cleanSheet'] += tournamentPerformance['cleanSheet']
            gamePerformance['goalsConceded'] += tournamentPerformance['goalsConceded']
        else:
            return None
        return gamePerformance

    @classmethod
    def get_club_tournament_performance(cls,tournamentID,clubID):
        # try to locate club
        club = ClubModel.find_by_id(clubID)
        if not club:
            return None

        gamePerformance = {
                "win" : 0,
                "draw" : 0,
                "loss" : 0,
                "cleanSheet" : 0,
                "goalsConceded" : 0,
        }

        results = ResultModel.find_club_tournament_result(tournamentID,clubID)
        tournamentPerformance = cls.calculate_performance(results,clubID)
        if tournamentPerformance:
            gamePerformance['win'] += tournamentPerformance['win']
            gamePerformance['draw'] += tournamentPerformance['draw']
            gamePerformance['loss'] += tournamentPerformance['loss']
            gamePerformance['cleanSheet'] += tournamentPerformance['cleanSheet']
            gamePerformance['goalsConceded'] += tournamentPerformance['goalsConceded']
        else:
            return None
        return gamePerformance
