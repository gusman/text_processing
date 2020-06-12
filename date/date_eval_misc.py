import pandas as pd
from scipy import stats

if __name__ == '__main__':
    f_eval1 = '../tmp_dir/time/date_gold_standard_v03_rslt_all_words.xlsx'
    f_eval2 = '../tmp_dir/time/date_gold_standard_v03_rslt_spec_st.xlsx'


    df_eval1 = pd.read_excel(f_eval1)
    df_eval2 = pd.read_excel(f_eval2)

    print("--- T-TEST Metode Pemilihan Kalimat ---")
    data1 = df_eval1['jc_sim'][:400].to_numpy()
    data2 = df_eval2['jc_sim'][:400].to_numpy()
    stat, p = stats.ttest_rel(data1, data2)
    print('P-Value JC_AVG: %0.5f %0.5f' % (stat, p))

    data1 = df_eval1['pre'][:400].to_numpy()
    data2 = df_eval2['pre'][:400].to_numpy()
    stat, p = stats.ttest_rel(data1, data2)
    print('P-Value P_AVG: %0.5f %0.5f' % (stat, p))

    data1 = df_eval1['rec'][:400].to_numpy()
    data2 = df_eval2['rec'][:400].to_numpy()
    stat, p = stats.ttest_rel(data1, data2)
    print('P-Value R_AVG: %0.5f %0.5f' % (stat, p))

    data1 = df_eval1['f1'][:400].to_numpy()
    data2 = df_eval2['f1'][:400].to_numpy()
    stat, p = stats.ttest_rel(data1, data2)
    print('P-Value F1_AVG: %0.5f %0.5f' % (stat, p))


