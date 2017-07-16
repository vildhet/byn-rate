import pymongo
import time
from datetime import datetime, timedelta

from ..db import db


class DailyData:
    def __init__(self, data_type):
        self.data_type = data_type

        self._key = {
            'type': self.data_type
        }

        self._filter = {
            '_id': 0,
            'date': 1,
            'value': 1
        }

    def yield_all(self):
        cursor = db.daily.find(self._key, self._filter).sort('date', pymongo.ASCENDING)
        yield from cursor

    def yield_latest(self, n):
        cursor = db.daily.find(self._key, self._filter).sort('date', pymongo.DESCENDING).limit(n)
        yield from cursor

    def get_by_date(self, date):
        row = db.daily.find_one({
            'type': self.data_type,
            'date': date
        })

        return row['value'] if row else None

    def fetch(self):
        pass

    def fill_gaps(self):
        cursor = db.daily.find(self._key).sort('date', pymongo.ASCENDING)
        previous = next(cursor)

        to_insert = list()

        def fill_to_date(entry, date):
            next_date = datetime.strptime(entry['date'], '%Y-%m-%d') + timedelta(days=1)

            while date != next_date:
                to_insert.append({
                    'date': next_date.strftime('%Y-%m-%d'),
                    'value': entry['value'],
                    'type': entry['type']
                })
                next_date += timedelta(days=1)

        for entry in cursor:
            current_date = datetime.strptime(entry['date'], '%Y-%m-%d')
            fill_to_date(previous, current_date)
            previous = entry

        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        fill_to_date(previous, today + timedelta(days=1))

        db.daily.insert_many(to_insert)

    def update(self):
        entries = self.fetch()
        db.daily.remove(self._key)
        db.daily.insert_many(entries)
        self.fill_gaps()
