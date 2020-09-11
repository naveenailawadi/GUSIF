from flask_restful import Resource
from api.resources import load_json, validate_admin_token, load_header_token, TOKEN_MINUTES
from api.models import db, UserModel, validate_admin


class AlumniAdditionResource(Resource):
    def post(self):
        data = load_json()

        try:
            phone_numbers = data['phone_numbers']
        except KeyError:
            phone_numbers = []

        return data, 201
