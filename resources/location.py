import traceback
from flask_restful import Resource, reqparse
from datetime import datetime

from models.location import LocationModel


class Location(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('latitude', type=str, required=True, help="This field cannot be null")
    parser.add_argument('longitude', type=str, required=True, help="This field cannot be null")

    # get locaton
    def get(self, clubID, playerID):
        location = LocationModel.find_location(clubID, playerID)
        if location:
            return {"location": location.json()}, 200
        else:
            return {"message": "player location info not found."}, 404

    # update locaton
    def put(self, clubID, playerID):
        data = self.parser.parse_args()
        current_time = datetime.utcnow()

        location = LocationModel.find_location(clubID, playerID)
        if location:  # if history data exists
            location.lastUpdate = current_time
            location.latitude = data["latitude"]
            location.longitude = data["longitude"]
            try:  # try to update existing data
                location.save_to_db()
                return {"location": location.json()}, 200
            except:
                traceback.print_exc()
                return {"message": "Server error when updating location data."}, 500

        # else no history data exists
        location = LocationModel(clubID, playerID, data["latitude"], data["longitude"], current_time)
        try:
            location.save_to_db()
        except:
            traceback.print_exc()
            return {"message": "Server error when saving location data."}, 500
        return {"location": location.json()}, 201

    # delete locaton
    def delete(self, clubID, playerID):
        location = LocationModel.find_location(clubID, playerID)
        if location:
            try:
                location.delete_from_db()
                return {"message": "location deleted."}, 200
            except:
                traceback.print_exc()
                return {"message": "Sever error when deleting location"}, 500
        else:
            return {"message": "player location info not found."}, 404


class LocationByClub(Resource):

    # get locaton
    def get(self, clubID):
        all_locations = LocationModel.find_all_club_players_location(clubID)
        location_list = []
        for location in all_locations:
            location_list.append(location.json())

        return {"location": location_list}, 200
