import pandas as pd
import requests

SLEEP = 1.0 # Can also use 0.2 to test
PERCENT_FROM_LOW = 20
PERCENT_FROM_HIGH = 15
LOW_FROM_HIGH = 20
COLUMNS = ['Company', 'LastPrice', '52week H', '52week L', 'Code','Reco']

import logging
logging.basicConfig(filename='scrap.log',level=logging.WARNING)

RECO_LIST = {
    'Near Low': 'Near Low', 
    'Critical': 'Critical',
    'Big Dip': 'Big Dip', 
}

def get_page(BASE_URL, code):
    url = BASE_URL.format(code)
    page = requests.get(url)
    return page

def cond_check(last_price, low_52week, high_52week):
    low_factor = 1.0 + PERCENT_FROM_LOW/100.0
    high_factor = 1.0 - PERCENT_FROM_HIGH/100.0
    low_from_high = 1.0 - LOW_FROM_HIGH/100.0
    if (low_52week*low_factor > last_price) and \
        (high_52week*high_factor > last_price):
        # Stocks to watch
        return RECO_LIST['Near Low']
    elif (low_52week*1.1 > last_price):
        # Critical cases
        return RECO_LIST['Critical']
    elif (high_52week * low_from_high) > last_price:
        return RECO_LIST['Big Dip']
    return None
