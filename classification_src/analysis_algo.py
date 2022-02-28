import pandas as pd 
import sys
from os.path import basename
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier 
from sklearn.linear_model import LogisticRegression

from mlxtend.evaluate import mcnemar
from mlxtend.evaluate import mcnemar_table

from scipy.stats import f_oneway 
from mlxtend.evaluate import cochrans_q

import lib.classifier_tool as tool
from lib import misc

if __name__ == "__main__":
    f_in = sys.argv[1]

    bencana = misc.get_bencana_name(f_in)
    if None == bencana:
        sys.exit('>> Bencana name is not found ')

    df = pd.read_json(f_in)

    dct_preproc = {
        'angin_topan'   : ['tc_swrem', 'tfidf', 'unibi' ],
        'banjir'        : ['tc_swrem', 'tfidf', 'unibi' ],
        'erupsi'        : ['tc_swrem', 'bow', 'unibi' ],
        'gempa'         : ['tc_swrem', 'bow', 'unibi' ],
        'karhutla'      : ['tc_swrem', 'bow', 'unibi' ], 
        'kekeringan'    : ['tc_swrem', 'tfidf', 'unibi' ], 
        'longsor'       : ['tc_swrem_stem', 'bow', 'unibi' ],
        'tsunami'       : ['tc_swrem', 'bow', 'uni' ],
    }


    text_preproc = dct_preproc[bencana][0]
    text_feature = dct_preproc[bencana][1]
    text_gram = dct_preproc[bencana][2]
 


    # default feature
    feat = tool.construct_bow_uni_and_bigrams
    feature = 'BOW'
    ngrams = 'UNIBI'

    # if there feature type param
    if 'tfidf'.lower() == text_feature.lower():
        if 'uni'.lower() == text_gram.lower():
                feat = tool.construct_tfidf_unigrams
                ngrams = 'UNI'

        elif 'bi'.lower() == text_gram.lower():
                feat = tool.construct_tfidf_bigrams
                ngrams = 'BI'

        elif 'unibi'.lower() == text_gram.lower():
                feat = tool.construct_tfidf_uni_and_bigrams
                ngrams = 'UNIBI'

        else:
                feat = tool.construct_tfidf_uni_and_bigrams
                ngrams = 'UNIBI'

        feature = 'TFIDF'

    if 'bow'.lower() == text_feature.lower():
        if 'uni'.lower() == text_gram.lower():
                feat = tool.construct_bow_unigrams
                ngrams = 'UNI'

        elif 'bi'.lower() == text_gram.lower():
                feat = tool.construct_bow_bigrams
                ngrams = 'BI'

        elif 'unibi'.lower() == text_gram.lower():
                feat = tool.construct_bow_uni_and_bigrams
                ngrams = 'UNIBI'

        else:
                feat = tool.construct_bow_uni_and_bigrams
                ngrams = 'UNIBI'

        feature = 'BOW'


    print("Selection of algo")
    print(f"Repr: {text_preproc}")
    print(f"Feature: {feature}")
    print(f"N-gram: {ngrams}")

    y = df['label'].to_numpy()
    df_result = pd.DataFrame()

    X, vectorizer = feat(df[text_preproc])
    clf = MultinomialNB()
    report, dict_result = tool.eval_cv(X, y, clf, bencana)
    sr_multi_nb = pd.Series(dict_result).sort_index()
    df_result['multi_nb_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['multi_nb_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['multi_nb_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])

    X, vectorizer = feat(df[text_preproc])
    clf = SVC()
    report, dict_result = tool.eval_cv(X, y, clf, bencana)
    sr_svc = pd.Series(dict_result).sort_index()
    df_result['svc_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['svc_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['svc_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])
    
    X, vectorizer = feat(df[text_preproc])
    clf = LinearSVC(max_iter=20000, dual=True)
    report, dict_result = tool.eval_cv(X, y, clf, bencana)
    sr_lsvc = pd.Series(dict_result).sort_index()
    df_result['lsvc_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['lsvc_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['lsvc_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])

    X, vectorizer = feat(df[text_preproc])
    clf = RandomForestClassifier(max_depth=100, random_state=0, n_estimators=100)
    report, dict_result = tool.eval_cv(X, y, clf, bencana)
    sr_rf = pd.Series(dict_result).sort_index()
    df_result['rf_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['rf_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['rf_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])
    
    X, vectorizer = feat(df[text_preproc])
    clf = LogisticRegression(max_iter=20000)
    report, dict_result = tool.eval_cv(X, y, clf, bencana)
    sr_lr = pd.Series(dict_result).sort_index()
    df_result['lr_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result['lr_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result['lr_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])

    X, vectorizer = feat(df[text_preproc])
    clf = AdaBoostClassifier()
    report, dict_result = tool.eval_cv(X, y, clf, bencana)
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

    print(df_result.round(3))

    result = f_oneway(
            df_result['multi_nb_P'].to_numpy(),
            df_result['svc_P'].to_numpy(),
            df_result['lsvc_P'].to_numpy(),
            df_result['rf_P'].to_numpy(),
            df_result['lr_P'].to_numpy(),
            df_result['ada_P'].to_numpy())
    print("ANNOVA P : %0.3f, %0.3f" % result)
    
    result = f_oneway(
            df_result['multi_nb_R'].to_numpy(),
            df_result['svc_R'].to_numpy(),
            df_result['lsvc_R'].to_numpy(),
            df_result['rf_R'].to_numpy(),
            df_result['lr_R'].to_numpy(),
            df_result['ada_R'].to_numpy())
    print("ANNOVA R : %0.3f, %0.3f" % result)

    result = f_oneway(
            df_result['multi_nb_F1'].to_numpy(),
            df_result['svc_F1'].to_numpy(),
            df_result['lsvc_F1'].to_numpy(),
            df_result['rf_F1'].to_numpy(),
            df_result['lr_F1'].to_numpy(),
            df_result['ada_F1'].to_numpy())
    print("ANNOVA F1 : %0.3f, %0.3f" % result)


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
    print("COHRAN Q-Test: q: %0.3f, p_value: %0.3f" % (q, p_value))
    
    #f_out = basename(f_in)
    #df_result.to_excel(f_in.replace('.json', '_RESULT.xlsx'))

    l_algo = [ 'multi_nb', 'svc', 
               'lsvc', 'rf', 
               'lr', 'ada' ]

    l_rslt = [ sr_multi_nb.to_numpy(), sr_svc.to_numpy(),
               sr_lsvc.to_numpy(), sr_rf.to_numpy(),
               sr_lr.to_numpy(), sr_ada.to_numpy() ]

    l_pair = list(zip(l_algo, l_rslt))

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
            chi2, p = mcnemar(ary=tb, exact=True)

            #print(tb)
            l_mcnemar_rslt.append((chi2, p))
            print(f"McNemar %s v %s:  chi2 : %0.3f,  %0.3f" 
                    % (k0, k1, chi2, p))

    for i in l_mcnemar_rslt:
        print("%0.3f %0.3f" % i, end=' ')
    print("")
