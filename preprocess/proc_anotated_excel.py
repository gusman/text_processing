import pandas as pd

class AnotatedConverter:
    def __init__(self, f_in):
        self.f_in = f_in
        self.f_json = f_in.replace('.xlsx', '.json')
        self.df = pd.read_excel(f_in)
        
    def __get_json_df_angin_topan(self):
        return self.df.rename(columns={'Berita bencana angin  topan' : 'label'})
    
    def write_to_json(self):
        ret = None
       
        if self.f_in.lower().find('angin_topan'):
            df_tmp = self.__get_json_df_angin_topan()
        else:
            return ret
        
        df_tmp = df_tmp[['id',	'source', 'date', 'title', 'content', 'label']]
        try:
            df_tmp.to_json(self.f_json, index=False, indent=2, orient='table')
            ret = self.f_json
        except Exception as e:
            print(e)
            
        return ret
        
        