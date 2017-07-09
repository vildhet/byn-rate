from .quandl_data import QuandlData
from .nbrb_data import NbrbData
from .daily_data import DailyData

brent = QuandlData('brent', 'CHRIS/ICE_B1', 'Settle')
eurrub = QuandlData('eurrub', 'ECB/EURRUB', 'Value')
bynusd = NbrbData('bynusd', 145)
byneur = NbrbData('byneur', 19)

def get_by_name(name):
    if name in globals():
        return globals()[name]
    return None

def get_all():
    return [d for d in globals().values() if isinstance(d, DailyData)]