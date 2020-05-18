import pandas as pd 

class GazetteerAdmLoc:
    adm1_gztr = '/home/admin/text_processing/ner/gazetteer/prov_gazetteer.csv'
    adm2_gztr = '/home/admin/text_processing/ner/gazetteer/kota_kab_gazetteer.csv'
    adm3_gztr = '/home/admin/text_processing/ner/gazetteer/kecamatan_gazetteer.csv'
    
    def __init__(self):
        df_adm1 = pd.read_csv(self.adm1_gztr)
        df_adm2 = pd.read_csv(self.adm2_gztr)
        df_adm3 = pd.read_csv(self.adm3_gztr)

        self.df_adm1 = df_adm1.apply(lambda x: x.astype(str).str.lower())
        self.df_adm2 = df_adm2.apply(lambda x: x.astype(str).str.lower())
        self.df_adm3 = df_adm3.apply(lambda x: x.astype(str).str.lower())
        
    def __search_df_adm(self, words, adm_level, col):
        loc_id = None
        loc_str = None
        len_str = -1
        
        if 1 == adm_level:
            df_adm = self.df_adm1
        elif 2 == adm_level:
            df_adm = self.df_adm2
        elif 3 == adm_level:
            df_adm = self.df_adm3
        
        df_tmp = df_adm[df_adm[col].str.startswith(words)]

        if 0 < len(df_tmp.index):
            df_tmp = df_adm[df_adm[col] == words]
            df_tmp = df_tmp.drop_duplicates()
            len_str = len(df_tmp.index)

            # Need to evaluate below logic
            if 0 < len_str:
                loc_str = df_tmp.iloc[0, 1]
                #loc_str = words
                loc_id = df_tmp.iloc[0, 0]
                #print(loc_str)
        
        return len_str, loc_id, loc_str

    def search_gazetteer_by_name(self, n_grams, index, sr_locs, adm_level=1):  
        ret_len = 0
        loc_id = None
        loc_str = None
        words = ''
        
        for offset in range(0, n_grams):
            if 0 == ret_len and index + offset < len(sr_locs.index):
                words += ' ' + sr_locs[index + offset].lower()
                words = words.strip()
                ret_len, loc_id, loc_str = self.__search_df_adm(words, adm_level, 'Name')
    
        return loc_id, loc_str
    
    def search_gazetteer_by_id(self, n_grams, index, sr_locs, adm_level=1):  
        ret_len = 0
        loc_id = None
        loc_str = None
        words = ''
         
        for offset in range(0, n_grams):
            if 0 == ret_len and index + offset < len(sr_locs.index):
                words += ' ' + sr_locs[index + offset].lower()
                words = words.strip()
                ret_len, loc_id, loc_str = self.__search_df_adm(words, adm_level, 'ID')       
    
        return loc_id, loc_str
