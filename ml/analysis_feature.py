import pandas as pd 
import sys
from sklearn.naive_bayes import MultinomialNB
from scipy.stats import ttest_rel 
from mlxtend.evaluate import mcnemar
from mlxtend.evaluate import mcnemar_table

import classifier_tool as tool

if __name__ == "__main__":
    f_in = sys.argv[1]
    df = pd.read_json(f_in)

    print("Selection of feature")
    print("feature selection: BOW vs TFIDF")
    print("Algorithm:  Multinomial NB")
    print("Repr: tc_lower")

    clf = MultinomialNB()
    y = df['label'].to_numpy()
    df_result = pd.DataFrame()

    X, vectorizer = tool.construct_bow_unigrams(df['tc_lower'])
    report, dict_result = tool.eval_cv(5, X, y, clf)
    sr_bow_uni = pd.Series(dict_result).sort_index()
    
    df_result['bow_uni_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['bow_uni_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['bow_uni_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])

    X, vectorizer = tool.construct_tfidf_unigrams(df['tc_lower'])
    report, dict_result = tool.eval_cv(5, X, y, clf)
    sr_tfidf_uni = pd.Series(dict_result).sort_index()
    
    df_result['tfidf_uni_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['tfidf_uni_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['tfidf_uni_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])
    
    df_result.loc['MEAN'] = df_result.mean()
    df_result = df_result[[
        'bow_uni_P', 'tfidf_uni_P',
        'bow_uni_R', 'tfidf_uni_R',
        'bow_uni_F1', 'tfidf_uni_F1',
    ]]

    print(df_result)

    result = ttest_rel(
            df_result['bow_uni_P'].to_numpy(), 
            df_result['tfidf_uni_P'].to_numpy())
    print("Paired Test P: %0.5f, %0.5f" % result)
    
    result = ttest_rel(
            df_result['bow_uni_R'].to_numpy(), 
            df_result['tfidf_uni_R'].to_numpy())
    print("Paired Test R: %0.5f, %0.5f" % result)


    result = ttest_rel(
            df_result['bow_uni_F1'].to_numpy(), 
            df_result['tfidf_uni_F1'].to_numpy())
    print("Paired Test F1: %0.5f, %0.5f" % result)

    # McNemar Test
    y_bow_uni = sr_bow_uni.to_numpy()
    y_tfidf_uni = sr_tfidf_uni.to_numpy()
    tb = mcnemar_table(
            y_target = y, 
            y_model1 = y_bow_uni, 
            y_model2 = y_tfidf_uni)
    chi2, p = mcnemar(ary=tb, corrected=True)
    print("Mcnemar: chi2: %0.5f, p_value: %0.5f" % (chi2, p))

#    df_out = pd.DataFrame()
#    df_out['Y_TRUE'] = df['label'] 
#    df_out['Y_BOW_UNI'] = sr_bow_uni
#    df_out['Y_TFIDF_UNI'] = sr_tfidf_uni
#    df_out.to_excel("RESULT.xlsx")


