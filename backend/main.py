from flask import Flask,url_for
from application.database import db
from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from celery.schedules import crontab
from celery import Celery
from send_mail import init_mail
from flask_mail import Message
from flask_sse import sse
from functools import wraps
from jinja2 import Template
import csv

celery = Celery('Application')

def create_app():
    app = Flask(__name__)    
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///Householdservices_db.db"
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
    
    app.config["REDIS_URL"] = "redis://localhost"
    
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_HOST'] = 'localhost'      
    app.config['CACHE_REDIS_PORT'] = 6379             
    app.config['CACHE_REDIS_DB'] = 0
    CORS(app, supports_credentials=True, origins="http://localhost:5173")
    jwt = JWTManager(app)
    db.init_app(app)
    app.app_context().push()
    celery.conf.update(
    broker_url=app.config["CELERY_BROKER_URL"],
    result_backend=app.config["CELERY_RESULT_BACKEND"],
    timezone=app.config["CELERY_TIMEZONE"],
    broker_connection_retry_on_startup=app.config["BROKER_CONNECTION_RETRY_ON_STARTUP"]
    )
    celery.conf.timezone = 'Asia/Kolkata'
    class ContextTask(celery.Task):
      def __call__(self, *args, **kwargs):
          with app.app_context():
              return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return app, jwt
   
app, jwt = create_app()

#creates app instance -object of flask
# app=Flask(__name__)


# CORS(app,supports_credentials=True)

# jwt = JWTManager(app)

# db.init_app(app=app) #object.method(parameter)

# app.app_context().push()



from application.controllers import *

# ------- Flask sse-------( server sent events) for publishing events /alerts to users --frontend-in vue mounted :subscribe the event #
app.register_blueprint(sse, url_prefix='/stream')

mail = init_mail()

#SCHEDULED TASKS (CELERY)
@celery.task()
def daily_reminder_to_professional():
    profs=Professional.query.all()
    for prof in profs:
        print(prof.prof_email)
        flag=False
        for req in prof.prof_req:
            if req.sev_status =='requested':
                print(req.sev_status)
                flag=True
                break                
        if flag:
            with mail.connect() as conn:
                subject= " HomeWhiz Household services Reminder"
                message = """
                        <div style="max-width: 600px; margin: 20px auto; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                            <h1 style="color: rgb(63, 35, 18);">Reminder: Visit HomeWhiz Household services app</h1>
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <a href="http://127.0.0.1:8080/" style="padding: 10px 20px; background-color: rgb(63, 35, 18); color: #fff; text-decoration: none; border-radius: 5px;">HomeWhiz Reminder</a>
                            </div>
                            <p>This is a friendly reminder to visit HomeWhiz Household services app and accept or reject the service requests.</p>
                            <p>Don't miss out on the latest service requests. Click the link above to accept or reject them.</p>
                            <p>If you have any questions or need assistance, feel free to reach out to our support team.</p>
                            <p>Best regards,<br>Homewhiz Team</p>

                        </div>
                        """
                msg = Message(recipients=[req.prof_email],html=message, subject=subject)
                conn.send(msg)
            sse.publish({"message": "You have pending service requests, please accept or reject the request!", "color":"alert alert-primary" },type=prof.prof_email)
    print('daily reminder to professionals executed')
    return {'message': 'daily reminder to professionals executed',"status": "success"}
