import traceback
import json
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from datetime import datetime

from models.result import ResultModel
from models.club import ClubModel
from models.tournament import TournamentModel
from models.stats import StatsModel

class Result(Resource):
    # (id,homeID,awayID,tournamentID,date,stage,ftScore,extraScore,penScore,info,homeEvents,awayEvents)
    parser = reqparse.RequestParser()
    parser.add_argument('homeID', type=int, required=True,help="The homeID cannot be blank.")
    parser.add_argument('awayID', type=int, required=True,help="The awayID cannot be blank.")
    parser.add_argument('tournamentID', type=int, required=True,help="The tournament cannot be blank.")
    parser.add_argument('date', type=str, required=True,help="The date cannot be blank.")
    parser.add_argument('stage', type=str, required=False)
    parser.add_argument('ftScore', type=str, required=False)
    parser.add_argument('extraScore', type=str, required=False)
    parser.add_argument('penScore', type=str, required=False)
    parser.add_argument('info', type=str, required=False)
    parser.add_argument('homeEvents', type=dict,required=False,action='append')
    parser.add_argument('awayEvents', type=dict,required=False,action='append')

    def get(self): # get all results
        return {'results':[result.json() for result in ResultModel.find_all()]}, 200

    def post(self):     #create result
        data = self.parser.parse_args()
        print(data['homeEvents'])
        if not data['ftScore']:
            return {'message' : 'The fulltime score cannot be blank.'},400
        # try to parse the date
        try:
            data['date'] = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError:
            return { "message": "Incorrect data format, should be YYYY-MM-DD"} ,400

        homeClub = ClubModel.find_by_id(data["homeID"])
        if not homeClub:
            return { "message": "Home club not found"} ,404
        homeName = homeClub.name

        awayClub = ClubModel.find_by_id(data["awayID"])
        if not awayClub:
            return { "message": "Away club not found"} ,404
        awayName = awayClub.name

        tournament = TournamentModel.find_by_id(data["tournamentID"])
        tournamentName = tournament.name

        data["homeName"] = homeName
        data["awayName"] = awayName
        data["tournamentName"] = tournamentName

        unique_keys = {
            'tournamentID' : data['tournamentID'],
            'homeID' : data['homeID'],
            'awayID' : data['awayID'],
            'date' : data['date'],
            'stage' : data['stage'],
        }
        # check if already exists
        result = ResultModel.find_by_tournament_home_away_date_stage(**unique_keys)
        if result:
            return {'message': 'result already exists'}, 400

        # if not exist, proceed to create
        data['homeEvents'] = json.dumps(data['homeEvents'])
        data['awayEvents'] = json.dumps(data['awayEvents'])
        print('homeEvents:')
        print(data['homeEvents'])
        result = ResultModel(None,**data)
        try:        # try to insert
            result.save_to_db()
            return result.json(),201 # echo the created result
        except:
            traceback.print_exc()
            return {'message':'Internal server error, upload result failed.'},500

    def delete(self):     #delete player
        data = self.parser.parse_args()
        # try to parse the date
        try:
            data['date'] = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError:
            return { "message": "Incorrect data format, should be YYYY-MM-DD"} ,400

        unique_keys = {
            'tournamentID' : data['tournamentID'],
            'homeID' : data['homeID'],
            'awayID' : data['awayID'],
            'date' : data['date'],
            'stage' : data['stage'],
        }
        # check if exists
        result = ResultModel.find_by_tournament_home_away_date_stage(**unique_keys)
        if result is None:
            return {'message': "game result doesn't exist"}, 404

        # if exists, proceed to delete
        try:        # try to delete
            result.delete_from_db()
            return {'message':'game deleted successfully!'},200
        except:
            traceback.print_exc()
            return {'message':'Internal server error, result deletion failed.'},500

    def put(self):     #update result
        data = self.parser.parse_args()
        # try to parse the date
        try:
            data['date'] = datetime.strptime(data['date'], '%Y-%m-%d')
        except ValueError:
            return { "message": "Incorrect data format, should be YYYY-MM-DD"} ,400

        unique_keys = {
            'tournamentID' : data['tournamentID'],
            'homeID' : data['homeID'],
            'awayID' : data['awayID'],
            'date' : data['date'],
            'stage' : data['stage'],
        }
        # check if already exists
        result = ResultModel.find_by_tournament_home_away_date_stage(**unique_keys)
        if not result:
            return {'message': "result doesn't exists"}, 404

        # if exist, proceed to update
        try:        # try to insert
            if data['ftScore']:
                result.ftScore = data['ftScore']
            if data['extraScore']:
                result.extraScore = data['extraScore']
            if data['penScore']:
                result.penScore = data['penScore']
            if data['info']:
                result.info = data['info']
            if data['homeEvents']:
                result.homeEvents = data['homeEvents']
            if data['awayEvents']:
                result.awayEvents = data['awayEvents']
            result.save_to_db()
            return result.json(),200 # echo the updated result
        except:
            traceback.print_exc()
            return {'message':'Internal server error, result update failed.'},500


