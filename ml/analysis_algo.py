import pandas as pd 
import sys
from os.path import basename
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier 
from sklearn.linear_model import LogisticRegression

from scipy.stats import f_oneway 
from mlxtend.evaluate import cochrans_q

import classifier_tool as tool

if __name__ == "__main__":
    f_in = sys.argv[1]
    df = pd.read_json(f_in)

    print("Selection of algo")
    print("Repr: tc_lower")
    print("Feature: bow-uni")

    y = df['label'].to_numpy()
    df_result = pd.DataFrame()

    X, vectorizer = tool.construct_bow_unigrams(df['tc_lower'])
    clf = MultinomialNB()
    report, dict_result = tool.eval_cv(5, X, y, clf)
    sr_multi_nb = pd.Series(dict_result).sort_index()
    df_result['multi_nb_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['multi_nb_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['multi_nb_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])

    X, vectorizer = tool.construct_bow_unigrams(df['tc_lower'])
    clf = SVC()
    report, dict_result = tool.eval_cv(5, X, y, clf)
    sr_svc = pd.Series(dict_result).sort_index()
    df_result['svc_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['svc_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['svc_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])
    
    X, vectorizer = tool.construct_bow_unigrams(df['tc_lower'])
    clf = LinearSVC(max_iter=10000)
    report, dict_result = tool.eval_cv(5, X, y, clf)
    sr_lsvc = pd.Series(dict_result).sort_index()
    df_result['lsvc_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['lsvc_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['lsvc_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])

    X, vectorizer = tool.construct_bow_unigrams(df['tc_lower'])
    clf = RandomForestClassifier(max_depth=100, random_state=0, n_estimators=100)
    report, dict_result = tool.eval_cv(5, X, y, clf)
    sr_rf = pd.Series(dict_result).sort_index()
    df_result['rf_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['rf_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['rf_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])
    
    X, vectorizer = tool.construct_bow_unigrams(df['tc_lower'])
    clf = LogisticRegression(max_iter=200)
    report, dict_result = tool.eval_cv(5, X, y, clf)
    sr_lr = pd.Series(dict_result).sort_index()
    df_result['lr_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['lr_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['lr_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])

    X, vectorizer = tool.construct_bow_unigrams(df['tc_lower'])
    clf = AdaBoostClassifier()
    report, dict_result = tool.eval_cv(5, X, y, clf)
    sr_ada = pd.Series(dict_result).sort_index()
    df_result['ada_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['ada_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['ada_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])

    df_result.loc['MEAN'] = df_result.mean()
    df_result = df_result[[
        'multi_nb_P', 'svc_P', 'lsvc_P', 'rf_P', 'lr_P', 'ada_P',
        'multi_nb_R', 'svc_R', 'lsvc_R', 'rf_R', 'lr_R', 'ada_R', 
        'multi_nb_F1', 'svc_F1', 'lsvc_F1', 'rf_F1', 'lr_F1', 'ada_F1',
    ]]

    print(df_result)

    result = f_oneway(
            df_result['multi_nb_P'].to_numpy(),
            df_result['svc_P'].to_numpy(),
            df_result['lsvc_P'].to_numpy(),
            df_result['rf_P'].to_numpy(),
            df_result['lr_P'].to_numpy(),
            df_result['ada_P'].to_numpy())
    print("ANNOVA P : %0.5f, %0.5f" % result)
    
    result = f_oneway(
            df_result['multi_nb_R'].to_numpy(),
            df_result['svc_R'].to_numpy(),
            df_result['lsvc_R'].to_numpy(),
            df_result['rf_R'].to_numpy(),
            df_result['lr_R'].to_numpy(),
            df_result['ada_R'].to_numpy())
    print("ANNOVA R : %0.5f, %0.5f" % result)

    result = f_oneway(
            df_result['multi_nb_F1'].to_numpy(),
            df_result['svc_F1'].to_numpy(),
            df_result['lsvc_F1'].to_numpy(),
            df_result['rf_F1'].to_numpy(),
            df_result['lr_F1'].to_numpy(),
            df_result['ada_F1'].to_numpy())
    print("ANNOVA F1 : %0.5f, %0.5f" % result)


    # Coher Q analysis
    q, p_value = cochrans_q(
            y, 
            sr_multi_nb.to_numpy(),
            sr_svc.to_numpy(),
            sr_lsvc.to_numpy(),
            sr_rf.to_numpy(),
            sr_lr.to_numpy(),
            sr_ada.to_numpy(),
            )
    print("COHRAN Q-Test: q: %0.5f, p_value: %0.5f" % (q, p_value))
    
    f_out = basename(f_in)
    df_result.to_excel(f_in.replace('.json', '_RESULT.xlsx'))
