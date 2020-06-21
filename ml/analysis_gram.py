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

    print("Selection of gram")
    print("feature selection: uni, bi, uni-bi")
    print("Algorithm:  Multinomial NB")
    print("Repr: tc_stem")
    print("Feature: BOW")

    clf = MultinomialNB()
    y = df['label'].to_numpy()
    df_result = pd.DataFrame()

    X, vectorizer = tool.construct_bow_unigrams(df['tc_swrem'])
    report, dict_result = tool.eval_cv(5, X, y, clf)
    sr_bow_uni = pd.Series(dict_result).sort_index()
    
    df_result['bow_uni_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['bow_uni_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['bow_uni_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])

    X, vectorizer = tool.construct_bow_bigrams(df['tc_swrem'])
    report, dict_result = tool.eval_cv(5, X, y, clf)
    sr_bow_bi = pd.Series(dict_result).sort_index()
    
    df_result['bow_bi_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['bow_bi_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['bow_bi_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])
   
    X, vectorizer = tool.construct_bow_uni_and_bigrams(df['tc_swrem'])
    report, dict_result = tool.eval_cv(5, X, y, clf)
    sr_bow_unibi = pd.Series(dict_result).sort_index()
    
    df_result['bow_unibi_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['bow_unibi_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['bow_unibi_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])

    df_result.loc['MEAN'] = df_result.mean()
    df_result = df_result[[
        'bow_uni_P', 'bow_bi_P', 'bow_unibi_P',
        'bow_uni_R', 'bow_bi_R', 'bow_unibi_R',
        'bow_uni_F1', 'bow_bi_F1', 'bow_unibi_F1'
    ]]

    print(df_result)

    result = f_oneway(
            df_result['bow_uni_P'].to_numpy(),
            df_result['bow_bi_P'].to_numpy(),
            df_result['bow_unibi_P'].to_numpy())
    print("ANNOVA P : %0.5f, %0.5f" % result)
    
    result = f_oneway(
            df_result['bow_uni_R'].to_numpy(),
            df_result['bow_bi_R'].to_numpy(),
            df_result['bow_unibi_R'].to_numpy())
    print("ANNOVA R : %0.5f, %0.5f" % result)

    result = f_oneway(
            df_result['bow_uni_F1'].to_numpy(),
            df_result['bow_bi_F1'].to_numpy(),
            df_result['bow_unibi_F1'].to_numpy())
    print("ANNOVA F1 : %0.5f, %0.5f" % result)


    # Coher Q analysis
    y_bow_uni = sr_bow_uni.to_numpy()
    y_bow_bi  = sr_bow_bi.to_numpy()
    y_bow_unibi  = sr_bow_unibi.to_numpy()
    q, p_value = cochrans_q(y, y_bow_uni, y_bow_bi, y_bow_unibi)
    print("COHRAN Q-Test: q: %0.5f, p_value: %0.5f" % (q, p_value))


    l_grams =  [ 'bow_uni', 'bow_bi', 'bow_unibi' ]
    l_rslt =  [ y_bow_uni, y_bow_bi, y_bow_unibi ]
    l_pair = list(zip(l_grams, l_rslt))

    l_mcnemar_rslt =  []
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
            l_mcnemar_rslt.append("{chi2:.5f}".format(chi2=chi2))
            l_mcnemar_rslt.append("{p:.5f}".format(p=p))
            print(f"McNemar %s v %s:  chi2 : %0.5f, p_value: %0.5f" 
                    % (k0, k1, chi2, p))
    print(" ".join(l_mcnemar_rslt))
