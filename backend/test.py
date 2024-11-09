from flask import Flask
from application.database import db
from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from celery.schedules import crontab
# from config import LocalDevelopmentConfig
from celery import Celery
from send_mail import init_mail
from flask_mail import Message
from flask_sse import sse
from functools import wraps
from jinja2 import Template

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

app.config["REDIS_URL"] = "redis://localhost"

app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'      
app.config['CACHE_REDIS_PORT'] = 6379             
app.config['CACHE_REDIS_DB'] = 0

jwt = JWTManager(app)

db.init_app(app=app) #object.method(parameter)

app.app_context().push()

from application.controllers import *


from flask import send_file
import csv
import io
from celery import Celery

# Initialize Celery
celery = Celery('tasks', broker='redis://localhost:6379/0')

@app.route('/api/export-products')
def export_products():
  # Trigger celery task and wait for result
  task_result = user_triggered_async_job.delay()
  result = task_result.get()  # Wait for task completion
  
  # Create in-memory file
  si = io.StringIO()
  cw = csv.writer(si)
  
  # Write header
  cw.writerow(result['header'])
  
  # Write content
  for item in result['content']:
      cw.writerow([
          item['name'],
          item['quantity'],
          item['manufacture'],
          item['expiry'],
          item['rpu']
      ])
  
  # Create binary stream
  output = io.BytesIO()
  output.write(si.getvalue().encode('utf-8'))
  output.seek(0)
  
  return send_file(
      output,
      mimetype='text/csv',
      as_attachment=True,
      download_name='product_report.csv'
  )

@celery.task()
def user_triggered_async_job():
  header = ["Product Name", "Product Quantity", "Product Manufacturing Date", 
            "Product Expiry Date", "Product RPU"]
  
  content = []
  for product in Product.query.all():
      item = {
          'name': product.name,
          'quantity': product.quantity,
          'manufacture': product.manufacture.strftime('%Y-%m-%d'),
          'expiry': product.expiry.strftime('%Y-%m-%d'),
          'description': product.description,
          'rpu': product.rpu,
      }
      content.append(item)
  
  return {'header': header, 'content': content}




