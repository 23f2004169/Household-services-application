from flask import Flask
import os
from application.database import db
from flask import jsonify
from flask import request
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required, set_access_cookies
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from celery.schedules import crontab
# from config import LocalDevelopmentConfig
from celery import Celery
from send_mail import init_mail
from flask_mail import Message
from flask_sse import sse
from functools import wraps

from cache import Cache

#creates app instance -object of flask
app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///Householdservices_db.db"
 
CORS(app, origins=['http://localhost:5173'], supports_credentials=True)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "3DFGHVKxdgfbchsvdjesvfjfdrbbbby3fuyb" 
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'
app.config['BROKER_CONNECTION_RETRY_ON_STARTUP'] = True
app.config['CELERY_TIMEZONE'] = 'Asia/Kolkata'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1) #token expire after 1 hour
jwt = JWTManager(app)

db.init_app(app=app) #object.method(parameter)


cache = Cache(app)


app.app_context().push()

from application.controllers import *

with app.app_context():
    db.create_all()
    if __name__=='__main__':
        app.run(host="0.0.0.0", port=8080)

# ------- Flask sse( server sent events) for publishing events /alerts to users -------frontend-in vue mounted :subscribe the event #
app.register_blueprint(sse, url_prefix='/stream')

# ------- Celery app ------- #
celery = Celery('Application')

# Update celery app configurations
celery.conf.update(
    broker_url=app.config["CELERY_BROKER_URL"],
    result_backend=app.config["CELERY_RESULT_BACKEND"],
    timezone=app.config["CELERY_TIMEZONE"],
    broker_connection_retry_on_startup=app.config["BROKER_CONNECTION_RETRY_ON_STARTUP"]
)
celery.conf.timezone = 'Asia/Kolkata'


@celery.task()
def monthly_report():
    print('monthly report to users executed')
    return {'message': "Monthly report to users executed"}


@celery.task()
def user_triggered_async_job():
    print('user triggered async job executed')
    return {'message': "User triggered async job executed"}


# ------- To schedule the tasks --------#
celery.conf.beat_schedule = {
    'my_daily_task': {
        'task': "main.monthly_report",
        'schedule': crontab(hour=21, minute=0),
    },
    'my_quick_check_task': {
        'task': "main.monthly_report",
        'schedule': crontab(minute='*/1'),
    },
}





