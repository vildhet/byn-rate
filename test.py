#!/usr/bin/env python3


from datetime import datetime
from backend.data import NbrbData

data = NbrbData('bynusd', 145)

s = datetime(2016, 6, 29)
e = datetime(2016, 7, 1)
d = data.fetch_range(s, e)


print(d)