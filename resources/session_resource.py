from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from models.session_model import SessionModel
import datetime


class Session(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=str, required=True, help='This feild cannot be left blank or invalid format') 
    parser.add_argument("start_time", type=int, required=True, help='This feild cannot be left blank or invalid format')
    parser.add_argument("duration", type=int, required=True, help='This feild cannot be left blank or invalid format')
  
    def post(self):
        data = Session.parser.parse_args()
        session = SessionModel(data['user_id'], data['start_time'], data['duration'])
    
        try:
            session.save_to_db() 
            check_sessions = SessionModel.find_by_date_range(data['user_id'], datetime.date.fromtimestamp(data['start_time']), datetime.date.fromtimestamp(data['start_time']+23))
            if not check_sessions:
                raise Exception
            
        except Exception as e:
            print(e)
            return {"message": "An error occurred inserting the item"}, 500 

        return(session.json()), 201 

    



    
        



