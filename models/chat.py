from db import db

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
    def find_tournament_chat(cls,tournamentID,clubID,limit,offset):
        return cls.query.filter_by(tournamentID=tournamentID,clubID=clubID).order_by(cls.time.desc()).limit(limit).offset(offset).all()

    @classmethod
    def find_club_chat(cls,clubID,limit,offset):
        return cls.query.filter_by(tournamentID=None,clubID=clubID).order_by(cls.time.desc()).limit(limit).offset(offset).all()

    @classmethod
    def find_private_chat(cls,receiverID,senderID,limit,offset):
        return cls.query.filter_by(tournamentID=None,clubID=None,receiverID=receiverID,senderID=senderID).order_by(cls.time.desc()).limit(limit).offset(offset).all()

    def save_to_db(self):   ## upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):   ## delete
        db.session.delete(self)
        db.session.commit()
