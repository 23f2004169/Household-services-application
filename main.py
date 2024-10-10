from flask import Flask
import os
from application.database import *

#current working directory
cwd=os.getcwd()
basedir=os.path.abspath(os.path.dirname(__file__))

#creates app instance -object of flask
app=Flask(__name__)
db_path=os.path.join(basedir,"database_files/household_services.db")

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///"+db_path
db.init_app(app=app) #object.method(parameter)

#pushing app context globally to flask class file app -direct access of app for other modules(db)
app.app_context().push()

from application.controllers import *

if __name__=='__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)