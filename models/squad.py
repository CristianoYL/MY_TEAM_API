from db import db

class SquadModel(db.Model):
    __tablename__ = 'squad'

    tournamentID = db.Column(db.Integer,db.ForeignKey('tournament.id'), primary_key=True)
    clubID = db.Column(db.Integer, db.ForeignKey('club.id'), primary_key=True)
    playerID = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key=True)
    number = db.Column(db.Integer)
    isAdmin = db.Column(db.Boolean)

    def __init__(self,tournamentID,clubID,playerID,number,isAdmin):
        self.tournamentID = tournamentID
        self.clubID = clubID
        self.playerID = playerID
        self.number = number
        self.isAdmin = isAdmin

    def json(self):
        return {
            'tournamentID' : self.tournamentID,
            'clubID' : self.clubID,
            'playerID' : self.playerID,
            'number' : self.number,
            'isAdmin' : self.isAdmin
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_tournament_id(cls,tournamentID):
        return cls.query.filter_by(tournamentID=tournamentID)

    @classmethod
    def find_by_club_id(cls,clubID):
        return cls.query.filter_by(clubID=clubID)

    @classmethod
    def find_by_player_id(cls,playerID):
        return cls.query.filter_by(playerID=playerID)

    @classmethod
    def find_tournament_club_squad(cls,tournamentID,clubID):
        return cls.query.filter_by(tournamentID=tournamentID,clubID=clubID)

    @classmethod
    def find_player(cls,tournamentID,clubID,playerID):
        return cls.query.filter_by(tournamentID=tournamentID,clubID=clubID,playerID=playerID).first()

    @classmethod
    def is_number_available(cls,tournamentID,clubID,number):
        player = cls.query.filter_by(tournamentID=tournamentID,clubID=clubID,number=number).first()
        if player:
            return False
        return True

    def save_to_db(self):   ## upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):   ## delete
        db.session.delete(self)
        db.session.commit()
