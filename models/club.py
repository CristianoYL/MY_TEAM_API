from db import db

class ClubModel(db.Model):
    __tablename__ = 'club'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    info = db.Column(db.String(2000))

    def __init__(self,_id,name,info):
        self.id = _id
        self.name = name
        self.info = info

    def json(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "info" : self.info
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):   ## upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):   ## delete
        db.session.delete(self)
        db.session.commit()
