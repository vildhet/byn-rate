import requests
from .daily_data import DailyData

API_LINK = 'https://www.quandl.com/api/v1/datasets/CHRIS/ICE_B1.json'

class BrentData(DailyData):
    def __init__(self):
        super().__init__()

    @property
    def data_type(self):
        return 'brent'

    def update(self):
        api_data = requests.get(API_LINK).json()

        date_index = api_data['column_names'].index('Date')
        value_index = api_data['column_names'].index('Settle')

        self.data = []
        for d in api_data['data']:
            row = {
                'date': d[date_index],
                'value': d[value_index],
                'type': self.data_type
            }
            self.data.append(row)
        
        
