from datetime import datetime, timezone


class WebAccessor:
    def __init__(self, collection):
        self.collection = collection

    @staticmethod
    def format_entry(entry):
        dt = datetime.strptime(entry['date'], '%Y-%m-%d')
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

    def yield_latest(self, size):
        sources = [(c.data_type, c.yield_latest(size)) for c in self.collections]

        for i in range(size):
            batch = dict()
            for s in sources:
                entry = next(s[1])

                if 'date' not in batch:
                    batch['date'] = entry['date']

                assert batch['date'] == entry['date'], str(batch) + ', ' +  str(entry) + ', ' + s[0]

                batch[s[0]] = entry['value']

            yield batch

    def get_latest(self, size):
        return [e for e in self.yield_latest(size)]