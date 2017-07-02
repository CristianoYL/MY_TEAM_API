from db import db

class EventModel(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    clubID = db.Column(db.Integer, db.ForeignKey('club.id'))
    eventTitle = db.Column(db.String(100))
    eventAddress = db.Column(db.String(200))
    latitude = db.Column(db.String(50))
    longitude = db.Column(db.String(50))
    eventTime = db.Column(db.DateTime)

    def __init__(self,_id,clubID,eventTitle,eventAddress,latitude,longitude,eventTime):
        self.id = _id
        self.clubID = clubID
        self.eventTitle = eventTitle
        self.eventAddress = eventAddress
        self.latitude = latitude
        self.longitude = longitude
        self.eventTime = eventTime

    def json(self):
        return {
            "id" : self.id,
            "clubID" : self.clubID,
            "eventTitle" : self.eventTitle,
            "eventAddress" : self.eventAddress,
            "latitude" : self.latitude,
            "longitude" : self.longitude,
            "eventTime" : self.eventTime.isoformat()
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_club_events(cls,clubID):
        return cls.query.filter_by(clubID=clubID).order_by(cls.eventTime.desc())

    @classmethod
    def find_by_time_slot(cls,after,before):
        return cls.query.filter(cls.eventTime.between(after,before)).order_by(cls.eventTime.desc())

    def save_to_db(self):   ## upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):   ## delete
        db.session.delete(self)
        db.session.commit()
