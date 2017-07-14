#!/usr/bin/env python3


from datetime import datetime, timezone
import time
import json
from tabulate import tabulate

from data import daily as data


dates = ['2017-07-10', '2017-07-11', '2017-07-12', '2017-07-13', '2017-07-14']
daily_info = [data.get_by_date(d) for d in dates]

names = sorted(list(daily_info[0].keys()))

headers = ['Name'] + dates
rows = []

for name in names:
    row = [name] + [str(info[name]) for info in daily_info]
    rows.append(row)

t = tabulate(rows, headers=headers, tablefmt='orgtbl')
print(t)