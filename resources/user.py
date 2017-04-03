from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt import jwt_required

from models.user import UserModel

class UserRegistration(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True,help="Email cannot be blank.")
    parser.add_argument('password', type=str, required=True, help="Password cannot be blank.")

    @classmethod
    def post(cls):   #register
        credentials = cls.parser.parse_args()

        user = UserModel.find_by_email(credentials['email'])
        if user:
            return {
                'message':'Registration failed! An account with email<{}> already exists.'
                            .format(credentials['email'])
            }, 400

        user = UserModel(None,**credentials)

        try:
            user.save_to_db()
        except:
            return {'message':'Internal Server Error, registration failed!'}, 500
        return {'message':'Register account <{}> succeeded!'.format(credentials['email'])}, 201


class UserUpdate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str, required=True, help="Password cannot be blank.")

    @classmethod
    @jwt_required()
    def post(cls,email):   #change password
        new_password = cls.parser.parse_args()['password']
        user = UserModel.find_by_email(email)
        if user:    # user exists
            if safe_str_cmp(user.password,new_password):    # no change in new password
                return {'message':'You cannot use the same password!'}, 400
            # if password is valid
            user.password = new_password
            try:
                user.save_to_db()
            except:
                return {'message':'Internal Server Error, change password failed!'}, 500
            return {'message':'password updated!'}, 200
        # if account doesn't exists
        return {'message':'Account not found!'}, 404


class UserList(Resource):
    @classmethod
    def get(cls):   #view all users
        users = []
        result = UserModel.find_all()
        for user in result:
            users.append({'id':user.id,'email':user.email})
        return {'users':users},200
