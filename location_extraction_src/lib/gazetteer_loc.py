import pandas as pd 

class GazetteerAdmLoc:
    def __init__(self, adm1_gztr, adm2_gztr, adm3_gztr):
        df_adm1 = pd.read_csv(adm1_gztr)
        df_adm2 = pd.read_csv(adm2_gztr)
        df_adm3 = pd.read_csv(adm3_gztr)

        self.df_adm1 = df_adm1.apply(lambda x: x.astype(str).str.lower())
        self.df_adm2 = df_adm2.apply(lambda x: x.astype(str).str.lower())
        self.df_adm3 = df_adm3.apply(lambda x: x.astype(str).str.lower())
        
        self.adm1_keys_filter = []
        self.adm2_keys_filter = []

    def __proc_match(self, df_match, keys_filter):
        df_tmp = pd.DataFrame(columns = df_match.columns)
        df_match = df_match.drop_duplicates()
        if None != keys_filter and 0 < len(keys_filter):
            for index, row in df_match.iterrows():
                id = row.loc['ID']
                lst_ok = [ k for k in keys_filter if id.startswith(k) ]
                if 0 < len(lst_ok):
                    df_tmp.loc[len(df_tmp.index)] = row
        else:
            df_tmp = df_match.copy()
        return df_tmp
        
    def __search_df_adm(self, words, adm_level, col):
        loc_id = None
        loc_str = None
        len_str = -1
        len_df = -1
        keys_filter = None
        
        if 1 == adm_level:
            df_adm = self.df_adm1
            keys_filter = None
        elif 2 == adm_level:
            df_adm = self.df_adm2
            keys_filter = self.adm1_keys_filter
        elif 3 == adm_level:
            df_adm = self.df_adm3
            keys_filter = self.adm2_keys_filter
        
        df_tmp = df_adm[df_adm[col].str.startswith(words)]

        if 0 < len(df_tmp.index):
            df_tmp = df_adm[df_adm[col] == words]
            len_df = len(df_tmp.index)

        # Need to evaluate below logic
        if 0 < len_df:
            df_tmp = self.__proc_match(df_tmp, keys_filter)
            len_str = len(df_tmp.index)
            
        if 0 < len_str:
            loc_str = df_tmp.iloc[0, 1]
            loc_id = df_tmp.iloc[0, 0]

        return len_str, loc_id, loc_str

    def search_gazetteer_by_name(self, n_grams, index, sr_locs, adm_level=1):  
        prev_ret_len = 0
        curr_ret_len = 0
        loc_id = None
        loc_str = None
        words = ''
        
        for offset in range(0, n_grams):
            if index + offset < len(sr_locs.index):
                words += ' ' + sr_locs[index + offset].lower()
                words = words.strip()
                curr_ret_len, tmp_loc_id, tmp_loc_str =\
                    self.__search_df_adm(words, adm_level, 'Name')
                
            if curr_ret_len > prev_ret_len:
                loc_id, loc_str = tmp_loc_id, tmp_loc_str
                
        return loc_id, loc_str
    
    def search_gazetteer_by_id(self, n_grams, index, sr_locs, adm_level=1):  
        ret_len = 0
        loc_id = None
        loc_str = None
        words = ''
         
        for offset in range(0, n_grams):
            if 0 >= ret_len and index + offset < len(sr_locs.index):
                words += ' ' + sr_locs[index + offset].lower()
                words = words.strip()
                ret_len, loc_id, loc_str = self.__search_df_adm(words, adm_level, 'ID')       
    
        return loc_id, loc_str
