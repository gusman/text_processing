import pandas as pd 
import sys
from sklearn.naive_bayes import MultinomialNB
from scipy.stats import f_oneway
from mlxtend.evaluate import cochrans_q

from mlxtend.evaluate import mcnemar
from mlxtend.evaluate import mcnemar_table

import classifier_tool as tool


if __name__ == "__main__":
    f_in = sys.argv[1]
    df = pd.read_json(f_in)

    print("Selection of representation - text")
    print("Text selection: title only vs content only vs title and content")
    print("Algorithm:  Multinomial NB")
    print("Feature:   BOW - Unigram")

    clf = MultinomialNB()
    y = df['label'].to_numpy()
    df_result = pd.DataFrame()


    X, vectorizer = tool.construct_bow_unigrams(df['tc_lower'])
    report, dict_result = tool.eval_cv(5, X, y, clf)
    sr_tc_lower = pd.Series(dict_result).sort_index()
    df_result['tc_lower_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['tc_lower_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['tc_lower_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])


    X, vectorizer = tool.construct_bow_unigrams(df['t_lower'])
    report, dict_result = tool.eval_cv(5, X, y, clf)
    sr_t_lower = pd.Series(dict_result).sort_index()
    df_result['t_lower_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['t_lower_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['t_lower_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])


    X, vectorizer = tool.construct_bow_unigrams(df['c_lower'])
    report, dict_result = tool.eval_cv(5, X, y, clf)
    sr_c_lower = pd.Series(dict_result).sort_index()
    df_result['c_lower_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['c_lower_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['c_lower_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])


    df_result.loc['MEAN'] = df_result.mean()
    df_result = df_result[[
        't_lower_P', 'c_lower_P', 'tc_lower_P',
        't_lower_R', 'c_lower_R', 'tc_lower_R',
        't_lower_F1', 'c_lower_F1', 'tc_lower_F1',
    ]]

    print(df_result)

    result = f_oneway(
            df_result['t_lower_P'].to_numpy(),
            df_result['c_lower_P'].to_numpy(),
            df_result['tc_lower_P'].to_numpy())
    print("ANNOVA P : %0.5f, %0.5f" % result)
    
    result = f_oneway(
            df_result['t_lower_R'].to_numpy(),
            df_result['c_lower_R'].to_numpy(),
            df_result['tc_lower_R'].to_numpy())
    print("ANNOVA R : %0.5f, %0.5f" % result)

    result = f_oneway(
            df_result['t_lower_F1'].to_numpy(),
            df_result['c_lower_F1'].to_numpy(),
            df_result['tc_lower_F1'].to_numpy())
    print("ANNOVA F1 : %0.5f, %0.5f" % result)


   # COHRAN Q-Test
    y_tc_lower = sr_tc_lower.to_numpy()
    y_t_lower  = sr_t_lower.to_numpy()
    y_c_lower  = sr_c_lower.to_numpy()
    q, p_value = cochrans_q(y, y_tc_lower, y_t_lower, y_c_lower)
    print("COHRAN Q-Test: q: %0.5f, p_value: %0.5f" % (q, p_value))

    l_repr =  [ 't_lower', 'c_lower', 'tc_lower' ]
    l_rslt =  [ y_t_lower, y_c_lower, y_tc_lower ]
    l_pair = list(zip(l_repr, l_rslt))

    for i, t0 in enumerate(l_pair):
        for j, t1 in enumerate(l_pair[i+1:]):
            k0 = t0[0]
            k1 = t1[0]
            v0 = t0[1]
            v1 = t1[1]
            
            tb = mcnemar_table(
                y_target = y, 
                y_model1 = v0, 
                y_model2 = v1)
            chi2, p = mcnemar(ary=tb, corrected=True)
            print(f"McNemar %s - %s:  chi2 : %0.5f, p_value: %0.5f" 
                    % (k0, k1, chi2, p))
    
