from nltk.tag import StanfordNERTagger
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

import pandas as pd
import timeit
import sys
import re

from ner_tool import NerTool

# re keywords based on file name
def re_string(text):
    re_keywords = ''
    if 'angin_topan' in text:
        re_keywords = r'badai|puting beliung|angin topan|tornado|angin kencang'
    elif 'banjir' in text:
        re_keywords = r'banjir'
    elif 'erupsi' in text:
        re_keywords = r'vulkanik|erupsi|letusan|awan panas|lava'
    elif 'gempa' in text:
        re_keywords = r'gempa|tektonik'
    elif 'karhutla'in text:
        re_keywords = r'kebakaran hutan|kebakaran lahan|titik panas'
    elif 'kekeringan'in text:
        re_keywords = r'kekeringan'
    elif 'longsor'in text:
        re_keywords = r'longsor'
    elif 'tsunami'in text:
        re_keywords = r'tsunami'
    else:
        re_keywords = 'XXXXXXXXXXXXXXXX'

    return re_keywords


f_in = sys.argv[1]
f_out = f_in.replace('.xlsx', '_ner_st_keywords.xlsx')

# Load gold standard
df_gold = pd.read_excel(f_in)

# Prepare df output
df_out = df_gold[[ 'id', ]].copy()
df_out['raw_ner'] = ''
df_out['exec_time'] = ''

# Create df only row wit label is 'Y'
df_data = df_gold[['id', 'title', 'content']]

# Initialize Ner tool
ner_model = 'C:\\Users\\dharmapu\\Documents\\personal\\ui\\KA-AMSD_src\\src\\text_processing\\ner-model\\idner-model-20k-mdee.ser.gz'
ner_app = 'C:\\Users\\dharmapu\Documents\\personal\\ui\\KA-AMSD_src\\src\\stanford-ner\\stanford-ner.jar'
ner_tool = NerTool(ner_model, ner_app)


# Ner processing and store output in df_out
for index, row in df_data.iterrows():
    row_id = row['id']
    row_text = row['title'] + ' ' + row['content']
    re_keywords = re_string(row_id)

    print(row_id)

    start_time = timeit.default_timer()
    sent_tokens = sent_tokenize(row_text)
    sent_valid = [ l for l in sent_tokens\
                      if None != re.search(re_keywords, l, flags=re.IGNORECASE) ]
    w_tokens = word_tokenize(' '.join(sent_valid))

    row_loc = ner_tool.parse_text(w_tokens)
    row_loc = ", ".join(row_loc)
    exec_time = timeit.default_timer() - start_time
    
    df_out.loc[df_out['id'] == row_id, 'raw_ner'] = row_loc
    df_out.loc[df_out['id'] == row_id, 'exec_time'] = exec_time

df_out.to_excel(f_out, index=False)
