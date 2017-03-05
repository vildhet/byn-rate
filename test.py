#!/usr/bin/env python3

from backend import data

data.eurrub.update()
print(data.eurrub.get())