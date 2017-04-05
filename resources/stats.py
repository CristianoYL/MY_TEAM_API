import traceback
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

from models.stats import StatsModel

class Stats(Resource):
    # (tournamentID, playerID, attendence, appearance, start, goal,
    #   penalty, penaltyShootout, penaltyTaken, ownGoal, header, assist, yellow,
    #   red, cleanSheet, penaltySaved)
    parser = reqparse.RequestParser()
    parser.add_argument('attendence', type=int, required=True, help="This field cannot be blank.")
    parser.add_argument('appearance', type=int, required=True, help="This field cannot be blank.")
    parser.add_argument('start', type=int, required=True, help="This field cannot be blank.")
    parser.add_argument('goal', type=int, required=True, help="This field cannot be blank.")
    parser.add_argument('penalty', type=int, required=True, help="This field cannot be blank.")
    parser.add_argument('penaltyShootout', type=int, required=True, help="This field cannot be blank.")
    parser.add_argument('penaltyTaken', type=int, required=True, help="This field cannot be blank.")
    parser.add_argument('ownGoal', type=int, required=True, help="This field cannot be blank.")
    parser.add_argument('header', type=int, required=True, help="This field cannot be blank.")
    parser.add_argument('assist', type=int, required=True, help="This field cannot be blank.")
    parser.add_argument('yellow', type=int, required=True, help="This field cannot be blank.")
    parser.add_argument('red', type=int, required=True, help="This field cannot be blank.")
    parser.add_argument('cleanSheet', type=int, required=True, help="This field cannot be blank.")
    parser.add_argument('penaltySaved', type=int, required=True, help="This field cannot be blank.")

    def get(self,tournamentID,playerID):  # get stats
        stats = StatsModel.find_player_tournament_stats(tournamentID,playerID)
        if stats:
            return stats.json(), 200
        return {'message' : 'stats not found.'}, 404

    def post(self,tournamentID,playerID): # create a new stats
        stats = StatsModel.find_stats(tournamentID,playerID)
        if stats:
            return {'message' : 'stats already exists.'}, 400
        stats = StatsModel(tournamentID,playerID,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        try:
            stats.save_to_db()
            return stats.json(), 201
        except:
            traceback.print_exc()
            return {'message' : 'Internal server error, create stats failed.'}, 500

    def delete(self,tournamentID,playerID): # delete a stats
        stats = StatsModel.find_stats(tournamentID,playerID)
        if not stats:
            return {'message' : 'stats not found.'}, 404
        try:
            stats.delete_from_db()
            return {'message' : 'stats deleted.'}, 200
        except:
            traceback.print_exc()
            return {'message' : 'Internal server error, delete stats failed.'}, 500

    def put(self,tournamentID,playerID):  # update an existing stats
        stats = StatsModel.find_stats(tournamentID,playerID)
        data = self.parser.parse_args()

        if not stats:
            return {'message' : 'stats not found'}, 404

        vector = StatsModel(tournamentID,playerID,**data)
        new_stats = StatsModel.get_updated_stats(stats,vector)

        try:
            new_stats.save_to_db()
            return new_stats.json(), 200
        except:
            traceback.print_exc()
            return {'message' : 'Internal server error, update stats failed.'}, 500


class StatsList(Resource):

    def get(self):
        return {'stats':[stats.json() for stats in StatsModel.find_all()]},200