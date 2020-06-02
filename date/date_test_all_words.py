import pandas as pd
import sys
from date_measurement import DateMeasurement as DM 
from date_tool import dt_search as dt_search

def refine_content_date(content_date, pub_date):
    if 0 < len(content_date):
        l_date = content_date.split('|')
        y_pub = pub_date[:4]
        for i, val in enumerate(l_date):
            if 10 > len(val):
                l_date[i] = y_pub + "-" + val
    else:
        l_date = [pub_date]

    l_date = list(set(l_date))
    return '|'.join(l_date)

def extract_date(pub_date_text, content_text):
    pub_date = dt_search.find_dates(pub_date_text, mmdd=False)
    content_date = dt_search.find_dates(content_text)    
    content_date = refine_content_date(content_date, pub_date)

    return pub_date, content_date


if __name__ == "__main__":
    f_in = sys.argv[1]
    df = pd.read_excel(f_in)

    for index, row in df.iterrows():
        pub_date_text = row['date']
        content_text = row['title'] + ' ' + row['content']
        pub_date, content_date = extract_date(pub_date_text, content_text)

        df.loc[index, 'pred_date_pub'] = pub_date
        df.loc[index, 'pred_date_text'] = content_date

        # prepare 
        ref_date = row['date_text']
        pred_date = content_date
        l_true = ref_date.split('|')
        l_pred = pred_date.split('|')

        # clean
        l_true = [ e.replace('\'', '') for e in l_true ]
        l_pred = [ e.replace('\'', '') for e in l_pred ]
        
        dm = DM(l_true, l_pred)
        df.loc[index, 'jc_sim'] = dm.jaccard_simmilarity()
        df.loc[index, 'pre'] = dm.precision()
        df.loc[index, 'rec'] = dm.recall()
        df.loc[index, 'f1'] = dm.f1_score()



    f_out = f_in.replace('.xlsx', '_rslt_all_words.xlsx')
    df.to_excel(f_out, index=False)
