import re
from datetime import datetime, timedelta
import pytz

class TimeParser:
    def __init__(self):
        self.tz = pytz.timezone('Asia/Ho_Chi_Minh')
        self.day_mapping = {'hom nay': 0, 'hom qua': -1, 'mai': 1}
        self.weekday_mapping = {
            'thu hai': 0, 'thu ba': 1, 'thu tu': 2,
            'thu nam': 3, 'thu sau': 4, 'thu bay': 5, 'chu nhat': 6
        }
        self.time_period = {
            'sang': (6, 12), 'chieu': (12, 18),
            'toi': (18, 24), 'dem': (0, 6)
        }

    def parse_time_component(self, text):
        text_lower = text.lower()
        time_match = re.search(r'(\d{1,2}):?(\d{2})?\s*(h|gio|am|pm)?', text)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2)) if time_match.group(2) else 0
            if 'pm' in text_lower or 'chieu' in text_lower:
                if hour < 12:
                    hour += 12
            return (hour, minute)
        return (7, 0)

    def parse_date_component(self, text):
        text_lower = text.lower()
        now = datetime.now(self.tz)
        
        for day_name, offset in self.day_mapping.items():
            if day_name in text_lower:
                return (now + timedelta(days=offset)).date()
        
        for weekday_name, weekday_num in self.weekday_mapping.items():
            if weekday_name in text_lower:
                days_ahead = weekday_num - now.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                return (now + timedelta(days=days_ahead)).date()
        
        date_match = re.search(r'(\d{1,2})[/-](\d{1,2})(?:[/-](\d{2,4}))?', text)
        if date_match:
            day = int(date_match.group(1))
            month = int(date_match.group(2))
            year = int(date_match.group(3)) if date_match.group(3) else now.year
            if year < 100:
                year += 2000
            return datetime(year, month, day, tzinfo=self.tz).date()
        
        return now.date()

    def parse(self, text):
        date = self.parse_date_component(text)
        hour, minute = self.parse_time_component(text)
        dt = datetime(date.year, date.month, date.day, hour, minute, tzinfo=self.tz)
        return dt

    def parse_to_iso(self, text):
        dt = self.parse(text)
        return dt.isoformat()
