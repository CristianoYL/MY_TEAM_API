import traceback, os
from flask_restful import Resource, reqparse
from flask import redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


class Avatar(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file', type=FileStorage, required=True, location='files')

    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    UPLOAD_FOLDER = ".\\static\\images\\avatar"
    AVATAR_PREFIX = "player_avatar_"

    @classmethod
    def allowed_file(cls, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in cls.ALLOWED_EXTENSIONS

    def get(self, playerID):
        return send_from_directory(self.UPLOAD_FOLDER, '{}{}.jpg'.format(self.AVATAR_PREFIX, playerID))

    def post(self, playerID):
        # check if the post request has the file part
        data = self.parser.parse_args()
        file = data['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(self.UPLOAD_FOLDER, filename))
            return url_for('avatar', playerID=playerID), 200
        return {'message': 'unknown error.'}, 500
