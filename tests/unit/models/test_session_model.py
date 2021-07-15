from unittest import TestCase
from models.session_model import SessionModel
import datetime

class SessionModelTest(TestCase):

    def test_create_session_model(self):
        session = SessionModel('Test User Id', 1234, 4567)

        self.assertEqual(session.user_id, 'Test User Id', "The user id after creation does not equal the constructor argument.")
        self.assertEqual(session.start_time, 1234, "The sessionstart time after creation does not equal the constructor argument.")
        self.assertEqual(session.duration, 4567, "The sessionduration after creation does not equal the constructor argument.")

    def test_session_model_json(self):
        session = SessionModel('Test User Id', 1234, 4567)
        session_date = datetime.date.fromtimestamp(4567)

        expected = {
            'user_id': 'Test User Id', 
            'start_time': 1234,
            'duration': 4567,
            'start_date': session_date
        }

        self.assertEqual(session.json(), expected, "The JSON export of the session is incorrect.  Recieved {}, expected {}".format(session.json(), expected))


