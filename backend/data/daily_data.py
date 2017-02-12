from ..db import db

class DailyData:
    def __init__(self):
        self.data = []

    def update(self):
        pass

    def db_write(self):
        db.daily.remove()
        db.daily.insert_many(self.data)

    def db_read(self):
        key = {'type': self.data_type}
        data = db.daily.find()
        for row in data:
            self.data.append(row)
