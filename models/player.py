from db import db

class PlayerModel(db.Model):
    __tablename__ = 'player'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), db.ForeignKey('user.email'))
    role = db.Column(db.String(30))
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    displayName = db.Column(db.String(50))
    age = db.Column(db.Integer)
    height = db.Column(db.Float(precision=1))
    weight = db.Column(db.Float(precision=1))
    phone = db.Column(db.String(20))
    leftFooted = db.Column(db.Boolean)
    avatar = db.Column(db.Integer)

    def __init__(self,_id,email,role,firstName,lastName,displayName,
                age,height,weight,phone,leftFooted,avatar):
        self.id = _id
        self.email = email
        self.role = role
        self.firstName = firstName
        self.lastName = lastName
        self.displayName = displayName
        self.age = age
        self.weight = weight
        self.height = height
        self.phone = phone
        self.leftFooted = leftFooted
        self.avatar = avatar

    def json(self):
        return {
            "id" : self.id,
            "email" : self.email,
            "role" : self.role,
            "firstName" : self.firstName,
            "lastName" : self.lastName,
            "displayName" : self.displayName,
            "age" : self.age,
            "height": self.height,
            "weight" : self.weight,
            "phone" : self.phone,
            "leftFooted" : self.leftFooted,
            "avatar" : self.avatar
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

    @classmethod
    def find_by_display_name(cls,displayName):
        return cls.query.filter_by(displayName=displayName)

    @classmethod
    def find_by_fullname(cls,firstName,lastName):
        return cls.query.filter_by(firstName=firstName,lastName=lastName)

    @classmethod
    def find_by_firstname(cls,firstName):
        return cls.query.filter_by(firstName=firstName)

    @classmethod
    def find_by_lastname(cls,lastName):
        return cls.query.filter_by(lastName=lastName)

    def save_to_db(self):   ## upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):   ## delete
        db.session.delete(self)
        db.session.commit()
