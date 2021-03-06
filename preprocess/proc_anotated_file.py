#!/usr/bin/env python

import sys
import json
import time
import pandas as pd
import preprocess as pre
import logging



f_excel = sys.argv[1]
f_json = f_excel.replace('.xlsx', '_preproc.json')
f_log = f_excel.replace('.xlsx', '_log.txt')

logging.basicConfig(filename=f_log, filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

df = pd.read_excel(f_excel)
df_tmp = df.copy()
# Clean up the title and text
for i, row in df_tmp.iterrows():
    id = df_tmp.loc[i, 'id']
    logging.warning('cleanup - ' + id)
    logger.handlers[0].flush()

    #clean up title
    title = df_tmp.loc[i, 'title']
    title = title.encode('ascii', 'backslashreplace')
    title = title.decode('utf8')
    title = pre.clean_text(title)
    df_tmp.loc[i, 'title'] = title

    #clean up text
    text = df_tmp.loc[i, 'text']
    text = text.encode('ascii', 'backslashreplace')
    text = text.decode('utf8')
    text = pre.clean_text(text)
    df_tmp.loc[i, 'text'] = text

# pre processed lowering
df_tmp['t_lower'] = ''
df_tmp['c_lower'] = ''
df_tmp['tc_lower'] = ''

for i, r in df_tmp.iterrows():
    id = df_tmp.loc[i, 'id']
    logging.warning('lower - ' + id)
    logger.handlers[0].flush()

    df_tmp.loc[i, 't_lower'] = df_tmp.loc[i, 'title'].lower()
    df_tmp.loc[i, 'c_lower'] = df_tmp.loc[i, 'text'].lower()
    df_tmp.loc[i, 'tc_lower'] = df_tmp.loc[i, 't_lower'] + " " + df_tmp.loc[i, 'c_lower']


# pre processed stop words removal
df_tmp['t_swrem'] = ''
df_tmp['c_swrem'] = ''
df_tmp['tc_swrem'] = ''

for i, r in df_tmp.iterrows():
    id = df_tmp.loc[i, 'id']
    logging.warning('swrem - ' + id)
    logger.handlers[0].flush()

    df_tmp.loc[i, 't_swrem'] = pre.rem_stop_words(df_tmp.loc[i, 't_lower'])
    df_tmp.loc[i, 'c_swrem'] = pre.rem_stop_words(df_tmp.loc[i, 'c_lower'])
    df_tmp.loc[i, 'tc_swrem'] = df_tmp.loc[i, 't_swrem'] + " " + df_tmp.loc[i, 'c_swrem']


# pre processed stemming
df_tmp['t_stem'] = ''
df_tmp['c_stem'] = ''
df_tmp['tc_stem'] = ''

for i, r in df_tmp.iterrows():
    id = df_tmp.loc[i, 'id']
    logging.warning('stem - ' + id)
    logger.handlers[0].flush()
    
    start = time.perf_counter()
    df_tmp.loc[i, 't_stem'] = pre.stem_text(df_tmp.loc[i, 't_lower'])
    df_tmp.loc[i, 'c_stem'] = pre.stem_text(df_tmp.loc[i, 'c_lower'])
    df_tmp.loc[i, 'tc_stem'] = df_tmp.loc[i, 't_stem'] + " " + df_tmp.loc[i, 'c_stem']

    diff = time.perf_counter() - start
    msg = f"elappsed time: {diff}" 
    logging.warning(msg)
    logger.handlers[0].flush()

# pre processed swrem stemming
df_tmp['t_swrem_stem'] = ''
df_tmp['c_swrem_stem'] = ''
df_tmp['tc_swrem_stem'] = ''

for i, r in df_tmp.iterrows():
    id = df_tmp.loc[i, 'id']
    print('swrem_stem - ' + id)

    df_tmp.loc[i, 't_swrem_stem'] = pre.stem_text(df_tmp.loc[i, 't_swrem'])
    df_tmp.loc[i, 'c_swrem_stem'] = pre.stem_text(df_tmp.loc[i, 'c_swrem'])
    df_tmp.loc[i, 'tc_swrem_stem'] = df_tmp.loc[i, 't_swrem_stem'] + " " + df_tmp.loc[i, 'c_swrem_stem']

# write to json  format
df_tmp.to_json(f_json, indent = True, orient = 'records')
