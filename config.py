#This is configuration folder to figure flask


from datetime import timedelta
import os
from dotenv import load_dotenv #allows us to load our environment

#establish our base directory so whenever we use "."

basedir = os.path.abspath(os.path.dirname(__file__))



#need to establish where our envireonment variabels are coming from
load_dotenv(os.path.join(basedir, '.env'))



#Create our Config class
class Config():
    """
    
    Create Config class which will setup out configuration variables.
    Using Environment variables where available other create config variable.
    """

#regular config for Flask app
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASC_ENV = os.environ.get('FLASK_ENV')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    
    #config if you are connecting to database
    SECRET_KEY = os.environ.get('SECKET_KEY') or 'Literally whatever you want as long as its s string. Cool Beans'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=365)

