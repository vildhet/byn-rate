import tensorflow as tf

from data import daily
from data.daily import WorkdayAccessor

def get_training_data():
    batch = WorkdayAccessor([daily.bynusd])
    print(batch.get_latest(3))