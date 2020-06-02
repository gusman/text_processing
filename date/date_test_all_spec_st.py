import pandas as pd
import sys
import re
from date_measurement import DateMeasurement as DM 
from date_tool import dt_search as dt_search
from nltk.tokenize import sent_tokenize, word_tokenize

re_disaster = { 
    'gempa' : r'gempa|tektonik',
    'tsunami' : r'tsunami',
    'erupsi' : r'vulkanik|erupsi|letusan|awan panas|lava',
    'kekeringan' : r'kekeringan',
    'banjir' : r'banjir',
    'angin_topan' : r'badai|puting beliung|angin topan|tornado|angin kencang',
    'longsor' : r'longsor',
    'karhutla' : r'kebakaran hutan|kebakaran lahan|titik panas',
}


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

def get_re_string(text_id):
    ret = r''

    for k, v in re_disaster.items():
        if k in text_id.lower():
            ret = v
            break

    return ret
        
def filter_context_text(text_id, text):
    st_tokens = sent_tokenize(text)
    re_string = get_re_string(text_id)
    st_tokens = [ s for s in st_tokens if re.search(re_string, s.lower(), re.I) ]
    return ' '.join(st_tokens)


if __name__ == "__main__":
    f_in = sys.argv[1]
    df = pd.read_excel(f_in)

    for index, row in df.iterrows():
        text_id = row['id']
        pub_date_text = row['date']
        content_text = row['title'] + ' ' + row['content']
        content_text = filter_context_text(text_id, content_text)

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



    f_out = f_in.replace('.xlsx', '_rslt_spec_st.xlsx')
    df.to_excel(f_out, index=False)
