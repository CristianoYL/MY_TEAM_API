from db import db

class PlayerModel(db.Model):
    __tablename__ = 'player'

    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    role = db.Column(db.String(30))
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    displayName = db.Column(db.String(50))
    age = db.Column(db.Integer)
    height = db.Column(db.Float(precision=1))
    weight = db.Column(db.Float(precision=1))
    phone = db.Column(db.String(20))
    leftFooted = db.Column(db.Boolean)
    avatar = db.Column(db.String(300))

    def __init__(self,_id,userID,role,firstName,lastName,displayName,
                age,height,weight,phone,leftFooted,avatar):
        self.id = _id
        self.userID = userID
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
            "userID" : self.userID,
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
    def find_by_user(cls,userID):
        return cls.query.filter_by(userID=userID).first()

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
