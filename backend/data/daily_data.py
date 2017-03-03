from ..db import db

def pick(dictionary, keys):
    return { k: dictionary[k] for k in keys}

class DailyData:
    def __init__(self):
        self._entries = []

    @property
    def entries(self):
        return [pick(e, ['date', 'value']) for e in self._entries]

    def update(self):
        pass

    def set_entries(self, entries):
        self._entries = entries

    def db_write(self):
        db.daily.remove()
        db.daily.insert_many(self._entries)

    def db_read(self):
        entries = []
        key = {'type': self.data_type}
        cursor = db.daily.find()
        for row in cursor:
            entries.append(row)
        self.set_entries(entries)