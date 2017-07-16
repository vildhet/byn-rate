import tensorflow as tf

from data import daily
from data.daily import BatchAccessor

def get_training_data():
    batch = BatchAccessor(daily.get_all())
    print(batch.get_latest(3))