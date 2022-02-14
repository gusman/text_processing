import pandas as pd
import re

DIR_ANOTATED_FILE = '../anotated_data/location_and_time'
DIR_LOC_STAGING = '../location_extraction_staging'

def get_anotated_file(bencana):
    f_path = DIR_ANOTATED_FILE + f'/{bencana}_loc_time.xlsx'
    return f_path

def get_adm_information(id, df_anotated):
    df_data = df_anotated[ df_anotated['id'] == id ].copy()
    l_adm1 = [ d for d in df_data['Lokasi ADM1'].values ]
    l_adm2 = [ d for d in df_data['Lokasi ADM2'].values ]
    l_adm3 = [ d for d in df_data['Lokasi ADM3'].values ]
    
    l_adm1 = [ e.strip().lower() for e in l_adm1 if str(e).lower().strip() != 'nan'.lower() and str(e).lower().strip() != 'NULL'.lower()]
    l_adm2 = [ e.strip().lower() for e in l_adm2 if str(e).lower().strip() != 'nan'.lower() and str(e).lower().strip() != 'NULL'.lower()]
    l_adm3 = [ e.strip().lower() for e in l_adm3 if str(e).lower().strip() != 'nan'.lower() and str(e).lower().strip() != 'NULL'.lower()]

    l_adm2 = [ e.replace('kabupaten', '').strip() for e in l_adm2 ]
    l_adm2 = [ e.replace('kota', '').strip() for e in l_adm2 ]

    return ','.join(set(l_adm1)), ','.join(set(l_adm2)), ','.join(set(l_adm3))

if __name__ == '__main__':
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
        adm1, adm2, adm3 = get_adm_information(id, df_anotated)
        df_final.loc[i, 'adm1'] = adm1
        df_final.loc[i, 'adm2'] = adm2
        df_final.loc[i, 'adm3'] = adm3

    print(df_final)
    f_out = f'{DIR_LOC_STAGING}/loc_actual.xlsx'
    df_final.to_excel(f_out, index=False)
