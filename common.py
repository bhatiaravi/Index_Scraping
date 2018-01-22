import pandas as pd
import requests

SLEEP = 1.0 # Can also use 0.2 to test
PERCENT_FROM_LOW = 20
PERCENT_FROM_HIGH = 15
LOW_FROM_HIGH = 18
COLUMNS = ['Company', 'LastPrice', '52week H', '52week L', 'Code','Reco']


import logging
logging.basicConfig(filename='scrap.log',level=logging.WARNING)

RECO_LIST = {
    'Near Low': '{0}% from Low', 
    'Critical': 'Critical - {0}% from Low',
    'Big Dip': 'Big Dip - {0}% from High', 
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
        low_percent = (last_price - low_52week)*100.0/low_52week
        return RECO_LIST['Near Low'].format(str(round(low_percent, 2)))
    elif (low_52week*1.1 > last_price):
        # Critical cases
        low_percent = (last_price - low_52week)*100.0/low_52week
        return RECO_LIST['Critical'].format(str(round(low_percent)))
    elif (high_52week * low_from_high) > last_price:
        dip_percent = (high_52week - last_price)*100.0/high_52week
        return RECO_LIST['Big Dip'].format(str(round(dip_percent)))
    return None

def pe_details():
    PE_DF_COLS = ['Company', 'Sector', 'PE', 'Sector_PE']
    PE_DETAILS_URL = 'https://www.nseindia.com/homepage/peDetails.json'
    pe_detail = requests.get(PE_DETAILS_URL).content
    pe_detail = json.loads(pe_detail)
    pe_array = []
    for comp in pe_detail:
        pe = float(pe_detail[comp]['PE'].strip().replace('"',''))
        sector_pe = float(pe_detail[comp]['sectorPE'].strip().replace('"',''))
        pe_array.append([comp, pe_detail[comp]['sector'], pe, sector_pe])
    df_pe = pd.DataFrame(pe_array, columns=PE_DF_COLS)
    # Alert based on pe
    df_pe_alert = df_pe[(df_pe.PE < df_pe.Sector_PE) & (df_pe.PE > 0.1)]
    return df_pe, df_pe_alert
