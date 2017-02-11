import os
import os.path
from . import config

def init_application():
    print('Start application')
    if not os.path.exists(config.storage):
        os.makedirs(config.storage)

init_application()