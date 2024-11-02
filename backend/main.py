from flask import Flask
import os
from application.database import db
from flask import jsonify
from flask import request
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required, set_access_cookies
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta


from flask_caching import Cache
from celery.schedules import crontab
# from config import LocalDevelopmentConfig
from celery import Celery
# from send_mail import init_mail
from flask_mail import Message
from flask_sse import sse
from functools import wraps
from sqlalchemy import or_

#creates app instance -object of flask
app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///Householdservices_db.db"

CORS(app, origins='http://localhost:5173')
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "3DFGHVKxdgfbchsvdjesvfjfdry3fuyb"  
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)

db.init_app(app=app) #object.method(parameter)

app.app_context().push()

from application.controllers import *

with app.app_context():
    db.create_all()
    if __name__=='__main__':
        app.run(host="0.0.0.0", port=8080)