class ResultByClub(Resource):
    def get(self,clubID): # get club's results
        return {'results':[result.json() for result in ResultModel.find_by_club(clubID)]}, 200


class ResultByHome(Resource):
    def get(self, clubID): #get team results for all home game
        return {"results" : [result.json() for result in ResultModel.find_by_home(clubID)]}, 200


class ResultByAway(Resource):
    def get(self, clubID): #get team results for all home game
        return {"results" : [result.json() for result in ResultModel.find_by_away(clubID)]}, 200


class ResultByTournamentClub(Resource):
    def get(self,tournamentID,clubID): # get club's results
        return {'results':[result.json() for result in ResultModel.find_club_tournament_result(tournamentID,clubID)]}, 200

    def post(self,tournamentID,clubID): # post new game result and update player stats
        parser = reqparse.RequestParser()
        parser.add_argument('homeID', type=int, required=False)
        parser.add_argument('awayID', type=int, required=False)
        parser.add_argument('homeName', type=str, required=False)
        parser.add_argument('awayName', type=str, required=False)
        parser.add_argument('tournamentName', type=str, required=False)
        parser.add_argument('date', type=str, required=True,help="The date cannot be blank.")
        parser.add_argument('stage', type=str, required=False)
        parser.add_argument('ftScore', type=str, required=False)
        parser.add_argument('extraScore', type=str, required=False)
        parser.add_argument('penScore', type=str, required=False)
        parser.add_argument('info', type=str, required=False)
        parser.add_argument('homeEvents', type=dict,required=False,action='append')
        parser.add_argument('awayEvents', type=dict,required=False,action='append')
        parser.add_argument('stats', type=dict,required=True,action='append')

        data = parser.parse_args()

        try:
            data['date'] = datetime.strptime(data['date'], '%Y-%m-%d')
        except ValueError:
            return { "message": "Incorrect data format, should be YYYY-MM-DD"} ,400

        if data['homeID'] == 0:
            data['homeID'] = None
        if data['awayID'] == 0:
            data['awayID'] = None
        unique_keys = {
            'tournamentID' : tournamentID,
            'homeID' : data['homeID'],
            'awayID' : data['awayID'],
            'date' : data['date'],
            'stage' : data['stage'],
        }
        # check if already exists
        result = ResultModel.find_by_tournament_home_away_date_stage(**unique_keys)
        if result:
            return {'message': 'result already exists'}, 400

        # if not exist, proceed to create
        data['homeEvents'] = json.dumps(data['homeEvents'])
        data['awayEvents'] = json.dumps(data['awayEvents'])
        print('home events:')
        print(data['homeEvents'])
        print('away events:')
        print(data['awayEvents'])

        result_params = {
            "homeID" : data['homeID'],
            "awayID" : data['awayID'],
            "tournamentID" : tournamentID,
            "homeName" : data['homeName'],
            "awayName" : data['awayName'],
            "tournamentName" : data['tournamentName'],
            "date" : data['date'],
            "stage" : data['stage'],
            "ftScore" : data['ftScore'],
            "extraScore": data['extraScore'],
            "penScore" : data['penScore'],
            "info" : data['info'],
            "homeEvents" : data['homeEvents'],
            "awayEvents" : data['awayEvents']
        }

        result = ResultModel(None,**result_params)

        response = {
            'result' : result.json(),
            'stats' : []
        }

        try:        # try to insert
            result.save_to_db()
        except:
            traceback.print_exc()
            return {'message':'Internal server error, upload result failed.'},500

        for stats in data['stats']:
            vector = StatsModel(**stats)
            previous_stats = StatsModel.find_stats(tournamentID,clubID,stats['playerID'])
            if not previous_stats:
                return {'message':'Internal server error, failed to locate player <id:{}> stats'.format(stats["playerID"])},500

            updated_stats = StatsModel.get_updated_stats(previous_stats,vector)

            try:
                updated_stats.save_to_db()
                response['stats'].append(updated_stats.json())
            except:
                return {'message':'Internal server error, upload stats failed.'},500

        return response,201 # echo the created result
