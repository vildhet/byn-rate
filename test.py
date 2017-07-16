#!/usr/bin/env python3


from datetime import datetime, timezone
import time
import json
from tabulate import tabulate

from data import daily as data
from predict import dumb_model

def print_table():
    dates = ['2017-07-07', '2017-07-08', '2017-07-09', '2017-07-10']
    daily_info = [data.get_by_date(d) for d in dates]

    names = sorted(list(daily_info[0].keys()))

    headers = ['Name'] + dates
    rows = []

    for name in names:
        row = [name] + [str(info[name]) for info in daily_info]
        rows.append(row)

    t = tabulate(rows, headers=headers, tablefmt='orgtbl')
    print(t)



# data.brent.fill_gaps()
# print_table()
dumb_model.get_training_data()
