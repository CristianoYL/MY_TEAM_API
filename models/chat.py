from db import db
from sqlalchemy import or_,and_

class ChatModel(db.Model):
    __tablename__ = 'chat'

    id = db.Column(db.Integer, primary_key=True)
    tournamentID = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    clubID = db.Column(db.Integer, db.ForeignKey('club.id'))
    receiverID = db.Column(db.Integer, db.ForeignKey('player.id'))
    senderID = db.Column(db.Integer, db.ForeignKey('player.id'))
    messageType = db.Column(db.String(20))
    messageContent = db.Column(db.String(3000))
    time = db.Column(db.DateTime)


    def __init__(self,_id,tournamentID,clubID,receiverID,senderID,messageType,messageContent,time):
        self.id = _id
        self.tournamentID = tournamentID
        self.clubID = clubID
        self.receiverID = receiverID
        self.senderID = senderID
        self.messageType = messageType
        self.messageContent = messageContent
        self.time = time

    def json(self):
        return {
            "id" : self.id,
            "tournamentID" : self.tournamentID,
            "clubID" : self.clubID,
            "receiverID" : self.receiverID,
            "senderID" : self.senderID,
            "messageType" : self.messageType,
            "messageContent" : self.messageContent,
            "time" : self.time.isoformat()
        }

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_tournament_chat(cls,tournamentID,clubID,limit,beforeID,afterID):
        if beforeID:    # find chat prioir to given ID
            return cls.query.filter(cls.id < beforeID).filter_by(
                tournamentID=tournamentID,clubID=clubID
                ).order_by(cls.time.desc()).limit(limit)
        if afterID:     # find chat after given ID
            return cls.query.filter(cls.id > afterID).filter_by(
                tournamentID=tournamentID,clubID=clubID
                ).order_by(cls.time.desc()).limit(limit)
        # no requirement, find most recent chat
        return cls.query.filter_by(
            tournamentID=tournamentID,clubID=clubID
            ).order_by(cls.time.desc()).limit(limit)

    @classmethod
    def find_club_chat(cls,clubID,limit,beforeID,afterID):
        if beforeID:    # find chat prioir to given ID
            return cls.query.filter(cls.id < beforeID).filter_by(
                tournamentID=None,clubID=clubID
                ).order_by(cls.time.desc()).limit(limit)
        if afterID:     # find chat after given ID
            return cls.query.filter(cls.id > afterID).filter_by(
                tournamentID=None,clubID=clubID
                ).order_by(cls.time.desc()).limit(limit)
        # no requirement, find most recent chat
        return cls.query.filter_by(
            tournamentID=None,clubID=clubID
            ).order_by(cls.time.desc()).limit(limit)

    @classmethod
    def find_private_chat(cls,receiverID,senderID,limit,beforeID,afterID):
        if beforeID:    # find chat prioir to given ID
            return cls.query.filter(cls.id < beforeID).filter(
                or_(
                    and_(
                        cls.tournamentID==None,
                        cls.clubID==None,
                        cls.receiverID==receiverID,
                        cls.senderID==senderID
                        ),
                    and_(
                        cls.tournamentID==None,
                        cls.clubID==None,
                        cls.receiverID==senderID,
                        cls.senderID==receiverID
                        )
                    )
                ).order_by(cls.time.desc()).limit(limit)

        if afterID:     # find chat after given ID
            return cls.query.filter(cls.id > afterID).filter(
                or_(
                    and_(
                        cls.tournamentID==None,
                        cls.clubID==None,
                        cls.receiverID==receiverID,
                        cls.senderID==senderID
                        ),
                    and_(
                        cls.tournamentID==None,
                        cls.clubID==None,
                        cls.receiverID==senderID,
                        cls.senderID==receiverID
                        )
                    )
                ).order_by(cls.time.desc()).limit(limit)
        # no requirement, find most recent chat
        return cls.query.filter(
            or_(
                and_(
                    cls.tournamentID==None,
                    cls.clubID==None,
                    cls.receiverID==receiverID,
                    cls.senderID==senderID
                    ),
                and_(
                    cls.tournamentID==None,
                    cls.clubID==None,
                    cls.receiverID==senderID,
                    cls.senderID==receiverID
                    )
                )
            ).order_by(cls.time.desc()).limit(limit)

    def save_to_db(self):   ## upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):   ## delete
        db.session.delete(self)
        db.session.commit()
