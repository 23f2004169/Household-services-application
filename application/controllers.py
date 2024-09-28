from flask import current_app as app #alias for current running app
from flask import render_template,url_for,redirect,request
from application.models import *
from datetime import datetime,date
import decimal

@app.route("/")
def home():
    return render_template("index.html")
