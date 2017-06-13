from db import db

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    def __init__(self,_id,email,password):
        self.id = _id
        self.email = email
        self.password = password

    def json(self):
        return {
            "id" : self.id,
            "email" : self.email,
            "password" : self.password
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):   ## upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):   ## delete
        db.session.delete(self)
        db.session.commit()
