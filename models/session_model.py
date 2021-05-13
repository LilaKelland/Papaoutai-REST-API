from db import db
import datetime


class SessionModel(db.Model): # maps to db and objects (db.model)
    __tablename__ = 'session'

    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80))
    start_time = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    start_date = db.Column(db.Date)

    
    def __init__(self, user_id, start_time, duration):
        self.user_id = user_id
        self.start_time = start_time
        self.duration = duration
        self.start_date = datetime.date.fromtimestamp(self.start_time)

    def __repr__(self):
        return f'Session with user_id <{self.user_id}>, <{self.start_time}>, <{self.duration}>'

    def json(self):
        return {'user_id': self.user_id, 'start_time': self.start_time, 'duration': self.duration, 'start_date': datetime.date.strftime(self.start_date, '%b %d %Y')}#, 'start_datetime': self.start_datetime}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_date_range(cls, user_id, start, end):
        return(cls.query.filter(cls.start_date >= start, cls.start_date <= end, cls.user_id==user_id).all())

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

