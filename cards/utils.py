import json
import datetime
import time


def convert_timestamp(object):
    if isinstance(object, (datetime.datetime)):
        return object.timestamp()