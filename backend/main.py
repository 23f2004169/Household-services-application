from flask import Flask
from application.database import db
from datetime import timedelta
from flask_jwt_extended import JWTManager #JWT  Authentication for user
from flask_cors import CORS  #Allows cross-origin requests
from celery.schedules import crontab
from celery import Celery # For background task scheduling 
from send_mail import init_mail
from flask_mail import Message
from flask_sse import sse #For publishing events
from jinja2 import Template
import csv

def create_app():
    app = Flask(__name__)  
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///Householdservices_db.db" 
    app.config["JWT_SECRET_KEY"] = "3DFGHVKxdgfbchsvdjesvfjfdrbbbby3fuyb" 
    app.config['JWT_COOKIE_SECURE'] = False
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1) 
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1' 
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'
    app.config['BROKER_CONNECTION_RETRY_ON_STARTUP'] = True
    app.config['CELERY_TIMEZONE'] = 'Asia/Kolkata'  
    app.config["REDIS_URL"] = "redis://localhost" 
    app.config['CACHE_TYPE'] = 'RedisCache'  
    app.config['CACHE_REDIS_HOST'] = 'localhost'    
    app.config['CACHE_REDIS_PORT'] = 6379            
    app.config['CACHE_REDIS_DB'] = 0 
    CORS(app, supports_credentials=True, origins="http://localhost:5173")
    jwt = JWTManager(app) 
    db.init_app(app) 
    app.app_context().push() 
    return app, jwt

app, jwt = create_app()

# ------- Celery app ------- #
celery = Celery('Application')

celery.conf.update(
    broker_url=app.config["CELERY_BROKER_URL"],
    result_backend=app.config["CELERY_RESULT_BACKEND"],
    timezone=app.config["CELERY_TIMEZONE"],
    broker_connection_retry_on_startup=app.config["BROKER_CONNECTION_RETRY_ON_STARTUP"]
    ) 
celery.conf.timezone = 'Asia/Kolkata'

from application.controllers import *

# ---- Flask sse: To publish events ------ #
app.register_blueprint(sse, url_prefix='/stream')     

mail = init_mail() 

@celery.task()
def daily_reminder_to_professional():
    profs=Professional.query.all()
    for prof in profs:
        flag=False
        for req in prof.prof_req:
            if req.sev_status =='requested':
                flag=True
                break                
        if flag:
            with mail.connect() as conn:
                subject= " HomeWhiz Household services Reminder"
                message = """
                        <div style="max-width: 600px; margin: 20px auto; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); font-family: Arial, sans-serif;">
                            <h1 style="color: #3F2312; font-size: 24px;">Reminder: Visit HomeWhiz Household Services App</h1>
                            <div style="display: flex; align-items: center; justify-content: start; gap: 10px; margin-top: 10px;">
                                <a href="http://localhost:5173/" style="padding: 10px 20px; background-color: #3F2312; color: #fff; text-decoration: none; border-radius: 5px; font-weight: bold;">Visit HomeWhiz</a>
                            </div>
                            <p style="color: #333; margin-top: 20px;">This is a friendly reminder to visit HomeWhiz Household Services App and accept or reject the service requests.</p>
                            <p style="color: #333;">Don't miss out on the latest service requests. Click the link above to access them.</p>
                            <p style="color: #333;">If you have any questions or need assistance, feel free to reach out to our support team.</p>
                            <p style="margin-top: 20px; color: #555;">Best regards,<br><strong>HomeWhiz Team</strong></p>
                        </div>
                        """
                msg = Message(recipients=[req.prof_email],html=message, subject=subject)
                conn.send(msg)
            sse.publish({"message": "You have pending service requests, please accept or reject the request!", "color":"alert alert-primary" },type=prof.prof_email)
    print('daily reminder to professionals executed')
    return {'message': 'daily reminder to professionals executed',"status": "success"}

@celery.task()
def monthly_report_to_customers():
    custs=Customer.query.all()
    for cust in custs:
            with mail.connect() as conn:
                subject= "Homewhiz household services app Monthly Report"
                template =Template( """
                        <div style="max-width: 600px; margin: 20px auto; padding: 25px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); font-family: Arial, sans-serif; line-height: 1.6;">
                            <h1 style="color: #3F2312; text-align: center; margin-bottom: 20px;">Order Report</h1>
                            <p style="color: #333;">Dear {{ name }},</p>
                            <p style="color: #333;">Here is the order report for the last month.</p>
                            <table style="width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 14px; background-color: #fff; border: 1px solid #ddd;">
                                <thead>
                                    <tr style="background-color: #3F2312; color: #fff;">
                                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Service Request ID</th>
                                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Professional Email</th>
                                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Date of Request</th>
                                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Date of Completion</th>
                                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Status</th>
                                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Rating</th>
                                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Remarks</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for req in requests %}
                                    <tr style="background-color: {% if loop.index % 2 == 0 %}#f2f2f2{% else %}#fff{% endif %};">
                                        <td style="padding: 10px; border: 1px solid #ddd;">{{ req.sevreq_id }}</td>
                                        <td style="padding: 10px; border: 1px solid #ddd;">{{ req.prof_email }}</td>
                                        <td style="padding: 10px; border: 1px solid #ddd;">{{ req.date_of_request }}</td>
                                        <td style="padding: 10px; border: 1px solid #ddd;">{{ req.date_of_completion }}</td>
                                        <td style="padding: 10px; border: 1px solid #ddd;">{{ req.sev_status }}</td>
                                        <td style="padding: 10px; border: 1px solid #ddd;">{{ req.rating }}</td>
                                        <td style="padding: 10px; border: 1px solid #ddd;">{{ req.remarks }}</td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                            <p style="color: #333; margin-top: 20px;">If you have any questions or need further details, please don't hesitate to contact us.</p>
                            <p style="color: #333;">Thank you for your attention!</p>
                            <p style="margin-top: 20px; color: #555;">Best regards,<br><strong>HomeWhiz Team</strong></p>
                        </div>
                        """)
                message = template.render(name=cust.cust_email.split("@")[0], requests = cust.cust_req )
                msg = Message(recipients=[cust.cust_email],html=message, subject=subject)
                conn.send(msg)
            sse.publish({"message": "Monthly report to users executed","color":"alert alert-primary" },type=cust.cust_email)
    print('monthly report to users executed')
    return {"status": "success",'message': "Monthly report to users executed"}

# ------- To schedule the tasks --------#
celery.conf.beat_schedule = {
    'my_daily_task': {
        'task': "main.daily_reminder_to_professional",
        'schedule': crontab(hour=21, minute=0),
    },
    'my_monthly_task': {
        'task': "main.monthly_report_to_customers",
        'schedule': crontab(day_of_month='1',hour=9, minute=0),
    }
}

@celery.task(name='Application.user_triggered_async_job')
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

#async trigger job
@app.route('/api/export-professional/<prof_email>', methods=['POST'])
@jwt_required()
def export_professional(prof_email):
    if not prof_email:
        return jsonify({'error': 'Professional email is required'}), 400
    var=user_triggered_async_job.delay(prof_email)
    print("triggered job",var)
    return jsonify({'message': 'Export job started successfully, you will be notified when it completes.'}), 202


with app.app_context():
    db.create_all()
    
if __name__=='__main__':
    app.run(host="0.0.0.0", port=8080)



