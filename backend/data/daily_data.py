from datetime import datetime
import time

from .. import utils
from ..db import db

def to_web_format(entry):
    return {
        'x': entry['date'],
        'y': entry['value']
    }

class DailyData:
    def __init__(self, data_type):
        self.data_type = data_type

    @property
    def key(self):
        return {
            'type': self.data_type
        }

    def get_web(self):
        cursor = db.daily.find(self.key, {
            '_id': 0,
            'date': 1,
            'value': 1
        }).sort('date', 1)
        return [to_web_format(row) for row in cursor]

    def get_all(self):
        cursor = db.daily.find(self.key)
        return [row for row in cursor]

    def get_latest(self):
        return db.daily.find_one(self.key, sort=[('date', -1)])

    def get_by_date(self, date):
        dt = datetime.strptime(date, '%Y-%m-%d')
        ts = utils.utc_timestamp(dt)

        return db.daily.find_one({
            'type': self.data_type,
            'date': ts
        })

    def fetch(self):
        pass

    def update(self):
        db.daily.remove(self.key)
        entries = self.fetch()
        db.daily.insert_many(entries)
