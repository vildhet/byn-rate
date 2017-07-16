import requests
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
        params = {
            'api_key': '7CJj7Ta3hx_KtdBZpnxR'
        }
        api_data = requests.get(link, params=params).json()

        date_index = api_data['column_names'].index('Date')
        value_index = api_data['column_names'].index(self.value_column)

        entries = []
        for d in api_data['data']:
            row = {
                'date': d[date_index],
                'value': d[value_index],
                'type': self.data_type
            }
            entries.append(row)
        return entries