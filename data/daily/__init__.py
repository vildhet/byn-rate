from .quandl_data import QuandlData
from .nbrb_data import NbrbData
from .daily_data import DailyData

from .accessors import WebAccessor, BatchAccessor, WorkdayAccessor

brent = QuandlData('brent', 'CHRIS/ICE_B1', 'Settle')
eurrub = QuandlData('eurrub', 'ECB/EURRUB', 'Value')
bynusd = NbrbData('bynusd', 'USD')
byneur = NbrbData('byneur', 'EUR')

def get(name):
    if name in globals():
        return globals()[name]
    return None

def get_all():
    return [d for d in globals().values() if isinstance(d, DailyData)]
