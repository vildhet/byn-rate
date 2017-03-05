from datetime import datetime
import time
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

    def get(self):
        entries = []
        cursor = db.daily.find(self.key, {
            '_id': 0,
            'date': 1,
            'value': 1
        }).sort('date', 1)

        for row in cursor:
            entries.append(to_web_format(row))
        return entries

    def fetch(self):
        pass

    def update(self):
        db.daily.remove(self.key)
        entries = self.fetch()
        db.daily.insert_many(entries)
