import traceback
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

from models.tournament import TournamentModel
from models.squad import SquadModel
from models.stats import StatsModel

class TournamentByID(Resource):
    # (id,name,info)
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=False)
    parser.add_argument('info', type=str, required=False)

    def get(self,_id):
        tournament = TournamentModel.find_by_id(_id)
        if tournament:
            return tournament.json(), 200
        return {"message":"Tournament not found"}, 404

    def delete(self, _id):
        tournament = TournamentModel.find_by_id(_id)
        if tournament:
            try:
                tournament.delete_from_db()
                return { "message": "tournament deleted."} ,200
            except:
                traceback.print_exc()
                return { "message": "Internal server error, tournament deletion failed."} ,500
        return {"message":"tournament not found"}, 404

    def put(self, _id): # update existing club
        tournament = TournamentModel.find_by_id(_id)
        if tournament:
            try:
                data = self.parser.parse_args()
                tournament.name = data['name']
                tournament.info = data['info']
                tournament.save_to_db()
                return tournament.json(), 200
            except:
                traceback.print_exc()
                return { "message": "Internal server error, tournament info update failed."} ,500
        return {"message":"tournament not found"}, 404


class TournamentByName(Resource):
    # (id,name,info)

    def get(self,name):
        tournaments = TournamentModel.find_by_name(name)
        return {'tournaments':[tournament.json() for tournament in tournaments]}, 200


class Tournament(Resource):
    # (id,name,info)
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,help="Club name cannot be blank.")
    parser.add_argument('info', type=str, required=True, help="Please add some description about this club.")
    parser.add_argument('clubID', type=int, required=False)

    def post(self): # create a tournament
        data = self.parser.parse_args()

        tournament = TournamentModel.find_by_name(data['name'])
        if tournament:
            return {"message":"Tournament <{}> already exists".format(data['name'])}, 400

        tournament = TournamentModel(None,data['name'],data['info'])
        try:
            tournament.save_to_db()

        except:
            traceback.print_exc()
            return {"message":"Internal server error, tournament creation failed."}, 500
        return { "message": tournament.json()} ,201   # echo the created tournament info

    def get(self):  # get all tournaments
        return { "tournaments": [tournament.json() for tournament in TournamentModel.find_all()]}, 200


class TournamentByClub(Resource):
    # (id,name,info)

    def get(self,clubID):   # get club's all participating tournaments
        tournamentList = TournamentModel.find_by_club(clubID)
        return {'tournaments':tournamentList}, 200


class TournamentRegistration(Resource):
    # (id,name,info)
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,help="Club name cannot be blank.")
    parser.add_argument('info', type=str, required=True, help="Please add some description about this club.")

    def post(self,clubID,playerID): # create a tournament
        data = self.parser.parse_args()

        # step 1: create tournament
        tournaments = TournamentModel.find_by_name(data['name'])
        if tournaments.first(): # if tournament with same name exists, let the user know
            return {
                "message" : "Tournament <{}> already exists".format(data['name']),
                "tournaments" : [tournament.json() for tournament in tournaments]
                }, 400

        tournament = TournamentModel(None,data['name'],data['info'])
        try:    # save tournament
            tournament.save_to_db()
        except:
            traceback.print_exc()
            return {"message":"Internal server error! Tournament creation failed."}, 500

        # step 2: create squad
        squad = SquadModel.find_by_tournament_club_player(tournament.id,clubID,playerID)

        if squad:   # roll back
            try:    # delete tournament as well
                tournament.delete_from_db()
                traceback.print_exc()
                return {"message" : "Internal server error! Squad info already exists."}, 400
            except:
                traceback.print_exc()
                return {"message" : "Internal server error! Roll back error."}, 500

        try:    # create squad
            squad = SquadModel(tournament.id,clubID,playerID,0)
            squad.save_to_db()
        except: # if create squad failed, roll back
            try:    # delete tournament as well
                tournament.delete_from_db()
                traceback.print_exc()
                return {"message" : "Internal server error! Failed to create squad info."}, 500
            except:
                traceback.print_exc()
                return {"message" : "Internal server error! Roll back error."}, 500

        # step 3: create stats:
        stats = StatsModel.find_stats(tournament.id,clubID,playerID)
        if stats: # roll back
            try:    # delete tournament and squad as well
                tournament.delete_from_db()
                squad.delete_from_db
                traceback.print_exc()
                return {"message" : "Internal server error! Stats info already exists."}, 400
            except:
                traceback.print_exc()
                return {"message" : "Internal server error! Roll back error."}, 500

        try: # create stats
            stats = StatsModel(tournament.id, clubID, playerID, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
            stats.save_to_db()
        except: # roll back
            try:    # delete tournament as well
                tournament.delete_from_db()
                squad.delete_from_db
                traceback.print_exc()
                return {"message" : "Internal server error! Failed to create stats info."}, 500
            except:
                traceback.print_exc()
                return {"message" : "Internal server error! Roll back error."}, 500

        return {
            "message" : "Tournament and Squad created!",
            "tournament" : tournament.json(),
            "squad" : squad.json(),
            "stats" : stats.json()
            }, 201
