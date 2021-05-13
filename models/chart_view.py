from models.session_model import SessionModel
import datetime
import time
import math


class Day_Hours():
    def __init__(self, user_id, day):
        self.user_id = user_id
        self.day = day
        self.minutes_per_hour = {} #** order and send just a list over (x and y values separate)
        self._calc_hours_for_day()
        
    def get_day_chart(self):
        self._fill_in_empty_hours()
        week = Week(self.user_id, self.day)
        return  {"average_for_week": week.get_average_daily_bathrooming(),
       "minutes_per_hour": self.minutes_per_hour}
        #  "total_minutes": self.get_total_minutes(), 
        #  "label": self.day.strftime("%A, %b %d") 

    def get_total_minutes(self):
        return(sum(value for key, value in self.minutes_per_hour.items()))

    def _calc_hours_for_day(self):
        #TODO - deal with TypeError: 'NoneType' object is not iterable
        try:
            for row in self._find_sessions_for_day():
                self._split_session_into_hours(row.duration, row.start_time)
        except:
            self.minutes_per_hour = {0:0}

    def _find_sessions_for_day(self):
        try:
            return (SessionModel.find_by_date_range(self.user_id, self.day-datetime.timedelta(days = 1), self.day+ datetime.timedelta(days = 1)))
        except Exception as e:
            print(e)

    def _split_session_into_hours(self, duration, start_time):
        start_datetime = datetime.datetime.fromtimestamp(start_time)
        end_datetime = start_datetime + datetime.timedelta(seconds=duration)

        if end_datetime.hour < start_datetime.hour:
            end_hour = end_datetime.hour + 24
        else:
            end_hour = end_datetime.hour

        for count, session_hour in enumerate(range(start_datetime.hour, (end_hour + 1))):
            if count == 0:
                session_minutes = (60 - start_datetime.minute)  # TODO - this may result in over 60 min/ hour - floor this
                seconds_left = duration - session_minutes * 60
            
            else:
                if seconds_left >= 3600:
                    session_minutes = 60
                    seconds_left = seconds_left - 3600
                else:
                    session_minutes = math.floor(seconds_left / 60)

            if session_hour >= 24:
                session_hour -= 24
                session_day = (start_datetime + datetime.timedelta(days=1)).day
            else:
                session_day = start_datetime.day

            datetime_start_of_the_hour = datetime.datetime(start_datetime.year, start_datetime.month, session_day, session_hour)
            segment_date = datetime_start_of_the_hour.strftime('%Y-%m-%d')
            segment_hour = datetime_start_of_the_hour.strftime('%-H')
            
            if str(segment_date) == str(self.day):

                if segment_hour in self.minutes_per_hour:
                    self.minutes_per_hour.update({segment_hour: session_minutes + self.minutes_per_hour[segment_hour]})
                else:
                    self.minutes_per_hour.update({segment_hour: session_minutes})

    def _fill_in_empty_hours(self):
        for i in range (24):
            if i not in self.minutes_per_hour.keys():
                self.minutes_per_hour.update({i: 0})


class Week():
    def __init__(self, user_id, day):
        self.user_id = user_id
        self.day = day
        self.dayHours = Day_Hours(self.user_id, self.day)
        self.week_daily_totals = []
        self.weekday_abrvs = []
        self.days_of_month = []
        self.month = []
        self._calc_bathrooming_for_week()

    def get_week_chart(self):
        """returns chart x, y's and label formatted for chart"""
        if self.month[0] == self.month[len(self.month)-1]:
            label = f'{self.month[0]} {int(self.days_of_month[0])} - {int(self.days_of_month[len(self.days_of_month)-1])}' 
        else:
            label = f'{self.month[0]} {int(self.days_of_month[0])} - {self.month[len(self.days_of_month)-1]} {int(self.days_of_month[len(self.days_of_month)-1])}'
    
        return {"weekday_abrvs": self.weekday_abrvs, "label": label, "week_daily_totals": self.week_daily_totals, "week_avg": self.get_average_daily_bathrooming()}
       
    def get_week_total(self):
        return (sum(self.week_daily_totals))

    def get_average_daily_bathrooming(self):
        try:
            number_of_days_in_week = self._get_num_days_in_week()
        except:
            number_of_days_in_week = 0
            raise Exception
        if sum(self.week_daily_totals) != 0:
            return math.floor(sum(self.week_daily_totals) / number_of_days_in_week)
        return 0

    def _get_num_days_in_week(self):
        today_numeric_day_of_week = datetime.datetime.now().weekday()
        days_since_today = (datetime.date.today() - self.day).days
        print(days_since_today)
        if days_since_today > today_numeric_day_of_week:
            return 7
        return today_numeric_day_of_week + 1

    def _calc_bathrooming_for_week(self):
        """note this starts the week on monday - use strftime(%w) to start on Sun"""
        day_to_add = (self.day - datetime.timedelta(days=datetime.datetime.weekday(self.day))) # initialized to monday
        num_of_days_in_week = self._get_num_days_in_week()

        for _ in range(num_of_days_in_week):
            dayHours = Day_Hours(self.user_id, day_to_add)
            
            self.week_daily_totals.append(dayHours.get_total_minutes())
            self.weekday_abrvs.append(day_to_add.strftime("%a")[0])
            self.month.append(day_to_add.strftime("%b"))
            self.days_of_month.append(day_to_add.strftime("%d"))

            day_to_add += datetime.timedelta(days= 1)


class Weekly_Notification():
    def __init__(self, user_id, day):
        self.user_id = user_id
        self.day = day
        self.this_week = Week(user_id, day)
        self.last_week = Week(user_id, day-datetime.timedelta(days = 7))

    def find_percentage_difference(self):
        """only used on full weeks - or only call once week is complete"""
        this_week_total = self.this_week.get_week_total()

        if this_week_total != 0:
            return (
                this_week_total 
                / (this_week_total - self.last_week.get_week_total())
                * 100
            )
        return(0)

    def send_alert(self):
        percentage_difference = self.find_percentage_difference()
        direction = "decreased" if percentage_difference < 0 else "increased"

        return (f'Your bathromming time has {direction} {percentage_difference}%, now averaging {self.this_week.get_average_daily_bathrooming()} minutes per day')
    

    
       
    




