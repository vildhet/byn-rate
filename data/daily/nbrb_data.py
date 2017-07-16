import requests
import time
from datetime import datetime, timedelta

from .daily_data import DailyData


API_INFO_URL = 'http://www.nbrb.by/API/ExRates/Currencies/'
API_DATA_URL = 'http://www.nbrb.by/API/ExRates/Rates/Dynamics/'

DATE_FORMAT = '%Y-%m-%d'
DATE_FULL_FORMAT = '%Y-%m-%dT%H:%M:%S'

# Max days allowed by API
YEAR_DAYS = 365

DENOMINATION_2016 = datetime(2016, 7, 1)
DENOMINATION_2000 = datetime(2000, 1, 1)


class NbrbData(DailyData):
    def __init__(self, data_type, currency):
        super().__init__(data_type)
        self.currency = currency

    def get_ranges(self):
        def parse(info):
            start_date = datetime.strptime(info['Cur_DateStart'], DATE_FULL_FORMAT)
            end_date = datetime.strptime(info['Cur_DateEnd'], DATE_FULL_FORMAT)

            return info['Cur_ID'], start_date, end_date

        info = requests.get(API_INFO_URL).json()
        return [parse(i) for i in info if i['Cur_Abbreviation'] == self.currency]

    def denominate(self, rate, date):
        if date < DENOMINATION_2000:
            return rate / 10000000
        if date < DENOMINATION_2016:
            return rate / 10000
        return rate

    def fetch_data(self, cur_id, start, end):
        days = (end - start).days
        assert days <= YEAR_DAYS, 'Invalid range: %s days' % days

        url = API_DATA_URL + str(cur_id)
        params = {
            'startDate': start.strftime(DATE_FORMAT),
            'endDate': end.strftime(DATE_FORMAT)
        }

        data = requests.get(url, params=params).json()

        entries = []
        for d in data:
            dt = datetime.strptime(d['Date'], DATE_FULL_FORMAT)

            rate = self.denominate(d['Cur_OfficialRate'], dt)
            assert rate < 3, 'Exchange rate on {} is {}'.format(dt, rate)

            # We are interested in trading results, not in the official rate on the next day
            dt -= timedelta(days=1)

            row = {
                'date': dt.strftime(DATE_FORMAT),
                'value': rate,
                'type': self.data_type
            }
            entries.append(row)
        return entries

    def fetch_range(self, cur_id, start, end):
        for d in [DENOMINATION_2000, DENOMINATION_2016]:
            if start < d and d <= end:
                r1 = self.fetch_range(cur_id, start, d - timedelta(days=1))
                r2 = self.fetch_range(cur_id, d, end)
                return r1 + r2

        year = timedelta(days=YEAR_DAYS)
        data_collection = []

        while start <= end:
            if start + year < end:
                current_end = start + year
            else:
                current_end = end

            d = self.fetch_data(cur_id, start, current_end)
            data_collection += d

            start = current_end + timedelta(days=1)
        return data_collection

    def fetch(self):
        ranges = self.get_ranges()
        entries = []

        for r in ranges:
            entries += self.fetch_range(*r)
        
        return entries
