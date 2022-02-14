import pandas as pd
import re

DIR_ANOTATED_FILE = '../anotated_data/location_and_time'
DIR_DT_STAGING = '../date_extraction_staging'

def get_anotated_file(bencana):
    f_path = DIR_ANOTATED_FILE + f'/{bencana}_loc_time.xlsx'
    return f_path

def get_date_information(id, df_anotated):
    df_data = df_anotated[ df_anotated['id'] == id ].copy()

    l_dttm = []
    for d in df_data['Tanggal Kejadian'].values :
        if d != None \
            and str(d).lower().strip() != 'nan'.lower()  \
            and str(d).lower().strip() != 'NULL'.lower():

            if re.search(">", d) != None:
                d = re.split('>', d)
                l_dttm.extend(d)
            else:
                l_dttm.append(d)
    
    l_dttm = [ e.strip() for e in l_dttm ]
    return "|".join(set(l_dttm))

if __name__ == "__main__":
    l_bencana = ['angin_topan', 'banjir', 'erupsi', 'gempa', 'karhutla', 'kekeringan', 'longsor', 'tsunami']

    df_angin_topan = pd.read_excel(get_anotated_file('angin_topan'))
    df_banjir = pd.read_excel(get_anotated_file('banjir'))
    df_erupsi = pd.read_excel(get_anotated_file('erupsi'))
    df_gempa = pd.read_excel(get_anotated_file('gempa'))
    df_karthula = pd.read_excel(get_anotated_file('karhutla'))
    df_kekeringan = pd.read_excel(get_anotated_file('kekeringan'))
    df_longsor = pd.read_excel(get_anotated_file('longsor'))
    df_tsunami = pd.read_excel(get_anotated_file('tsunami'))

    dict_anotated = { 
        'angin_topan' : df_angin_topan,
        'banjir' : df_banjir,
        'erupsi' : df_erupsi,
        'gempa' : df_gempa,
        'karhutla' : df_karthula,
        'kekeringan' : df_kekeringan,
        'longsor' : df_longsor,
        'tsunami' : df_tsunami,
        }

    df_final = pd.DataFrame()

    for bencana in l_bencana:
        df_anotated = dict_anotated[bencana]
        df_positive = df_anotated[['id', 'Positif Bencana Alam']]
        df_positive = df_positive[df_positive['Positif Bencana Alam'] == 'O']
        df_positive = df_positive.drop_duplicates()
        df_positive = df_positive.reset_index(drop=True)

        df_final = pd.concat([df_final, df_positive], ignore_index=True)

    for i, data in df_final.iterrows():
        id = data['id']
        bencana = re.sub('_[\d]*$', '', id)
       
        df_anotated = dict_anotated[bencana]
        dttm = get_date_information(id, df_anotated)
        df_final.loc[i, 'date'] = dttm

    
    print(df_final)

    f_out = DIR_DT_STAGING + '/date_actual.xlsx'
    df_final.to_excel(f_out, index=False)
