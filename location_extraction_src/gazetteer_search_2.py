import pandas as pd
import sys
import os

from lib.gazetteer_loc import GazetteerAdmLoc as GZTR

DIR_LOC_STAGING = '../location_extraction_staging'
DIR_NER_OUTPUT = f'{DIR_LOC_STAGING}/ner_output'
DIR_NER_GZTR_OUTPUT = f'{DIR_LOC_STAGING}/gazetteer_output'

GZTR_ADM1 = './lib/gazetteer/prov_gazetteer.csv'
GZTR_ADM2 = './lib/gazetteer/kota_kab_gazetteer.csv'
GZTR_ADM3 = './lib/gazetteer/kecamatan_gazetteer.csv'

def search_in_gazetteer(sr_locs):
    dict_adm1 = {}
    dict_adm2 = {}
    dict_adm3 = {}
       
    for index, item in sr_locs.iteritems():
        loc_id, loc_str = gztr.search_gazetteer_by_name(4, index, sr_locs, 1)
        if None != loc_id and loc_id not in dict_adm1:
            dict_adm1[loc_id] = loc_str
        gztr.adm1_keys_filter = list(dict_adm1.keys())
        
    for index, item in sr_locs.iteritems():
        loc_id, loc_str = gztr.search_gazetteer_by_name(4, index, sr_locs, 2)
        if None != loc_id and loc_id not in dict_adm2:
            dict_adm2[loc_id] = loc_str
        gztr.adm2_keys_filter = list(dict_adm2.keys())
    
    for index, item in sr_locs.iteritems():
        loc_id, loc_str = gztr.search_gazetteer_by_name(4, index, sr_locs, 3)
        if None != loc_id and loc_id not in dict_adm3:
            dict_adm3[loc_id] = loc_str
            
    return dict_adm1, dict_adm2, dict_adm3

def consolidate_location(dict_adm1, dict_adm2, dict_adm3):
    adm1_str = ''
    adm2_str = ''
    adm3_str = ''

    # List of adm 3
    tmp_list = list(dict_adm3.values())
    if 0 < len(tmp_list):
        adm3_str = ', '.join(tmp_list)
    
    # list of adm 2
    adm3_keys = [ ".".join(k.split('.')[:-1]) for k in list(dict_adm3.keys()) ]
    new_adm2_keys = [ k for k in adm3_keys if k not in dict_adm2 ]
    sr_id = pd.Series(new_adm2_keys)
    for index, item in sr_id.iteritems():
        loc_id, loc_str = gztr.search_gazetteer_by_id(1, index, sr_id, 2)
        if None != loc_id and None != loc_str:
            dict_adm2[loc_id] = loc_str
        
    tmp_list = list(dict_adm2.values())
    if 0 < len(tmp_list):
        adm2_str = ', '.join(tmp_list)
    
    # list of adm 1
    adm2_keys = [ ".".join(k.split('.')[:-1]) for k in list(dict_adm2.keys()) ]
    new_adm1_keys = [ k for k in adm2_keys if k not in dict_adm1 ]
    sr_id = pd.Series(new_adm1_keys)
    for index, item in sr_id.iteritems():
        loc_id, loc_str = gztr.search_gazetteer_by_id(1, index, sr_id, 1)
        if None != loc_id and None != loc_str:
            dict_adm1[loc_id] = loc_str
        
    tmp_list = list(dict_adm1.values())
    if 0 < len(tmp_list):
        adm1_str = ', '.join(tmp_list)
    
    return adm1_str, adm2_str, adm3_str

if __name__ == "__main__":
    # Prepared dataframe
    f_in = sys.argv[1]
    
    df_ner = pd.read_excel(f_in)
    df_data = df_ner[df_ner.raw_ner.notnull()].copy()
    
    df_out = df_ner[['id']].copy()
    df_out['adm1'] = ''
    df_out['adm2'] = ''
    df_out['adm3'] = ''
    
    # Initilize gazetteer
    gztr = GZTR(GZTR_ADM1, GZTR_ADM2, GZTR_ADM3)
    
    dict_adm1 = {}
    dict_adm2 = {}
    dict_adm3 = {}

    for index, row in df_data.iterrows():
        row_id = row['id']
        sr_locs = pd.Series([ l.strip() for l in row['raw_ner'].split(',')])
        dict_adm1, dict_adm2, dict_adm3 = search_in_gazetteer(sr_locs)

        adm1_str, adm2_str, adm3_str =\
            consolidate_location(dict_adm1, dict_adm2, dict_adm3)

        df_out.loc[df_out['id'] == row_id, 'adm1'] = adm1_str
        df_out.loc[df_out['id'] == row_id, 'adm2'] = adm2_str
        df_out.loc[df_out['id'] == row_id, 'adm3'] = adm3_str
    
    f_name = os.path.basename(f_in)
    f_out = f_name.replace('.xlsx', '_result_2.xlsx')
    f_out = f'{DIR_NER_GZTR_OUTPUT}/{f_out}'
    df_out.to_excel(f_out, index=False)
