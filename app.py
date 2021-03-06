import os

from flask import Flask
from flask_restful import Resource, Api, reqparse

from resources.session_resource import Session
from resources.chart_resource import WeekChart, DayChart

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL?sslmode=require', 'sqlite:///papaoutai.db').replace('postgres://', 'postgresql://') # second value is default value
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
api = Api(app)


api.add_resource(Session, '/session')
api.add_resource(WeekChart, '/weekChart')
api.add_resource(DayChart, '/dayChart')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    #app.run(port=5000, debug=True)
    app.run(host='10.0.0.9', port=5000, debug=True)