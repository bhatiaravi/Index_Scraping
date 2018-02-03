import BeautifulSoup as bs
import json, time
from nse_codes import NSE_CODES_LIST, NSE_SME_CODES
from common import *

outcome_df = pd.DataFrame(columns=COLUMNS)

def clean(info):
    x = info.replace('\r','').replace('\n','')
    return json.loads(x)['data'][0]

def run_scrap_nse():
    # for NSE MAIN
    BASE_URL = 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol={0}&illiquid=0&smeFlag=0&itpFlag=0'
    for code in NSE_CODES_LIST:
        page = get_page(BASE_URL, code)
        html = bs.BeautifulSoup(page.content)
        resp = html.find(id='responseDiv')
        info = resp.contents[0]
        try:
            useful_info = clean(info)
            company_name = useful_info['companyName']
            last_price = float(useful_info['lastPrice'].replace(',',''))
            low_52week = float(useful_info['low52'].replace(',',''))
            high_52week = float(useful_info['high52'].replace(',',''))
            price_change = float(useful_info['pChange'].replace(',',''))
            reco = cond_check(last_price, low_52week, high_52week)
            # import ipdb; ipdb.set_trace()
            if reco is not None:
                # Stock qualifies for being watched
                outcome_df.loc[outcome_df.shape[0]] = [company_name, last_price, high_52week, low_52week, code, price_change, reco]
            time.sleep(SLEEP)
        except Exception, e:
            print repr(e)
            logging.error("Error in NSE: " + repr(e) + " for code " + code)
    # TODO: NSE SME
    BASE_URL_SME = 'https://www.nseindia.com/emerge/live_market/dynaContent/live_watch/get_quote_SME/GetSMEQuote.jsp?symbol={0}'
    for code in NSE_SME_CODES:
        page = get_page(BASE_URL_SME, code)
        html = bs.BeautifulSoup(page.content)
        resp = html.find(id='responseDiv')
        info = resp.contents[0]
        try:
            useful_info = clean(info)
            company_name = useful_info['companyName']
            last_price = float(useful_info['lastPrice'].replace(',',''))
            low_52week = float(useful_info['low52'].replace(',',''))
            high_52week = float(useful_info['high52'].replace(',',''))
            price_change = float(useful_info['pChange'].replace(',',''))
            reco = cond_check(last_price, low_52week, high_52week)
            if reco is not None:
                # Stock qualifies for being watched
                outcome_df.loc[outcome_df.shape[0]] = [company_name, last_price, high_52week, low_52week, code, price_change, reco]
            time.sleep(SLEEP)
        except Exception, e:
            print repr(e)
            logging.error("Error in NSE SME: " + repr(e) + " for code " + code)
    return outcome_df
