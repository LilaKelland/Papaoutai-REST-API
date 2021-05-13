from flask import Flask
from flask_restful import Resource, Api, reqparse

from resources.session_resource import Session
from resources.chart_resource import WeekChart, DayChart

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///papaoutai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turns off flask sql alchemy not sql alcomy 
api = Api(app)

@app.before_first_request  # this addition will create tables rather than create_tables 
def create_tables():
    db.create_all()

api.add_resource(Session, '/session')
api.add_resource(WeekChart, '/weekChart')
api.add_resource(DayChart, '/dayChart')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    #app.run(port=5000, debug=True)
    app.run(host='192.168.4.29', port=8080, debug=True)