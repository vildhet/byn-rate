from .quandl_data import QuandlData

brent = QuandlData('brent', 'CHRIS/ICE_B1', 'Settle')
eurrub = QuandlData('eurrub', 'ECB/EURRUB', 'Value')

def get_by_name(name):
    if name in globals():
        return globals()[name]
    return None
