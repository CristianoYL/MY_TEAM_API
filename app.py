from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

from resources.user import UserRegistration,UserList,UserUpdate
from resources.player import Player,PlayerList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///myteam.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'myteam'
api = Api(app)

jwt = JWT(app,authenticate,identity)    #/auth

api.add_resource(Player,'/player/<string:email>')
api.add_resource(PlayerList,'/player')
api.add_resource(UserRegistration,'/user')
api.add_resource(UserUpdate,'/user/<string:email>')
api.add_resource(UserList,'/user')

if __name__ == '__main__' :
    from db import db
    db.init_app(app)
    app.run(port = 5000,debug=True)
