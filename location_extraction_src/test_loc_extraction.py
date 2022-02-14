import pandas as pd
import sys

from lib.ner_measurement import NerMeasurement as NM


DIR_LOC_STAGING = '../location_extraction_staging'


def measure(str_true, str_pred):
    l_true = [ e.strip() for e in str_true.split(',') ]
    l_pred = [ e.strip() for e in str_pred.split(',') ]
    nm = NM(l_true, l_pred)
    jc_sm = nm.jaccard_simmilarity()
    p = nm.precision()
    r = nm.recall()
    f1 = nm.f1_score()
    
    return jc_sm, p, r, f1

if __name__ == '__main__':
    f_pred = sys.argv[1]
    f_ref = f'{DIR_LOC_STAGING}/loc_actual.xlsx'

    df_ref = pd.read_excel(f_ref)
    df_pred = pd.read_excel(f_pred)

    df_out = df_ref[['id','adm1', 'adm2', 'adm3']].copy()
    df_out[['pred_adm1', 'pred_adm2', 'pred_adm3']] = df_pred[['adm1', 'adm2', 'adm3']].copy()
    df_out.fillna('', inplace=True)

    df_out['jc_adm1'] = ''
    df_out['p_adm1'] = ''
    df_out['r_adm1'] = ''
    df_out['f1_adm1'] = ''

    for index, row in df_out.iterrows():
        jc_adm1, p_adm1, r_adm1, f1_adm1 = measure(row['adm1'], row['pred_adm1'])
        df_out.loc[index, 'jc_adm1'] = jc_adm1
        df_out.loc[index, 'p_adm1'] = p_adm1
        df_out.loc[index, 'r_adm1'] = r_adm1
        df_out.loc[index, 'f1_adm1'] = f1_adm1
        
        jc_adm2, p_adm2, r_adm2, f1_adm2 = measure(row['adm2'], row['pred_adm2'])
        df_out.loc[index, 'jc_adm2'] = jc_adm2
        df_out.loc[index, 'p_adm2'] = p_adm2
        df_out.loc[index, 'r_adm2'] = r_adm2
        df_out.loc[index, 'f1_adm2'] = f1_adm2
        
        jc_adm3, p_adm3, r_adm3, f1_adm3 = measure(row['adm3'], row['pred_adm3'])
        df_out.loc[index, 'jc_adm3'] = jc_adm3
        df_out.loc[index, 'p_adm3'] = p_adm3
        df_out.loc[index, 'r_adm3'] = r_adm3
        df_out.loc[index, 'f1_adm3'] = f1_adm3

        df_out.loc[index, 'jc_avg'] = (jc_adm3 + jc_adm2 + jc_adm1) / 3
        df_out.loc[index, 'p_avg']  = (p_adm3 + p_adm2 + p_adm1) / 3
        df_out.loc[index, 'r_avg']  = (r_adm3 + r_adm1 + r_adm1) / 3
        df_out.loc[index, 'f1_avg'] = (f1_adm3 + f1_adm2 + f1_adm1) / 3

    columns = [
        'jc_adm1', 'p_adm1', 'r_adm1', 'f1_adm1', 
        'jc_adm2','p_adm2', 'r_adm2', 'f1_adm2',
        'jc_adm3', 'p_adm3', 'r_adm3', 'f1_adm3', 
        'jc_avg', 'p_avg', 'r_avg', 'f1_avg', 
        ] 

    means_list = [ "{:.3f}".format(df_out[c].mean()) for c in columns ]

    lst = ['MEAN', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']
    lst = lst + means_list
    df_tmp = df_out.copy()
    df_tmp.loc[len(df_tmp)] = lst

    columns_out = [ 'id',
        'jc_adm1', 'p_adm1', 'r_adm1', 'f1_adm1', 
        'jc_adm2','p_adm2', 'r_adm2', 'f1_adm2',
        'jc_adm3', 'p_adm3', 'r_adm3', 'f1_adm3', 
        'jc_avg', 'p_avg', 'r_avg', 'f1_avg', 
        ] 

    print(df_tmp[columns_out])
