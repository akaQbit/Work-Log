import re
from datetime import datetime
from datetime import timedelta


class WorkEntry:
    def __init__(self, task_name='default task', working_minutes=10, notes='default notes'):
        self.task_name = task_name
        self.working_minutes = working_minutes
        self.notes = notes
        self.creation_date = datetime.now()

    def get_date(self, fmt='%Y-%m-%d %H:%M'):
        return self.creation_date.strftime(fmt)

    def get_summary(self):
        arg_dic = {
            'date': self.get_date(),
            'name': self.task_name,
            'time': self.working_minutes,
            'note': self.notes
        }

        content = """
        Date : {date}
        Task : {name}
        Time : {time}
        Note : {note}
        """.format(**arg_dic)

        return content

    def is_on_date(self, date):
        return self.is_between_dates(date, date)

    def is_between_dates(self, start_date, end_date):
        return self.creation_date.timestamp() - start_date.timestamp() >= 0 and (end_date + timedelta(days=1)).timestamp() - self.creation_date.timestamp() > 0

    def is_between_work_time(self, lower_time, upper_time):
        return lower_time <= self.working_minutes <= upper_time

    def has_keyword(self, keyword):
        return self.task_name.__contains__(keyword) or self.notes.__contains__(keyword)

    def has_pattern(self, pattern):
        return re.search(pattern, self.task_name) or re.search(pattern, self.notes)
