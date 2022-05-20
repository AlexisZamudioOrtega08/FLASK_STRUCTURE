#---------------- IMPORTS -------------------# 
from dotenv import load_dotenv
from flask import Flask, jsonify
import os

#To handle connections to the database.
from db import db

#crsf token protection
#from flask_wtf.csrf import CSRFProtect

#Api resources 
from flask_restful import Api

#auth resources
from flask_jwt import JWT
from security import authenticate, identity

#------------- CONFIGURATION ----------------# 
from config import config

#-------------- CONTROLLERS -----------------#
from resources.item import Item, ItemList
from resources.user import UserPasswordUpdate, UserRegister
#----------------- MODELS -------------------#
from models.userModel import UserModel

#---------- SECRET KEY LOAD -----------------#
def load_env_var():
    load_dotenv('../.venv')
    secretKey = os.getenv('SECRET_KEY')
    return secretKey

#------------- APP INITIALIZATION -----------#
app = Flask(__name__)
api = Api(app)

#------------- CREATE DATABASE --------------#
@app.before_first_request
def create_tables():
    db.create_all()
    if not UserModel.find_by_username('admin'):
        user = UserModel(0, 'admin', 'admin')
        user.save_to_db()

#------ AUTHENTICATION AND AUTHORIZATION -----#
#csrf = CSRFProtect()
app.secret_key = load_env_var()
jwt = JWT(app, authenticate, identity) # /auth 

#----------------- ROUTES -------------------#

#USER ROUTES
api.add_resource(UserRegister, '/user/register')
api.add_resource(UserPasswordUpdate, '/user/<string:username>')

#ITEM ROUTES
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Item, '/item', endpoint='post_item')
api.add_resource(ItemList, '/items')

def status_404(error):
    return jsonify({'message': 'Not found'}), 404

if __name__ == '__main__':
    #add configuration to the web app
    app.config.from_object(config['default'])
    #init database connection
    db.init_app(app)
    #manage page 404
    app.register_error_handler(404, status_404)
    #start the web app
    app.run()