import pandas as pd
import sys

from gazetteer_loc import GazetteerAdmLoc as GZTR

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
    gztr = GZTR()
    
    dict_adm1 = {}
    dict_adm2 = {}
    dict_adm3 = {}

    for index, row in df_data.iterrows():
        row_id = row['id']
        sr_locs = pd.Series([ l.strip() for l in row['raw_ner'].split(',')])
        dict_adm1, dict_adm2, dict_adm3 = search_in_gazetteer(sr_locs)

        adm1_str, adm2_str, adm3_str =\
            ', '.join(list(dict_adm1.values())),\
            ', '.join(list(dict_adm2.values())),\
            ', '.join(list(dict_adm3.values()))

        df_out.loc[df_out['id'] == row_id, 'adm1'] = adm1_str
        df_out.loc[df_out['id'] == row_id, 'adm2'] = adm2_str
        df_out.loc[df_out['id'] == row_id, 'adm3'] = adm3_str
    
    f_out = f_in.replace('.xlsx', '_result_1.xlsx')
    df_out.to_excel(f_out, index=False)
