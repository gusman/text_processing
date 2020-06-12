import pandas as pd
import sys

from gazetteer_loc import GazetteerAdmLoc as GZTR


if __name__ == "__main__":
    l_loc = [ 'Barat', 'Sumatera', 'Selatan', 'Aceh']
    sr_locs = pd.Series(l_loc)


    gztr = GZTR()

    #from function search gazetter 
    dict_adm1 = {}
    dict_adm2 = {}
    dict_adm3 = {}

    for index, item in sr_locs.iteritems():
        loc_id, loc_str = gztr.search_gazetteer_by_name(4, index, sr_locs, 1)
        if None != loc_id and loc_id not in dict_adm1:
            dict_adm1[loc_id] = loc_str
            gztr.adm1_keys_filter = list(dict_adm1.keys())

    print(dict_adm1)
        

