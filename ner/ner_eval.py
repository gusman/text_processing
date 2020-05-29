import pandas as pd
import sys
from os.path import basename
from ner_measurement import NerMeasurement as NM

def measure(str_true, str_pred):
    l_true = [ e.strip() for e in str_true.split(',') ]
    l_pred = [ e.strip() for e in str_pred.split(',') ]
    nm = NM(l_true, l_pred)
    jc_sm = nm.jaccard_simmilarity()
    p = nm.precision()
    r = nm.recall()
    f1 = nm.f1_score()
    
    return jc_sm, p, r, f1

if __name__ == "__main__":
    f_ref = '../tmp_dir/loc_gold_standard_v03.xlsx'

    f_in = sys.argv[1]
    f_out = f_in.replace('.xlsx', '_eval.xlsx')
    f_pred = f_in
    
    df_ref = pd.read_excel(f_ref)
    df_pred = pd.read_excel(f_pred)

    df_out = df_ref[['id','adm1', 'adm2', 'adm3']].copy()
    df_out[['pred_adm1', 'pred_adm2', 'pred_adm3']] = df_pred[['adm1', 'adm2', 'adm3']].copy()
    df_out.fillna('', inplace=True)

    for index, row in df_out.iterrows():
        total_jc = 0
        total_p = 0
        total_r = 0
        total_f1 = 0
        jc_adm, p_adm, r_adm, f1_adm = measure(row['adm1'], row['pred_adm1'])
        df_out.loc[index, 'jc_adm1'] = jc_adm
        df_out.loc[index, 'p_adm1'] = p_adm
        df_out.loc[index, 'r_adm1'] = r_adm
        df_out.loc[index, 'f1_adm1'] = f1_adm
        total_jc += jc_adm
        total_p += p_adm
        total_r += r_adm
        total_f1 += f1_adm

        jc_adm, p_adm, r_adm, f1_adm = measure(row['adm2'], row['pred_adm2'])
        df_out.loc[index, 'jc_adm2'] = jc_adm
        df_out.loc[index, 'p_adm2'] = p_adm
        df_out.loc[index, 'r_adm2'] = r_adm
        df_out.loc[index, 'f1_adm2'] = f1_adm
        total_jc += jc_adm
        total_p += p_adm
        total_r += r_adm
        total_f1 += f1_adm

        jc_adm, p_adm, r_adm, f1_adm = measure(row['adm3'], row['pred_adm3'])
        df_out.loc[index, 'jc_adm3'] = jc_adm
        df_out.loc[index, 'p_adm3'] = p_adm
        df_out.loc[index, 'r_adm3'] = r_adm
        df_out.loc[index, 'f1_adm3'] = f1_adm
        total_jc += jc_adm
        total_p += p_adm
        total_r += r_adm
        total_f1 += f1_adm

        df_out.loc[index, 'jc_avg'] = total_jc/3
        df_out.loc[index, 'p_avg'] = total_p/3
        df_out.loc[index, 'r_avg'] = total_r/3 
        df_out.loc[index, 'f1_avg'] = total_f1/3
    
    final_cols = [
        'id', 
        'adm1', 'adm2', 'adm3', 
        'pred_adm1', 'pred_adm2', 'pred_adm3',
        'jc_adm1', 'jc_adm2', 'jc_adm3', 'jc_avg',
        'p_adm1', 'p_adm2', 'p_adm3', 'p_avg',
        'r_adm1', 'r_adm2', 'r_adm3', 'r_avg',
        'f1_adm1', 'f1_adm2', 'f1_adm3', 'f1_avg',
    ]

    df_out = df_out[final_cols]
    dir_out = '../tmp_dir/eval'
    fname_out = basename(f_out)
    f_out = dir_out + '/' + fname_out
    df_out.to_excel(f_out, index=False)
