import traceback
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from datetime import datetime

from models.result import ResultModel
from models.club import ClubModel
from models.tournament import TournamentModel

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
    parser.add_argument('homeEvents', type=str, required=False)
    parser.add_argument('awayEvents', type=str, required=False)

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
        homeName = homeClub.name

        awayClub = ClubModel.find_by_id(data["awayID"])
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
    # (id,home,awayID,tournamentID,date,stage,ftScore,extraScore,penScore,info)

<<<<<<< HEAD
    def get(self,clubID): # get club's results
        return {'results':[result.json() for result in ResultModel.find_by_club(clubID)]}, 200
=======
    def get(self,clubID): # get team's results
        return {"results" : [result.json() for result in ResultModel.find_by_club(clubID)]}, 200

class ResultByHome(Resource):
    def get(self, clubID): #get team results for all home game
        return {"results" : [result.json() for result in ResultModel.find_by_home(clubID)]}, 200

class ResultByAway(Resource):
    def get(self, clubID): #get team results for all home game
        return {"results" : [result.json() for result in ResultModel.find_by_away(clubID)]}, 200
>>>>>>> 3f6b9ac5e50a68554b4ccb79bfab8f97520f1f95
