import pandas as pd
import sys

from gazetteer_loc import GazetteerAdmLoc as GZTR

class ADMLoc:
    dict_adm3 = {}
    dict_adm2 = {}
    dict_adm1 = {}

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

def consolidate_adm3(adm_loc):
    adm3_str = ''
    tmp_dict_adm3 = {}
    dict_adm2 = adm_loc.dict_adm2
    dict_adm3 = adm_loc.dict_adm3
        
    adm3_keys = [ ".".join(k.split('.')[:-1]) for k in list(dict_adm3.keys()) ]
    adm3_prefix_keys = [ k for k in adm3_keys if k in dict_adm2 ]
    for key in adm3_prefix_keys:
        key = key + "."
        tmp_dict = { k : v for k, v in dict_adm3.items() if k.startswith(key) }
        tmp_dict_adm3.update(tmp_dict)
    
    adm_loc.dict_adm3 = tmp_dict_adm3
    return adm_loc
    
def consolidate_adm2(adm_loc):
    dict_adm2 = adm_loc.dict_adm2
    dict_adm3 = adm_loc.dict_adm3
    
    # if empty the check adm3
    if 0 >= len(list(dict_adm2.keys())):
        adm3_keys = [ ".".join(k.split('.')[:-1]) for k in list(dict_adm3.keys()) ]
        new_adm2_keys = [ k for k in adm3_keys if k not in dict_adm2.keys() ]
        sr_id = pd.Series(new_adm2_keys)
        
        for index, item in sr_id.iteritems():
            loc_id, loc_str = gztr.search_gazetteer_by_id(1, index, sr_id, 2)
            if None != loc_id and None != loc_str:
                dict_adm2[loc_id] = loc_str
    
    adm_loc.dict_adm2 = dict_adm2
    return adm_loc

def consolidate_adm1(adm_loc):
    dict_adm1 = adm_loc.dict_adm1
    dict_adm2 = adm_loc.dict_adm2
    
    # Refer to adm2 list
    adm2_keys = [ ".".join(k.split('.')[:-1]) for k in list(dict_adm2.keys()) ]
    new_adm1_keys = [ k for k in adm2_keys if k not in dict_adm1 ]
    sr_id = pd.Series(new_adm1_keys)
    
    for index, item in sr_id.iteritems():
        loc_id, loc_str = gztr.search_gazetteer_by_id(1, index, sr_id, 1)
        if None != loc_id and None != loc_str:
            dict_adm1[loc_id] = loc_str
    
    
    adm_loc.dict_adm1 = dict_adm1
    return adm_loc

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
    
    for index, row in df_data.iterrows():
        adm_loc = ADMLoc()
        row_id = row['id']
        sr_locs = pd.Series([ l.strip() for l in row['raw_ner'].split(',')])
        adm_loc.dict_adm1, adm_loc.dict_adm2, adm_loc.dict_adm3 =\
            search_in_gazetteer(sr_locs)

        adm_loc = consolidate_adm2(adm_loc)
        adm_loc = consolidate_adm3(adm_loc)
        adm_loc = consolidate_adm1(adm_loc)

        l_adm1 = list(adm_loc.dict_adm1.values())
        l_adm2 = list(adm_loc.dict_adm2.values())
        l_adm3 = list(adm_loc.dict_adm3.values())

        # Remove adm1 and adm2 duplicate
        l_adm3 = list(set(l_adm3) - set(l_adm2))

        adm1_str = ', '.join(l_adm1)
        adm2_str = ', '.join(l_adm2)
        adm3_str = ', '.join(l_adm3)

        df_out.loc[df_out['id'] == row_id, 'adm1'] = adm1_str         
        df_out.loc[df_out['id'] == row_id, 'adm2'] = adm2_str
        df_out.loc[df_out['id'] == row_id, 'adm3'] = adm3_str
    
    f_out = f_in.replace('.xlsx', '_result_3.xlsx')
    df_out.to_excel(f_out, index=False)
