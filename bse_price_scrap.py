import BeautifulSoup as bs
import json, time
from bse_codes import BSE_CODES_LIST
from mail_sender import SendMail
from common import *

outcome_df = pd.DataFrame(columns=COLUMNS)

def get_val(html, param):
    inp = html.find(id=param)
    val = inp.attrs[2][1].replace(',','')
    return val

def clean(info):
    x = info.replace('\r','').replace('\n','')
    return json.loads(x)['data'][0]

BASE_URL = 'http://www.bseindia.com/stock-share-price/SiteCache/52WeekHigh.aspx?Type=EQ&text={0}'
BASE_URL_2 = 'http://www.bseindia.com/stock-share-price/SiteCache/EQHeaderData.aspx?text={0}'
BASE_URL_3 = 'http://www.bseindia.com/SiteCache/1D/stkCompanyHeader.aspx?Type=BRD&text={0}'

def run_scrap_bse():
    for code in BSE_CODES_LIST:
        code = str(code)
        try:
            # For 52 week data
            #import ipdb; ipdb.set_trace()
            page = get_page(BASE_URL, code)
            html = bs.BeautifulSoup(page.content)
            high_52week = float(get_val(html, 'hdnHigh52'))
            low_52week = float(get_val(html, 'hdnLOW52'))
            # For last price
            page = get_page(BASE_URL_2, code)
            last_price = float(page.content.split(',')[-2])
            # For company name
            page = get_page(BASE_URL_3, code)
            company_name = page.content.split(',')[-1]
            reco = cond_check(last_price, low_52week, high_52week)
            if reco is not None:
                # Stock qualifies for being watched
                outcome_df.loc[outcome_df.shape[0]] = [company_name, last_price, high_52week, low_52week, code, reco]
        except Exception, e:
            print repr(e)
            logging.error("Error in BSE: " + repr(e) + " for code " + code)
        time.sleep(SLEEP)
    return outcome_df
