#!/usr/bin/env python3


from datetime import datetime, timezone
import time
import json
from tabulate import tabulate

from data import daily
from data.daily import BatchAccessor
from predict import dumb_model

def print_table():
    accessor = BatchAccessor(daily.get_all())
    info = accessor.get_latest(5, '2017-07-10')
    info = list(reversed(info))

    names = sorted([k for k in info[0].keys() if k != 'date'])

    headers = ['Name'] + [i['date'] for i in info]
    rows = []

    for name in names:
        row = [name] + [str(i[name]) for i in info]
        rows.append(row)

    t = tabulate(rows, headers=headers, tablefmt='orgtbl')
    print(t)



# data.brent.fill_gaps()
# print_table()
dumb_model.get_training_data()
