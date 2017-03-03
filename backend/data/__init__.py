from .brent_data import BrentData

brent = BrentData()

def get_by_name(name):
    if name in globals():
        return globals()[name]
    return None

def read():
    brent.db_read()

read()