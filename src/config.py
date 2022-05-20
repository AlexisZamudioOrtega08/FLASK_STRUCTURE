#This is a config file taken by the flask main app.
from dotenv import load_dotenv
import os

from gevent import config

load_dotenv('../.venv')

#This key is used to encrypt the session data is needed.
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

    #This is the database configuration.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    username, password = os.getenv('MYSQL_DATABASE_USER'), os.getenv('MYSQL_DATABASE_PASSWORD')
    host, database = os.getenv('MYSQL_DATABASE_HOST'), os.getenv('MYSQL_DATABASE_DB')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{username}:{password}@{host}/{database}' 

class DevelopmentConfig(Config):
    DEBUG = True
    #UPLOADS = "PATH_TO_UPLOADS_DEV"
    SESSION_COOKIE_SECURE = False

    
class TestingConfig(Config):
    TESTING = True
    #UPLOADS = "PATH_TO_UPLOADS_TEST"

class ProductionConfig(Config):
    DEBUG = False
    #UPLOADS = "PATH_TO_UPLOADS_PROD"

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

