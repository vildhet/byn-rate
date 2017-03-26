#!/usr/bin/env python3


from backend.data import NbrbData

data = NbrbData('bynusd', 145)
data.fetch()

# print(d)