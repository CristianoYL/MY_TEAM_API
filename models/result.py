from db import db
from sqlalchemy import or_

class ResultModel(db.Model):
    __tablename__ = 'result'

    # (id,home,away,tournamentID,date,stage,ftScore,extraScore,penScore,info,homeEvents,awayEvents)
    id = db.Column(db.Integer, primary_key=True)
    home = db.Column(db.Integer, db.ForeignKey('club.id'))
    away = db.Column(db.Integer, db.ForeignKey('club.id'))
    tournamentID = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    date = db.Column(db.Date)
    stage = db.Column(db.String(30))
    ftScore = db.Column(db.String(20))
    extraScore = db.Column(db.String(20))
    penScore = db.Column(db.String(20))
    info = db.Column(db.String(500))
    homeEvents = db.Column(db.String(1000))
    awayEvents = db.Column(db.String(1000))

    def __init__(self,_id,home,away,tournamentID,date,stage,ftScore,extraScore,penScore,info,homeEvents,awayEvents):
        self.id = _id
        self.home = home
        self.away = away
        self.tournamentID = tournamentID
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
            "home" : self.home,
            "away" : self.away,
            "tournamentID" : self.tournamentID,
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
    def find_by_tournament_home_away_date_stage(cls,tournamentID,home,away,date,stage):
        return cls.query.filter_by(home=home,away=away,tournamentID=tournamentID,date=date,stage=stage).first()

    @classmethod
    def find_by_home(cls,home):
        return cls.query.filter_by(home=home)

    @classmethod
    def find_by_away(cls,away):
        return cls.query.filter_by(away=away)

    @classmethod
    def find_by_club(cls,clubID):
        return cls.query.filter(or_(cls.home==clubID,cls.away==clubID))

    @classmethod
    def find_club_tournament_result(cls,tournamentID,clubID):
        return cls.query.filter_by(tournamentID=tournamentID).filter(or_(cls.home==clubID,cls.away==clubID))

    def save_to_db(self):   ## upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):   ## delete
        db.session.delete(self)
        db.session.commit()
