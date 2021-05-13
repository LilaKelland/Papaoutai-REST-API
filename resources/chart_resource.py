from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from models.chart_view import Day_Hours, Week
import datetime

class WeekChart(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=str, required=True, help='This feild cannot be left blank or invalid format') 
    parser.add_argument('day_in_timestamp', type=int, required=True, help='This feild cannot be left blank or invalid format')
  
    def post(self):
        data = WeekChart.parser.parse_args()
        week = Week(data['user_id'], datetime.date.fromtimestamp(data['day_in_timestamp']))
    
        try:
            return(week.get_week_chart())
        except:
            return {"message": "An error occurred retreiving from week_chart"}, 400

        
class DayChart(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=str, required=True, help='This feild cannot be left blank or invalid format') 
    parser.add_argument("day_in_timestamp", type=int, required=True, help='This feild cannot be left blank or invalid format')
  
    def post(self):
        data = DayChart.parser.parse_args()
        dayHours = Day_Hours(data['user_id'], datetime.date.fromtimestamp(data['day_in_timestamp']))
    
        try:
            return (dayHours.get_day_chart())
        except Exception as e:
            print(e)
            return {"message": "An error occurred retreiving from day_chart"}, 400