###app,app_context
@celery.task()
def monthly_report_to_customers():
    custs=Customer.query.all()
    for cust in custs:
            with mail.connect() as conn:
                subject= "Homewhiz household services app Monthly Report"
                template =Template( """
                        <div style="max-width: 600px; margin: 20px auto; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                            <h1 style="color:  rgb(63, 35, 18);">Order Report</h1>
                            <p>Dear {{ name }},</p>
                            <p>Here is the order report for the specified date range.</p>
                    
                            <!-- Add your report content here -->
                            <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                                <thead>
                                    <tr style="background-color: rgb(63, 35, 18); color: #fff;">
                                        <th style="padding: 10px; text-align: left;"> Service request id</th>
                                        <th style="padding: 10px; text-align: left;">Professional email</th>
                                        <th style="padding: 10px; text-align: left;">Date of request</th>
                                        <th style="padding: 10px; text-align: left;">Date of completion</th>
                                        <th style="padding: 10px; text-align: left;">Status</th>
                                        <th style="padding: 10px; text-align: left;">Rating</th>
                                        <th style="padding: 10px; text-align: left;">Remarks</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for req in requests %}
                                    <tr>
                                        <td style="padding: 10px; border-bottom: 1px solid #ddd;">{{req.sevreq_id  }}</td>
                                        <td style="padding: 10px; border-bottom: 1px solid #ddd;">{{ req.prof_email }}</td>
                                        <td style="padding: 10px; border-bottom: 1px solid #ddd;">{{ req.date_of_request }}</td>
                                        <td style="padding: 10px; border-bottom: 1px solid #ddd;">{{ req.date_of_completion }}</td>
                                        <td style="padding: 10px; border-bottom: 1px solid #ddd;">{{ req.sev_status }}</td>
                                        <td style="padding: 10px; border-bottom: 1px solid #ddd;">{{ req.rating }}</td>
                                        <td style="padding: 10px; border-bottom: 1px solid #ddd;">{{ req.remarks }}</td>
                                       </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                    
                            <p>If you have any questions or need further details, please don't hesitate to contact us.</p>
                            <p>Thank you for your attention!</p>
                            <p>Best regards,<br>Homewhiz Team</p>
                        </div>
                        """)
                message = template.render(name=cust.cust_email.split("@")[0], requests = cust.cust_req )
                msg = Message(recipients=[cust.cust_email],html=message, subject=subject)
                conn.send(msg)
    print('monthly report to users executed')
    return {"status": "success",'message': "Monthly report to users executed"}

@celery.task()
def user_triggered_async_job(prof_email):
    header = ["Service request id", "Professional email", "Customer email", "Service id", "Date of request", "Date of completion", "Status", "Rating", "Remarks"]
    content = []
    
    with open(f'reports/servicerequest_report_{prof_email}.csv', 'w', newline='') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(header)
        
        for req in Sevrequest.query.filter_by(prof_email=prof_email).all():
            if req.sev_status == "closed":
                row = [
                    req.sevreq_id,
                    req.prof_email,
                    req.cust_email,
                    req.sev_id,
                    req.date_of_request,
                    req.date_of_completion,
                    req.sev_status,
                    req.rating,
                    req.remarks,
                ]
                csvwriter.writerow(row)
                content.append({
                    'sevreq_id': req.sevreq_id,
                    'prof_email': req.prof_email,
                    'cust_email': req.cust_email,
                    'service_id': req.sev_id,
                    'date_of_request': req.date_of_request,
                    'date_of_completion': req.date_of_completion,
                    'sev_status': req.sev_status,
                    'rating': req.rating,
                    'remarks': req.remarks,
                })
    
    sse.publish({"message": " Trial User triggered async job executed","color":"alert alert-primary", "filename": f'servicerequest_report_{prof_email}.csv',}, type="notifyadmin")
    print(f'Export job for {prof_email} completed.')
    return {'header': header, 'content': content, 'message': "User triggered async job executed"}
    

# ------- To schedule the tasks --------#
# celery.conf.beat_schedule = {
#     'my_daily_task': {
#         'task': "main.daily_reminder_to_professional",
#         'schedule': crontab(hour=21, minute=0),
#     },
#     'my_quick_check_task': {
#         'task': "main.monthly_report_to_customers",
#         'schedule': crontab(day_of_month='1',hour=9, minute=0),
#     }
# }


celery.conf.beat_schedule = {
    'my_daily_task': {
        'task': "main.daily_reminder_to_professional",
        'schedule': crontab(minute='*/1'),  
    },
    'my_monthly_task': {
        'task': "main.monthly_report_to_customers",
        'schedule': crontab(minute='*/1'), 
    }
}

with app.app_context():
    db.create_all()
    if __name__=='__main__':
        app.run(host="0.0.0.0", port=8080)

###

