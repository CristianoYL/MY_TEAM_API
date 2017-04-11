from db import db
from sqlalchemy import or_

class ResultModel(db.Model):
    __tablename__ = 'result'

    # (id,homeID,awayID,tournamentID,homeName,awayName,tournamentName,date,stage,ftScore,extraScore,penScore,info,homeEvents,awayEvents)
    id = db.Column(db.Integer, primary_key=True)
    homeID = db.Column(db.Integer, db.ForeignKey('club.id'))
    awayID = db.Column(db.Integer, db.ForeignKey('club.id'))
    tournamentID = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    homeName = db.Column(db.String(50))
    awayName = db.Column(db.String(50))
    tournamentName = db.(db.String(50))
    date = db.Column(db.Date)
    stage = db.Column(db.String(30))
    ftScore = db.Column(db.String(20))
    extraScore = db.Column(db.String(20))
    penScore = db.Column(db.String(20))
    info = db.Column(db.String(500))
    homeEvents = db.Column(db.String(1000))
    awayEvents = db.Column(db.String(1000))

    def __init__(self,_id,homeID,awayID,tournamentID,homeName,awayName,tournamentName,date,stage,ftScore,extraScore,penScore,info,homeEvents,awayEvents):
        self.id = _id
        self.homeID = homeID
        self.awayID = awayID
        self.tournamentID = tournamentID
        self.homeName = homeName
        self.awayName = awayName
        self.tournamentName = tournamentName
        self.date = date
        self.stage = stage
        self.ftScore = ftScore
        self.extraScore = extraScore
        self.penScore = penScore
        self.info = info
        self.homeEvents = homeEvents
        self.awayEvents = awayEvents

    def json(self):
        return {
            "id" : self.id,
            "homeID" : self.homeID,
            "awayID" : self.awayID,
            "tournamentID" : self.tournamentID,
            "homeName" : self.homeName,
            "awayName" : self.awayName,
            "tournamentName" : self.tournamentName,
            "date" : self.date.isoformat(),
            "stage" : self.stage,
            "ftScore" : self.ftScore,
            "extraScore": self.extraScore,
            "penScore" : self.penScore,
            "info" : self.info,
            "homeEvents" : self.homeEvents,
            "awayEvents" : self.awayEvents
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_tournament_home_away_date_stage(cls,tournamentID,homeID,awayID,date,stage):
        return cls.query.filter_by(homeID=homeID,awayID=awayID,tournamentID=tournamentID,date=date,stage=stage).first()

    @classmethod
    def find_by_home(cls,homeID):
        return cls.query.filter_by(homeID=homeID)

    @classmethod
    def find_by_away(cls,awayID):
        return cls.query.filter_by(awayID=awayID)

    @classmethod
    def find_by_club(cls,clubID):
        return cls.query.filter(or_(cls.homeID==clubID,cls.awayID==clubID))

    @classmethod
    def find_club_tournament_result(cls,tournamentID,clubID):
        return cls.query.filter_by(tournamentID=tournamentID).filter(or_(cls.homeID==clubID,cls.awayID==clubID))

    def save_to_db(self):   ## upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):   ## delete
        db.session.delete(self)
        db.session.commit()
