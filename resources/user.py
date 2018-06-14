from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token

from models.user import UserModel

BLANK_ERROR = '`{}` cannot be blank.'
INTERNAL_ERROR = 'Internal server error. {}'
DUPLICATE_EMAIL_ERROR = 'A user with email `{}` already exists.'

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('email', type=str, required=True, help=BLANK_ERROR.format('email'))
_user_parser.add_argument('password', type=str, required=True, help=BLANK_ERROR.format('password'))


class User(Resource):

    @classmethod
    def get(cls):  # view all users
        users = []
        result = UserModel.find_all()
        for user in result:
            users.append({'id': user.id, 'email': user.email})
        return {'users': users}, 200

    @classmethod
    def post(cls):  # register user
        credentials = _user_parser.parse_args()

        if UserModel.find_by_email(credentials['email']):
            return {'message': DUPLICATE_EMAIL_ERROR.format(credentials['email'])}, 400

        user = UserModel(None, **credentials)

        try:
            user.save_to_db()
            return {'message': 'Register account <{}> succeeded!'.format(credentials['email'])}, 201
        except:
            return {'message': INTERNAL_ERROR.format('Registration failed!')}, 500



class UserUpdate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str, required=True, help=BLANK_ERROR.format('password'))

    @classmethod
    @jwt_required
    def put(cls):  # change password
        user = get_jwt_identity()
        new_password = cls.parser.parse_args()['password']
        if safe_str_cmp(user.password, new_password):  # no change in new password
            return {'message': 'You cannot use the same password!'}, 400
        # if password is valid
        user.password = new_password
        try:
            user.save_to_db()
            return {'message': 'password updated!'}, 200
        except:
            return {'message': INTERNAL_ERROR.format('Changing password failed!')}, 500


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid credentials!'}, 401
