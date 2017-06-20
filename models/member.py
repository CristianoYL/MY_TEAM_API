from db import db

class MemberModel(db.Model):
    __tablename__ = 'member'

    clubID = db.Column(db.Integer, db.ForeignKey('club.id'), primary_key=True)
    playerID = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key=True)
    memberSince = db.Column(db.Date)
    isActive = db.Column(db.Boolean)
    priority = db.Column(db.Integer)
    # priority: 0-applicant,1-member, 2-admin, 3-leader

    priority_applicant = 0
    priority_regular = 1
    priority_cocap = 2
    priority_captain = 3

    def __init__(self,clubID,playerID,memberSince,isActive,priority):
        self.clubID = clubID
        self.playerID = playerID
        self.memberSince = memberSince
        self.isActive = isActive
        self.priority = priority

    def json(self):
        return {
            "clubID" : self.clubID,
            "playerID" : self.playerID,
            "memberSince" : self.memberSince.isoformat(),
            "isActive" : self.isActive,
            "priority" : self.priority
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_club_player(cls,clubID,playerID):
        return cls.query.filter_by(clubID=clubID,playerID=playerID).first()

    @classmethod
    def find_club_active_player(cls,clubID):
        return cls.query.filter_by(clubID=clubID,isActive=True)

    @classmethod
    def find_by_player(cls,playerID):
        return cls.query.filter_by(playerID=playerID)

    @classmethod
    def find_by_club(cls,clubID):
        return cls.query.filter_by(clubID=clubID)

    def save_to_db(self):   ## upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):   ## delete
        db.session.delete(self)
        db.session.commit()
