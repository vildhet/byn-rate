import requests
import time
from datetime import datetime

from .daily_data import DailyData


API_LINK = 'https://www.quandl.com/api/v1/datasets/'


class QuandlData(DailyData):
    def __init__(self, data_type, code, value_column):
        super().__init__(data_type)
        self.code = code
        self.value_column = value_column

    def fetch(self):
        link = API_LINK + self.code + '.json'
        api_data = requests.get(link).json()

        date_index = api_data['column_names'].index('Date')
        value_index = api_data['column_names'].index(self.value_column)

        entries = []
        for d in api_data['data']:
            dt = datetime.strptime(d[date_index], '%Y-%m-%d')
            timestamp = int(time.mktime(dt.timetuple()))
            row = {
                'date': timestamp,
                'value': d[value_index],
                'type': self.data_type
            }
            entries.append(row)
        return entries