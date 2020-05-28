import pandas as pd
import linecache
import json
import re
import random
import preprocess as pre
import sys


class SamplingDistr(): 
    lst_disaster = [
        'angin_topan', 'banjir', 'erupsi', 'gempa' ,'karhutla' ,
        'kekeringan', 'longsor', 'tsunami'
    ]

    lst_source  =  [
        'aceh_harianrakyat', 'aceh_tribun', 'bali_nusa', 'bali_post', 
        'bali_tribun', 'bangka_tribun', 'banjarmasin_tribun', 'banten_radar', 
        'banten_tangexpress', 'batam_pos', 'batam_tribun', 'belitung_tribun', 
        'bengkulu_express', 'bengkulu_pedoman', 'bogor_tribun', 
        'gorontalo_rgol', 'jabar_kapol', 'jabar_pikiranrakyat', 
        'jabar_tribun', 'jakarta_katadata', 'jakarta_tribun', 
        'jakarta_wartakota', 'jambi_tribun', 'jateng_tribun', 'jatim_tribun', 
        'jogja_radar', 'jogja_tribun', 'kalbar_equator', 'kalsel_infobanua', 
        'kalteng_tabengan', 'kalteng_tribun', 'kaltim_news', 'kaltim_tribun', 
        'kalut_metrokaltara', 'kupang_tribun', 'lampung_tribun', 
        'madura_tribun', 'malang_tribun', 'maluku_tribun', 'malut_berita', 
        'manado_tribun', 'medan_tribun', 'nasional_kompas', 'nasional_sindo', 
        'ntb_suara', 'palembang_tribun', 'papua_jubi', 
        'papuabarat_radarsorong', 'pekanbaru_tribun', 
        'pontianak_tribun', 'solo_tribun', 'sulbar_mamuju', 
        'sulsel_ekspres', 'sulsel_kabarmakassar', 'sulteng_raya',
        'sultra_zona', 'sumbar_haluan', 'sumbar_jurnal', 'sumbar_singgalang',
        'sumsel_sumeks', 'sumsel_tribun', 'sumut_go', 'surabaya_tribun',
    ]

    home_sampling = '/home/admin/sampling-data/'
    dir_news = '/home/admin/sampling-data/output/output_20200414' 
    dir_sampling = '/home/admin/sampling-data/sampling'
    f_distr = home_sampling + '/' + 'sample_distr_2020414.csv'

    def __init__(self, boundary):
        self.boundary = boundary
        self.df_nline = self.__create_nline_df_distr()
        self.df_nsample = self.__create_nsample_df_distr()


    def __create_nline_df_distr(self):
        df_nline = pd.DataFrame(columns=self.lst_disaster, 
                                index=self.lst_source)

        for disaster in self.lst_disaster:
            for source in self.lst_source:
                filename = source + ".json" + "_" + disaster + ".txt"
                filepath = self.dir_news + "/" + filename
                n_lines = sum(1 for line in open(filepath))
                df_nline.at[source, disaster] = n_lines
        return df_nline

    def __create_nsample_df_distr(self):
        df_sample = pd.DataFrame(index=self.lst_source)        

        for disaster in self.lst_disaster:
            lst_tmp = []
            for index, row in self.df_nline.iterrows():
                val = row[disaster]
                if (val < self.boundary):
                    lst_tmp.append(val)
                else:
                    lst_tmp.append(self.boundary)

            df_series = pd.DataFrame(lst_tmp, columns=['sample_' + disaster], 
                        index=self.lst_source)
            df_sample['sample_' + disaster] = df_series

        return df_sample

    def create_distr_file(self):
        df_join = self.df_nline.join(self.df_nsample, how='inner')
        df_join.to_csv(self.f_distr)
    
    def news_verificaton(self, json_line):
        ret = True

        title = json_line['title']
        date = json_line['date']
        content = json_line['content']

        if len(title) < 3 or len (date) < 3 or len (content) < 5:
            ret = False

        return ret

    def random_number(self, max_num, invalid_num):
        random_num = 0
        while(True):
            random_num = random.sample(range(1, max_num + 1, 1), 1)[0]
            if random_num not in invalid_num:
                break
        return random_num

    def retrieve_news(self, filepath, source, n_file, n_sample, ctr=1):
        regex = re.compile(r'\,$')
        lst_json = []
        lst_linenum = random.sample(range(1, n_file + 1, 1), n_sample)
        for n in lst_linenum:
            l = linecache.getline(filepath, n).strip()
            l = re.sub(regex, '', l)     
            try:
                json_line = json.loads(l)
                json_line['source'] = source
                json_line['id'] = disaster + '_' + "%04d" % ctr
                pre.clean_up([json_line])

                if True == self.news_verificaton(json_line):
                    lst_json.append(json_line)
                    ctr += 1
                else:
                    print("FAIL at line: %d" % n )
                    rdm_num = self.random_number(n_file, lst_json)
                    print("Append %d to list of line number" % rdm_num )
                    lst_linenum.append(rdm_num)

            except Exception as e:
                print("Fail to load json line " 
                        + filepath + " at line: " + str(n))
                print("Exception: ", e)
                rdm_num = self.random_number(n_file, lst_json)
                print("Append %d to list of line number" % rdm_num )
                lst_linenum.append(rdm_num)
        return ctr, lst_json
        
    def create_sampling_attrs(self, disaster):
        lst_attr = []

        if disaster not in self.lst_disaster:
            return None

        for source in self.lst_source:
            filename = source + '.json' + '_' + disaster + '.txt'
            filepath = self.dir_news + '/' + filename
            n_file = self.df_nline.loc[source, disaster]
            n_sample = self.df_nsample.loc[source, 'sample_' + disaster]

            lst_attr.append(
                {   
                    'filepath' : filepath, 
                    'source': source, 
                    'n_file' : n_file, 
                    'n_sample' : n_sample
                }
            )
        return lst_attr

    def create_news_sample(self, disaster):
        lst_news = []
        lst_attr = self.create_sampling_attrs(disaster)
        
        ctr = 1
        for attr in lst_attr:
            ctr, lst_json = self.retrieve_news(attr['filepath'], attr['source'], 
                            attr['n_file'], attr['n_sample'], ctr)
            lst_news.extend(lst_json)

        return lst_news

    def create_news_sample_file(self, disaster):
        lst_news_attr = [
            'id', 'source', 'date', 'title', 'content',
            'Berita bencana', 'Tanggal Kejadian', 'Lokasi Provinsi', 
            'Lokasi Kota/Kabupaten', 'Lokasi Kecamatan', 'Jumlah orang meninggal', 
            'Jumlah orang hilang', 'Jumlah orang cedera/sakit', 'Jumlah orang mengungsi',
            'Jumlah bangunan rusak'
        ]
        
        lst_news = self.create_news_sample(disaster)
        df = pd.DataFrame(lst_news)
        df = df.reindex(columns=lst_news_attr)
        
        filepath = self.dir_sampling + '/sample_' + disaster + '_20200414.xlsx'
        df.to_excel(filepath, index=False)

if __name__ == "__main__":
    disaster = sys.argv[1]
    sampling_distr = SamplingDistr(20)
    sampling_distr.create_news_sample_file(disaster) 

