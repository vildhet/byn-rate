#!/usr/bin/env python3

from backend.data import BrentData



data = BrentData()
data.db_read()
print(data.data)
