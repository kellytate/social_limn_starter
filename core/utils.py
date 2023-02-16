from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Entry, User
class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year=year
        self.month=month
        super(Calendar, self).__init__()

    def formatDay(self, day, entries):
        entries_per_day = entries.filter(created_at__day = day)
        d=''
        for entry in entries_per_day: d+= f'<li class="cal_list"><{entry.get_html_url}</li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul>{d}</ul></td>"
        return '<td></td>'
    
    def formatWeek(self, theweek, entries):
        week = ''
        for d, weekday in theweek:
            week += self.formatDay(d,entries)
        return f'<tr>{week}</tr>'
    
    def formatmonth(self,user ,withyear=True,):
        entries = Entry.objects.filter(user=user).filter(created_at__year=self.year, created_at__month=self.month)
        cal =f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        call += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, entries)}\n'
        return cal