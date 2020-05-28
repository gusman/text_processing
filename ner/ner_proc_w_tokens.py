from nltk.tag import StanfordNERTagger
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

import pandas as pd
import timeit
import sys

from ner_tool import NerTool

f_in = sys.argv[1]
f_out = f_in.replace('.xlsx', '_ner_w_tokens.xlsx')

# Load gold standard
df_gold = pd.read_excel(f_in)

# Prepare df output
df_out = df_gold[[ 'id', ]].copy()
df_out['raw_ner'] = ''
df_out['exec_time'] = ''

# Create df only row wit label is 'Y'
df_data = df_gold[df_gold.label == 'Y'][['id', 'title', 'content']]

# Initialize Ner tool
ner_model = '/home/admin/text_processing/ner/model/idner-model-20k-mdee.ser.gz'
ner_app = '/home/admin/stanford-ner/stanford-ner.jar'
ner_tool = NerTool(ner_model, ner_app)

# Ner processing and store output in df_out
for index, row in df_data.iterrows():
    row_id = row['id']
    row_text = row['title'] + row['content']
    
    start_time = timeit.default_timer()
    w_tokens = word_tokenize(row_text)
    row_loc = ner_tool.parse_text(w_tokens)
    row_loc = ", ".join(row_loc)
    exec_time = timeit.default_timer() - start_time
    
    df_out.loc[df_out['id'] == row_id, 'raw_ner'] = row_loc
    df_out.loc[df_out['id'] == row_id, 'exec_time'] = exec_time

df_out.to_excel(f_out, index=False)
