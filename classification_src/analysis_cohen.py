import pandas as pd
from sklearn.metrics import cohen_kappa_score

def anotation_analysis(bencana : str, dir_ano_1 : str, dir_ano_2 : str ) ->  list:

    df_ano_1 = pd.read_excel(f_ano_1)
    df_ano_1['label'] = df_ano_1['label'].replace(['Y', 'N'], ['O', 'X'])
    df_ano_2 = pd.read_excel(f_ano_2)

    cohen_score = cohen_kappa_score(df_ano_1['label'], df_ano_2['label'])

    n_ano1  = len(df_ano_1)
    n_yano1 = len(df_ano_1[df_ano_1['label'] == 'O'])
    n_nano1 = len(df_ano_1[df_ano_1['label'] == 'X'])
    p_yano1 = n_yano1 / n_ano1 * 100

    n_ano2  = len(df_ano_2)
    n_yano2 = len(df_ano_2[df_ano_2['label'] == 'O'])
    n_nano2 = len(df_ano_2[df_ano_2['label'] == 'X'])
    p_yano2 = n_yano2 / n_ano2 * 100

    return [bencana, cohen_score, n_ano1, n_yano1,  p_yano1, n_yano2, p_yano2]

if __name__ == '__main__' :
    l_bencana = [ 
            'angin_topan', 
            'banjir', 
            'erupsi', 
            'gempa', 
            'karhutla', 
            'kekeringan', 
            'longsor', 
            'tsunami' 
            ]
    

    df_result = pd.DataFrame(columns=[
        'Bencana', 'Cohen Score', 'N article', 'Y Ano1', 'P Y Ano1', 'Y Ano2', 'P Y Ano2'])

    for bencana in l_bencana:
        f_ano_1 = f'../anotated_data/label_anotated_1/{bencana}_text_label.xlsx'
        f_ano_2 = f'../anotated_data/label_anotated_2/{bencana}_text_label.xlsx'

        df_result.loc[len(df_result.index)] = anotation_analysis(bencana, f_ano_1, f_ano_2)

    print(df_result.round(3))
