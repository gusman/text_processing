from nltk.tag import StanfordNERTagger
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

import pandas as pd
import timeit
import sys

from lib.ner_tool import NerTool

DIR_LOC_STAGING = '../location_extraction_staging'
DIR_NER_OUTPUT = f'{DIR_LOC_STAGING}/ner_output'
NER_MODEL = './lib/ner-model/idner-model-20k-mdee.ser.gz'
NER_APP = './lib/stanford-ner/stanford-ner.jar'

if __name__ == '__main__':
    f_in = f'{DIR_LOC_STAGING}/loc_analysis_text.xlsx'
    f_out = f'{DIR_NER_OUTPUT}/ner_out_w_tokens.xlsx'

    # Load gold standard
    df_gold = pd.read_excel(f_in)

    # Prepare df output
    df_out = df_gold[[ 'id', ]].copy()
    df_out['raw_ner'] = ''
    df_out['exec_time'] = ''

    # Create df only row wit label is 'Y'
    df_data = df_gold[['id', 'title', 'content']]

    # Initialize Ner tool
    ner_tool = NerTool(NER_MODEL, NER_APP)

    # Ner processing and store output in df_out
    for index, row in df_data.iterrows():
        row_id = row['id']
        row_text = row['title'] + row['content']

        print(row_id)

        start_time = timeit.default_timer()
        w_tokens = word_tokenize(row_text)
        row_loc = ner_tool.parse_text(w_tokens)
        row_loc = ", ".join(row_loc)
        exec_time = timeit.default_timer() - start_time
        
        df_out.loc[df_out['id'] == row_id, 'raw_ner'] = row_loc
        df_out.loc[df_out['id'] == row_id, 'exec_time'] = exec_time

    print(df_out)
    df_out.to_excel(f_out, index=False)
