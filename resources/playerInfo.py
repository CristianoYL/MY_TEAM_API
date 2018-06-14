import traceback

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.player import PlayerModel
from models.member import MemberModel
from models.stats import StatsModel
from models.tournament import TournamentModel
from models.squad import SquadModel
from models.club import ClubModel
from utils.performance import GamePerformance


class PlayerInfoByID(Resource):
    @classmethod
    def get(cls, playerID):  # get player info by playerID
        player = PlayerModel.find_by_id(playerID)
        if not player:
            return {'message': 'Player info not found'}, 404

        members = MemberModel.find_by_player(playerID)
        if not members:
            return {'message': 'Player member info not found'}, 404
        clubs = []
        for member in members:
            club = ClubModel.find_by_id(member.clubID)
            if not club:
                return {'message': 'Player club info not found'}, 404
            club_info = club.json();
            club_info["priority"] = member.priority
            clubs.append(club_info)

        totalStats = StatsModel.find_player_total_stats(playerID)
        if not totalStats:
            return {'message': 'Player stats info not found'}, 404

        gamePerformance = GamePerformance.get_player_total_performance(playerID)

        if not gamePerformance:
            gamePerformance = {
                "win": 0,
                "draw": 0,
                "loss": 0,
            }

        playerInfo = {
            "player": player.json(),
            "clubs": clubs,
            "totalStats": totalStats,
            "gamePerformance": gamePerformance,
        }

        return playerInfo, 200


class PlayerInfoByToken(Resource):

    @classmethod
    @jwt_required()
    def get(cls):  # get player info by jwt
        user_id = get_jwt_identity()
        player = PlayerModel.find_by_user(user_id)
        if not player:
            return {'message': 'Player info not found'}, 404

        playerID = player.id
        return PlayerInfoByID.get(playerID)


class PlayerClubInfo(Resource):
    @classmethod
    def get(cls, clubID, playerID):  # get player's club stats, performance, and tournaments
        try:
            playerStats = {
                'stats': StatsModel.find_club_player_stats(clubID, playerID),
                'gamePerformance': {
                    "win": 0,
                    "draw": 0,
                    "loss": 0,
                },
                'tournaments': []
            }
            gamePerformance = GamePerformance.get_player_club_performance(clubID, playerID)
            if gamePerformance:
                playerStats['gamePerformance'] = gamePerformance

            squads = SquadModel.find_by_club_player(clubID, playerID)

            tournaments = []
            for squad in squads:
                tournament = TournamentModel.find_by_id(squad.tournamentID)
                if tournament:
                    tournaments.append(tournament.json())
                else:
                    return {'message': 'Internal server error! Failed to retrieve player tournament info'}, 500
            playerStats['tournaments'] = tournaments
            return playerStats, 200
        except:
            traceback.print_exc()
            return {'message': 'Internal Server Error. Cannot load player club stats.'}, 500
