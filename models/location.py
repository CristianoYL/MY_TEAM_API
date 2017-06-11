from db import db

class LocationModel(db.Model):
    __tablename__ = 'location'

    clubID = db.Column(db.Integer, db.ForeignKey('club.id'), primary_key=True)
    playerID = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key=True)
    latitude = db.Column(db.String(20))
    longitude = db.Column(db.String(20))
    lastUpdate = db.Column(db.DateTime)

    def __init__(self,clubID,playerID,latitude,longitude,lastUpdate):
        self.clubID = clubID
        self.playerID = playerID
        self.latitude = latitude
        self.longitude = longitude
        self.lastUpdate = lastUpdate

    def json(self):
        return {
            "clubID" : self.clubID,
            "playerID" : self.playerID,
            "latitude" : self.latitude,
            "longitude" : self.longitude,
            "lastUpdate" : self.lastUpdate.isoformat()
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_location(cls,clubID,playerID):
        return cls.query.filter_by(clubID=clubID,playerID=playerID).first()

    @classmethod
    def find_all_club_players_location(cls,clubID):
        return cls.query.filter_by(clubID=clubID)

    def save_to_db(self):   ## upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):   ## delete
        db.session.delete(self)
        db.session.commit()
