import nse_price_scrap
import bse_price_scrap
import pandas as pd
from common import PERCENT_FROM_LOW, PERCENT_FROM_HIGH
from mail_sender import SendMail
import os

# To enable cron execution
curr_dir = os.path.dirname(os.path.realpath(__file__)) + '/'
try:
    df1 = nse_price_scrap.run_scrap_nse()
    df2 = bse_price_scrap.run_scrap_bse()

    outcome_df = pd.concat([df1, df2])
    todays_codes = list(outcome_df['Code'].values)

    f = open(curr_dir + 'old_entries','r')
    old_entries = f.read()
    if old_entries != '':
        old_entries = old_entries.split(',')
    else: 
        old_entries = []
    f.close()

    f = open(curr_dir + 'old_entries', 'w')
    t = todays_codes
    t.extend(old_entries)
    m = list(set(t))
    final = ",".join(m)
    #import ipdb; ipdb.set_trace()
    f.write(final)
    f.close()

    for code in todays_codes:
        if code not in old_entries:
            outcome_df.loc[outcome_df['Code'] == code, 'Reco'] = outcome_df.loc[outcome_df['Code'] == code, 'Reco'] + ' #NEW'
    sub = 'Stocks within ' + str(PERCENT_FROM_LOW) + '% of 52 week'

    SendMail(subject=sub, table=outcome_df.to_html().replace('&lt;','<').replace('&gt;','>'))
except Exception, e:
    SendMail(subject=repr(e))
