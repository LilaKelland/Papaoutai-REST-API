from models.session_model import SessionModel
from tests.base_test import BaseTest

class SessionModelTest(Test):
    def test_crud(self):
        with self.app_context():
            session = SessionModel('Test User Id', 1234, 4567)
            
            self.assertIsNone(SessionModel.find_by_date_range('Test User Id', 0, 100000))
            session.save_to_db()

            self.assertIsNotNone(SessionModel.find_by_date_range('Test User Id', 0, 100000))