from db import db

class TokenModel(db.Model):
    __tablename__ = 'token'

    id = db.Column(db.Integer, primary_key=True)
    playerID = db.Column(db.Integer, db.ForeignKey('player.id'))
    instanceToken = db.Column(db.String(1000))

    def __init__(self,_id,playerID,instanceToken):
        self.id = _id
        self.playerID = playerID
        self.instanceToken = instanceToken

    def json(self):
        return {
                    "id": self.id,
                    "playerID": self.playerID,
                    "instanceToken": self.instanceToken
                }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_token_by_player_id(cls,playerID):
        return cls.query.filter_by(playerID=playerID).first()

    def save_to_db(self):   ## upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):   ## delete
        db.session.delete(self)
        db.session.commit()
