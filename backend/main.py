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
 
CORS(app, supports_credentials=True)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "3DFGHVKxdgfbchsvdjesvfjfdrbbbby3fuyb" 
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'
app.config['BROKER_CONNECTION_RETRY_ON_STARTUP'] = True
app.config['CELERY_TIMEZONE'] = 'Asia/Kolkata'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1) 

#doubtful
app.config["REDIS_URL"] = "redis://localhost"
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
######

jwt = JWTManager(app)

db.init_app(app=app) #object.method(parameter)

app.app_context().push()

from application.controllers import *

with app.app_context():
    db.create_all()
    if __name__=='__main__':
        app.run(host="0.0.0.0", port=8080)

# ------- Flask sse-------( server sent events) for publishing events /alerts to users --frontend-in vue mounted :subscribe the event #
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

mail = init_mail()

#SCHEDULED TASKS 
#DAILY REMINDER TO PROF MAIL/SMS IF SEVREQ=requested ALERT TO ACCEPT/REJECT , SET A TIME TO SEND THE REMINDER(EVENING)
@celery.task()
def daily_reminder_to_professional():
    profs=Professional.query.all()
    for prof in profs:
        flag=True
        for req in prof.prof_req:
            if req.sev_status!='requested':
                print(req.sev_status)
                flag=False
                break                
        if flag:
            with mail.connect() as conn:
                subject= " HomeWhiz Household services Reminder"
                message = """
                        <div style="max-width: 600px; margin: 20px auto; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                            <h1 style="color: #28a745;">Reminder: Visit HomeWhiz Household services app</h1>
                            <p>This is a friendly reminder to visit HomeWhiz Household services app and accept or reject the service requests.</p>
                            <p>Don't miss out on the latest service requests. Click the link below to accept or reject them..</p>
                            <a href="http://127.0.0.1:8080/" style="display: inline-block; padding: 10px 20px; background-color: #28a745; color: #fff; text-decoration: none; border-radius: 5px;">HomeWhiz Reminder</a>
                            <p>If you have any questions or need assistance, feel free to reach out to our support team.</p>
                        </div>
                        """
                msg = Message(recipients=[prof.prof_email],html=message, subject=subject)
                conn.send(msg)
            sse.publish({"message": "You have pending service requests, please accept or reject the request!", "color":"alert alert-primary" },type=prof.prof_email)
    print('daily reminder to professionals executed')
    return {"status": "success"}


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





