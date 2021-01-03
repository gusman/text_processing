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

    # default feature
    feat_uni = tool.construct_bow_unigrams
    feat_bi = tool.construct_bow_bigrams
    feat_unibi = tool.construct_bow_uni_and_bigrams
    feature = 'BOW'

    # if there feature type param
    if 2 < len(sys.argv) and 'tfidf'.lower() == sys.argv[2].lower():
        feat_uni = tool.construct_tfidf_unigrams
        feat_bi = tool.construct_tfidf_bigrams
        feat_unibi = tool.construct_tfidf_uni_and_bigrams
        feature = 'TFIDF'


    print("Selection of gram")
    print("feature selection: uni, bi, uni-bi")
    print("Algorithm:  Multinomial NB")
    print("Repr: tc_swrem")
    print(f"Feature: {feature}")

    clf = MultinomialNB()
    y = df['label'].to_numpy()
    df_result = pd.DataFrame()

    X, vectorizer = feat_uni(df['tc_swrem'])
    report, dict_result = tool.eval_cv(5, X, y, clf)
    sr_uni = pd.Series(dict_result).sort_index()
    
    df_result['uni_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['uni_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['uni_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])

    X, vectorizer = feat_bi(df['tc_swrem'])
    report, dict_result = tool.eval_cv(5, X, y, clf)
    sr_bi = pd.Series(dict_result).sort_index()
    
    df_result['bi_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['bi_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['bi_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])
   
    X, vectorizer = feat_unibi(df['tc_swrem'])
    report, dict_result = tool.eval_cv(5, X, y, clf)
    sr_unibi = pd.Series(dict_result).sort_index()
    
    df_result['unibi_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['unibi_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['unibi_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])

    df_result.loc['MEAN'] = df_result.mean()
    df_result = df_result[[
        'uni_P', 'bi_P', 'unibi_P',
        'uni_R', 'bi_R', 'unibi_R',
        'uni_F1', 'bi_F1', 'unibi_F1'
    ]]

    print(df_result)

    result = f_oneway(
            df_result['uni_P'].to_numpy(),
            df_result['bi_P'].to_numpy(),
            df_result['unibi_P'].to_numpy())
    print("ANNOVA P : %0.5f, %0.5f" % result)
    
    result = f_oneway(
            df_result['uni_R'].to_numpy(),
            df_result['bi_R'].to_numpy(),
            df_result['unibi_R'].to_numpy())
    print("ANNOVA R : %0.5f, %0.5f" % result)

    result = f_oneway(
            df_result['uni_F1'].to_numpy(),
            df_result['bi_F1'].to_numpy(),
            df_result['unibi_F1'].to_numpy())
    print("ANNOVA F1 : %0.5f, %0.5f" % result)


    # Coher Q analysis
    y_uni = sr_uni.to_numpy()
    y_bi  = sr_bi.to_numpy()
    y_unibi  = sr_unibi.to_numpy()
    q, p_value = cochrans_q(y, y_uni, y_bi, y_unibi)
    print("COHRAN Q-Test: q: %0.5f, p_value: %0.5f" % (q, p_value))


    l_grams =  [ 'uni', 'bi', 'unibi' ]
    l_rslt =  [ y_uni, y_bi, y_unibi ]
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
