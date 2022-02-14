import pandas as pd
import re
import os

from datetime import date
from datetime import timedelta

from lxml import etree as ET
from lib.date_tool import dt_search as ds

DIR_DT_STAGING = '../date_extraction_staging'
DIR_DT_STAGING_TIMEX = f'{DIR_DT_STAGING}/indo_timex'

def extract_date(f_path):
    try:
        tree = ET.parse(f_path)

        text = tree.xpath('//TEXT/TIMEX3/@value')
        s_text = set([ds.find_dates(t, mmdd = False) for t in text if len(t) > 0])
        s_text = set([ e for e in s_text if len(e) > 0 ])

        creation_time = tree.xpath('//DCT/TIMEX3/text()')
        if 0 < len(creation_time):
            crt_date = date.fromisoformat(creation_time[0])    

            if 'PRESENT_REF' in text:
                present_text = crt_date.strftime("%Y-%m-%d")
                s_text.add(present_text)

            if 'FUTURE_REF' in text:
                prev_date = crt_date + timedelta(days = 1) 
                prev_date_text = prev_date.strftime("%Y-%m-%d")
                s_text.add(prev_date_text)

            if 'PAST_REF' in text:
                next_date = crt_date - timedelta(days = 1) 
                next_date_text = next_date.strftime("%Y-%m-%d")
                s_text.add(next_date_text)

        return '|'.join(s_text)
    except:
        return ''

if __name__ == "__main__":
    d_name = f'{DIR_DT_STAGING_TIMEX}/indo_timex_label'

    df = pd.DataFrame(columns=['id', 'date'])
    for f in os.listdir(d_name):
        f_path = f'{d_name}/{f}'
        article_id = re.sub('_timex.tml', '', f)
        row = [ article_id, extract_date(f_path) ]
        df.loc[len(df.index)] = row

    print(df)
    f_out = f'{DIR_DT_STAGING_TIMEX}/indo_timex_result.xlsx'
    df.to_excel(f_out, index=False)
