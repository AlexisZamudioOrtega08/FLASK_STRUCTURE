from models.userModel import UserModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This field cannot be left blank')
    parser.add_argument('password', type=str, required=True, help='This field cannot be left blank')

    #@jwt_required()
    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}, 400
        else:
            user = UserModel(0, data['username'], data['password'])
            user.save_to_db()
            return {'message': 'User {} created successfully'.format(data['username'])}, 201

class UserPasswordUpdate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str, required=True, help='This field cannot be left blank')

    @jwt_required()
    def put(self, username):
        data = UserPasswordUpdate.parser.parse_args()
        user = UserModel.find_by_username(username)
        if user: 
            if (UserModel.check_password(user.password, data['password'])): 
                return {'message': 'Not changes detected for {}.'.format(user.username)}, 400
            else:
                user.password = user.crate_hash(data['password'])
                user.save_to_db()
                return {'message': 'Password updated successfully for {}.'.format(username)}
        else:
            return {'message': 'User {} not found'.format(username)}, 404



    