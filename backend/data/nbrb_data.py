import requests
import time
from datetime import datetime, timedelta

from .. import utils
from .daily_data import DailyData


API_INFO_URL = 'http://www.nbrb.by/API/ExRates/Currencies/'
API_DATA_URL = 'http://www.nbrb.by/API/ExRates/Rates/Dynamics/'

DATE_FORMAT = '%Y-%m-%d'
DATE_FULL_FORMAT = '%Y-%m-%dT%H:%M:%S'

# Max days allowed by API
YEAR_DAYS = 365

DENOMINATION_2016 = datetime(2016, 7, 1)
DENOMINATION_2000 = datetime(2000, 1, 1)

def info_request(func):
    def wrapper(self, *args, **kwargs):
        if not self.info:
            self.update_info()
        return func(self, *args, **kwargs)
    return wrapper


class NbrbData(DailyData):
    def __init__(self, data_type, cur_id):
        super().__init__(data_type)
        self.cur_id = cur_id
        self.info = None

    def update_info(self):
        url = API_INFO_URL + str(self.cur_id)
        self.info = requests.get(url).json()

    @info_request
    def get_start_date(self):
        date = self.info['Cur_DateStart']
        return datetime.strptime(date, DATE_FULL_FORMAT)

    def denominate(self, rate, date):
        if date < DENOMINATION_2000:
            return rate / 10000000
        if date < DENOMINATION_2016:
            return rate / 10000
        return rate

    def fetch_data(self, start, end):
        days = (end - start).days
        assert days <= YEAR_DAYS, 'Invalid range: %s days' % days

        url = API_DATA_URL + str(self.cur_id)
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

            row = {
                'date': utils.utc_timestamp(dt),
                'value': rate,
                'type': self.data_type
            }
            entries.append(row)
        return entries

    def fetch_range(self, start, end):
        for d in [DENOMINATION_2000, DENOMINATION_2016]:
            if start < d and d <= end:
                r1 = self.fetch_range(start, d - timedelta(days=1))
                r2 = self.fetch_range(d, end)
                return r1 + r2

        year = timedelta(days=YEAR_DAYS)
        data_collection = []

        while start <= end:
            if start + year < end:
                current_end = start + year
            else:
                current_end = end

            d = self.fetch_data(start, current_end)
            data_collection += d

            start = current_end + timedelta(days=1)
        return data_collection

    def fetch(self):
        start = self.get_start_date()
        today = datetime.today()
        
        return self.fetch_range(start, today)
