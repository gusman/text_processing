import pandas as pd
from scipy import stats

if __name__ == '__main__':
    f_eval1 = '../tmp_dir/loc/eval/loc_gold_standard_v03_ner_w_tokens_result_1_eval.xlsx'
    f_eval2 = '../tmp_dir/loc/eval/loc_gold_standard_v03_ner_w_tokens_result_2_eval.xlsx'
    f_eval3 = '../tmp_dir/loc/eval/loc_gold_standard_v03_ner_w_tokens_result_3_eval.xlsx'
    f_st_eval3 = '../tmp_dir/loc/eval/loc_gold_standard_v03_ner_st_keywords_result_3_eval.xlsx'

    df_eval1 = pd.read_excel(f_eval1)
    df_eval2 = pd.read_excel(f_eval2)
    df_eval3 = pd.read_excel(f_eval3)
    df_st_eval3 = pd.read_excel(f_st_eval3)

    print("--- ANOVA Metode Pemilihan Metode ekstraksi ---")
    data1 = df_eval1['jc_avg'][:400].to_numpy()
    data2 = df_eval2['jc_avg'][:400].to_numpy()
    data3 = df_eval3['jc_avg'][:400].to_numpy()
    stat, p = stats.f_oneway(data1, data2, data3)
    print('P-Value JC_AVG: %0.5f' % p)

    data1 = df_eval1['p_avg'][:400].to_numpy()
    data2 = df_eval2['p_avg'][:400].to_numpy()
    data3 = df_eval3['p_avg'][:400].to_numpy()
    stat, p = stats.f_oneway(data1, data2, data3)
    print('P-Value P_AVG: %0.5f' % p)

    data1 = df_eval1['r_avg'][:400].to_numpy()
    data2 = df_eval2['r_avg'][:400].to_numpy()
    data3 = df_eval3['r_avg'][:400].to_numpy()
    print('P-Value R_AVG: %0.5f' % p)

    data1 = df_eval1['f1_avg'][:400].to_numpy()
    data2 = df_eval2['f1_avg'][:400].to_numpy()
    data3 = df_eval3['f1_avg'][:400].to_numpy()
    stat, p = stats.f_oneway(data1, data2, data3)
    print('P-Value F1_AVG: %0.5f' % p)

    print("--- T-TEST Metode Pemilihan Kalimat ---")
    data1 = df_eval3['jc_avg'][:400].to_numpy()
    data2 = df_st_eval3['jc_avg'][:400].to_numpy()
    stat, p = stats.ttest_rel(data1, data2)
    print('P-Value JC_AVG: %0.5f' % p)

    data1 = df_eval3['p_avg'][:400].to_numpy()
    data2 = df_st_eval3['p_avg'][:400].to_numpy()
    stat, p = stats.ttest_rel(data1, data2)
    print('P-Value P_AVG: %0.5f' % p)

    data1 = df_eval3['r_avg'][:400].to_numpy()
    data2 = df_st_eval3['r_avg'][:400].to_numpy()
    stat, p = stats.ttest_rel(data1, data2)
    print('P-Value R_AVG: %0.5f' % p)

    data1 = df_eval3['f1_avg'][:400].to_numpy()
    data2 = df_st_eval3['f1_avg'][:400].to_numpy()
    stat, p = stats.ttest_rel(data1, data2)
    print('P-Value F1_AVG: %0.5f' % p)


