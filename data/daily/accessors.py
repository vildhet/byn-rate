from datetime import datetime, timezone, timedelta

DATE_FORMAT = '%Y-%m-%d'

class WebAccessor:
    def __init__(self, collection):
        self.collection = collection

    @staticmethod
    def format_entry(entry):
        dt = datetime.strptime(entry['date'], DATE_FORMAT)
        dt = dt.replace(tzinfo=timezone.utc)

        return {
            'x': int(dt.timestamp()),
            'y': entry['value']
        }

    def get_all(self):
        return [self.format_entry(e) for e in self.collection.yield_all()]


class BatchAccessor:
    def __init__(self, collections):
        assert len(collections) > 0
        self.collections = collections

    def yield_latest(self, days, to_date):
        sources = [(c.data_type, c.yield_latest(days, to_date)) for c in self.collections]

        for i in range(days):
            batch = dict()
            for s in sources:
                entry = next(s[1])

                if 'date' not in batch:
                    batch['date'] = entry['date']

                assert batch['date'] == entry['date']

                batch[s[0]] = entry['value']

            yield batch

    def get_latest(self, days, to_date=None):
        l = [e for e in self.yield_latest(days, to_date)]
        return list(reversed(l))

    def get_previous(self, date):
        dt = datetime.strptime(date, DATE_FORMAT)
        if dt.weekday() < 5:
            return self.get_latest(2, date)[0]
        else:
            # Date is a weekend
            return self.get_latest(1, date)[0]


class WorkdayAccessor(BatchAccessor):
    def __init__(self, collections):
        super().__init__(collections)

    def yield_latest(self, days, to_date):
        full_weeks = days // 5
        rest = days % 5

        total_days = full_weeks * 7

        if to_date:
            dt = datetime.strptime(to_date, DATE_FORMAT)
        else:
            dt = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        work_days = 0
        while work_days != rest:
            if dt.weekday() < 5:
                work_days += 1
            total_days += 1
            dt -= timedelta(days=1)

        for entry in super().yield_latest(total_days, to_date):
            dt = datetime.strptime(entry['date'], DATE_FORMAT)
            if dt.weekday() < 5:
                yield entry
        