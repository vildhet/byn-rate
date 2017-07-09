#!/usr/bin/env python3


from datetime import datetime, timezone
import time
import json
from backend.data import byneur as data

data.update()

print(data.get_latest())
