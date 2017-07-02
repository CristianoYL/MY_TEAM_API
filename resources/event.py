import traceback
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from datetime import date,datetime

from models.event import EventModel
from models.club import ClubModel

class Event(Resource):
    # (id,clubID,eventTitle,eventAddress,latitude,longitude,eventTime)
    parser = reqparse.RequestParser()
    parser.add_argument('clubID', type=int, required=True,help='ClubID not specified.')
    parser.add_argument('eventTitle', type=str, required=True)
    parser.add_argument('eventAddress', type=str, required=True)
    parser.add_argument('latitude', type=str, required=True)
    parser.add_argument('longitude', type=str, required=True)
    parser.add_argument('eventTime', type=str, required=True)

    datetime_format = '%Y-%m-%d %H:%M:%S'

    def get(self):   # find all events
        return {'events':[event.json() for event in EventModel.find_all()]},200

    def post(self):   # find event by id
        data = self.parser.parse_args()
        # try to parse datetime str into datetime object
        try:
            eventTime = datetime.strptime(data['eventTime'],self.datetime_format)
        except ValueError:
            return {
                "message": "Incorrect datetime format, should be YYYY-MM-DD HH:mm:ss"
                } ,400
        data['eventTime'] = eventTime
        event = EventModel(None,**data)
        try:
            event.save_to_db()
        except:
            traceback.print_exc()
            return {"message": "Internal server error, failed to create event"},500
        return event.json(),201


class EventByID(Resource):
    # (id,clubID,eventTitle,eventAddress,latitude,longitude,eventTime)
    parser = reqparse.RequestParser()
    parser.add_argument('eventTitle', type=str, required=False)
    parser.add_argument('eventAddress', type=str, required=False)
    parser.add_argument('latitude', type=str, required=False)
    parser.add_argument('longitude', type=str, required=False)
    parser.add_argument('eventTime', type=str, required=False)

    datetime_format = '%Y-%m-%d %H:%M:%S'
    def get(self,id):   # find event by id
        event = EventModel.find_by_id(id)
        if not event:
            return {'message': 'Event not found.'},404
        return event.json(),200

    def put(self,id): # update existing event
        event = EventModel.find_by_id(id)
        if not event:
            return {'message': 'Event not found.'},404
        # else update the event with given params
        data = self.parser.parse_args()
        if data['eventTitle']:
            event.eventTitle = data['eventTitle']
        if data['eventAddress']:
            event.eventAddress = data['eventAddress']
        if data['latitude']:
            event.latitude = data['latitude']
        if data['longitude']:
            event.longitude = data['longitude']
        if data['eventTime']:
            # try to parse datetime str into datetime object
            try:
                eventTime = datetime.strptime(data['eventTime'],self.datetime_format)
            except ValueError:
                return {
                    "message": "Incorrect datetime format, should be YYYY-MM-DD HH:mm:ss"
                    } ,400
            event.eventTime = eventTime
        try:
            event.save_to_db()
        except:
            traceback.print_exc()
            return {"message": "Internal server error, failed to update event"},500
        return event.json(),200

    def delete(self,id):   # delete event by id
        event = EventModel.find_by_id(id)
        if not event:
            return {'message': 'Event not found.'},404
        try:
            event.delete_from_db()
        except:
            traceback.print_exc()
            return {'message':'Internal server error, failed to delete event.'},500
        return {'message':'Event deleted!'},200


class EventByClub(Resource):

    datetime_format = '%Y-%m-%d %H:%M:%S'
    def get(self,clubID):   # find all events of given Club
        if not ClubModel.find_by_id(clubID):
            return {'message': 'Club not found.'},404
        return {'events':[event.json() for event in EventModel.find_club_events(clubID)]},200
