import pandas as pd
import re
import json
from collections import OrderedDict 
import sys

import prep_settings as st
sys.path.insert(1, st.preprocess_path)
import preprocess as pre

df_teks_ori = pd.read_excel(st.f_teks_ori)
df_analysis = df_teks_ori[['id', 'source', 'title']].copy()

def pre_news_raw_text(news_id):
    title_text = df_analysis.loc[df_analysis['id'] == news_id, 'title'].values[0]
    src_text = df_analysis.loc[df_analysis['id'] == news_id, 'source'].values[0]
    src_text = src_text + ".json"
    text_dir = st.d_news_text
    text_path = text_dir + st.d_delimiter + src_text

    special = r"(\W|\\u[\w][\w][\w][\w])*"
   
    title_text = title_text.replace('[', '\[')
    title_text = title_text.replace(']', '\]')
    title_text = title_text.replace('?', '\?')
    title_text = title_text.replace('(', '\(')
    title_text = title_text.replace(')', '\)')
    title_text = title_text.replace('.', '\.')
    title_text = title_text.replace(',', '\,')
    title_text = title_text.replace('"', '\",')
    
    title_text = title_text.replace(' ', special)
    re_title = r"title\":.*" + title_text + r".*(date|content)\""
    
    l_text = []
    with open(text_path) as f:
        l_text = [l for l in f if re.search(re_title, l)]

        for index, text in enumerate(l_text):
            tmp_text = text
            tmp_text = pre.clean_convertion(tmp_text)
            tmp_text = pre.clean_links_text(tmp_text)
            tmp_text = pre.clean_text(tmp_text)
            tmp_text = pre.clean_escape_char(tmp_text)

            ''' Clean up return line '''
            escape_char = re.compile(r'\\n')
            tmp_text = re.sub(escape_char, ' ', tmp_text, re.MULTILINE|re.IGNORECASE).strip()

            escape_char = re.compile(r'\\n')
            tmp_text = re.sub(escape_char, ' ', tmp_text, re.MULTILINE|re.IGNORECASE).strip()

            escape_char = re.compile(r'\\n')
            tmp_text = re.sub(escape_char, ' ', tmp_text, re.MULTILINE|re.IGNORECASE).strip()

            l_text[index] = tmp_text
                
    return list(OrderedDict.fromkeys(l_text))

def prep_news(l_text):
    l_news = []
    for t in l_text:
        text = t
        text = re.match('{.*}', text)
        
        try:
            json_obj = json.loads(text[0])
            content = json_obj['content']
            l_news.append(content)
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)

    return ' // '.join(l_news)

df_result = pd.DataFrame(columns = ['id', 'source', 'date', 'title', 'text'])
df_result['source'] = df_teks_ori['source'].copy()
df_result['date'] = df_teks_ori['date'].copy()

for index, row in df_analysis.iterrows():
    df_result.loc[index, 'id'] = df_analysis.loc[index, 'id']    
    df_result.loc[index, 'title'] = df_analysis.loc[index, 'title']
    
    text_id = df_analysis.loc[index, 'id']
    print(text_id)
    l_text = pre_news_raw_text(text_id)
    text = prep_news(l_text)
    df_result.loc[index, 'text'] = text

df_result.to_excel('result_' + st.news_type + '.xlsx', index=False)