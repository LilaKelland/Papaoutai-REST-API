"""
BaseTest

Parent class to each non-unit test.
Ensures a new blank database each time.
"""

from unittest import TestCase
from app import app
from db import db

class BaseTest(TestCase):
    def setUp(self):
        #make sure db exisits
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        with app.app_context(): #loads flask app stuff
            db.init_app(app)
            db.create_all()
        #get test client (of the app)
        self.app = app.test_client()
        self.app_context = app.app_context
        

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()