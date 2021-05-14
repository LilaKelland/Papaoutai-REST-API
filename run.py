from app import app
from db import db

db.init_app(app)

@app.before_first_request  # this addition will create tables rather than create_tables 
def create_tables():
    db.create_all()