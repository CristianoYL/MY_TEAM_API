from flask_restful import Resource

from models.squad import SquadModel
from models.club import ClubModel
from models.teamsheet import TeamsheetModel
from models.tournament import TournamentModel
from functions.performance import GamePerformance


class ClubInfoByID(Resource):
    def get(self, clubID):
        clubInfo = {
            "club" : None,
            "tournaments" : [],
            "teamsheet" : [],
            "gamePerformance":{
                "win" : 0,
                "draw" : 0,
                "loss" : 0,
            }
        }

        # get club basic info
        club = ClubModel.find_by_id(clubID)
        if not club:
            return {"message" : "Club not found"}, 404

        clubInfo["club"] = club.json()

        # get tournaments attended by retrieving & iterating through squads
        tours = set()   # store all distinct tournament IDs

        allPastSquads =  SquadModel.find_by_club_id(clubID)
        for squad in allPastSquads:
            tours.add(squad.tournamentID)

        for tourID in tours:
            # use tournamentID to locate tournament
            tournament = TournamentModel.find_by_id(tourID)
            if not tournament:
                return {"message": "Tournament not found"}, 404
            clubInfo["tournaments"].append(tournament.json())

        # get teamsheet
        clubInfo["teamsheet"] = [teamsheet.json() for teamsheet in TeamsheetModel.find_by_club(clubID)]

        gamePerformance = GamePerformance.get_club_total_performance(clubID)
        if gamePerformance:
            clubInfo["gamePerformance"] = gamePerformance

        return {"clubInfo" : clubInfo},200
