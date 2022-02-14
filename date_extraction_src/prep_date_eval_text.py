import pandas as pd
import re

from os.path import exists

DIR_LABELED_TEXT = '../classification_staging/labeled_text'
DIR_ANOTATED_FILE = '../anotated_data/location_and_time'
DIR_DT_STAGING = '../date_extraction_staging'

def get_anotated_file(bencana):
    f_path = DIR_ANOTATED_FILE + f'/{bencana}_loc_time.xlsx'
    return f_path

def get_text_file(bencana):
    f_text = DIR_LABELED_TEXT + f'/{bencana}_text_label.xlsx'
    return f_text

if __name__ == "__main__":
    l_bencana = ['angin_topan', 'banjir', 'erupsi', 'gempa', 'karhutla', 'kekeringan', 'longsor', 'tsunami']

#    print("File exists checking")
#    for b in l_bencana:
#        print(b, f'Labeled text: {exists(get_text_file(b))}')
#        print(b, f'Anotated file: {exists(get_anotated_file(b))}')

#
    #Construct anotated
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

    # Construxt Text DF
    df_angin_topan_text = pd.read_excel(get_text_file('angin_topan'))
    df_banjir_text = pd.read_excel(get_text_file('banjir'))
    df_erupsi_text = pd.read_excel(get_text_file('erupsi'))
    df_gempa_text = pd.read_excel(get_text_file('gempa'))
    df_karhutla_text = pd.read_excel(get_text_file('karhutla'))
    df_kekeringan_text = pd.read_excel(get_text_file('kekeringan'))
    df_longsor_text = pd.read_excel(get_text_file('longsor'))
    df_tsunami_text = pd.read_excel(get_text_file('tsunami'))

    dict_text = {
        'angin_topan' : df_angin_topan_text,
        'banjir' : df_banjir_text,
        'erupsi' : df_erupsi_text,
        'gempa' : df_gempa_text,
        'karhutla' : df_karhutla_text,
        'kekeringan' : df_kekeringan_text,
        'longsor' : df_longsor_text,
        'tsunami' : df_tsunami_text,
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
       
        df_tmp = dict_text[bencana]
        sr_tmp = df_tmp[df_tmp['id'] == id]

        df_final.loc[i, 'date'] = sr_tmp['date'].values[0]
        df_final.loc[i, 'title'] = sr_tmp['title'].values[0]
        df_final.loc[i, 'content'] = sr_tmp['text'].values[0]

    print(df_final)

    f_out = DIR_DT_STAGING + '/date_analysis_text.xlsx'
    df_final.to_excel(f_out, index=False)
