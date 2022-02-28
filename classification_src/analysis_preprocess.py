import pandas as pd 
import sys
from sklearn.naive_bayes import MultinomialNB
from scipy.stats import f_oneway
from mlxtend.evaluate import cochrans_q
from mlxtend.evaluate import mcnemar
from mlxtend.evaluate import mcnemar_table

import lib.classifier_tool as tool
from lib import misc


if __name__ == "__main__":
    f_in = sys.argv[1]

    bencana = misc.get_bencana_name(f_in)
    
    if None == bencana:
        sys.exit('>> Bencana name is not found ')

    dct_preproc = {
        'angin_topan' : 'tc', 
        'banjir' : 'tc', 
        'erupsi' : 'tc', 
        'gempa' : 'tc', 
        'karhutla' : 'tc', 
        'kekeringan' : 'tc', 
        'longsor' : 'tc', 
        'tsunami' : 'tc', 
    }
    text_preproc = dct_preproc[bencana]


    df = pd.read_json(f_in)

    print("Selection of text preprocess")
    print("Text selection: title only vs content only vs title and content")
    print("Algorithm:  Multinomial NB")
    print("Feature:   BOW - Unigram")
    print("Representation:   BOW - tc")

    clf = MultinomialNB()
    y = df['label'].to_numpy()
    df_result = pd.DataFrame()


    X, vectorizer = tool.construct_bow_unigrams(df[text_preproc + '_lower'])
    report, dict_result = tool.eval_cv(X, y, clf, bencana)
    sr_tc_lower = pd.Series(dict_result).sort_index()
    df_result[text_preproc + '_lower_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result[text_preproc + '_lower_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result[text_preproc + '_lower_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])


    X, vectorizer = tool.construct_bow_unigrams(df[text_preproc + '_swrem'])
    report, dict_result = tool.eval_cv(X, y, clf, bencana)
    sr_tc_swrem = pd.Series(dict_result).sort_index()
    df_result[text_preproc + '_swrem_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result[text_preproc + '_swrem_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result[text_preproc + '_swrem_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])


    X, vectorizer = tool.construct_bow_unigrams(df[text_preproc + '_stem'])
    report, dict_result = tool.eval_cv(X, y, clf, bencana)
    sr_tc_stem = pd.Series(dict_result).sort_index()
    df_result[text_preproc + '_stem_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result[text_preproc + '_stem_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result[text_preproc + '_stem_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])


    X, vectorizer = tool.construct_bow_unigrams(df[text_preproc + '_swrem_stem'])
    report, dict_result = tool.eval_cv(X, y, clf, bencana)
    sr_tc_swrem_stem = pd.Series(dict_result).sort_index()
    df_result[text_preproc + '_swrem_stem_P'] = pd.Series([ t['Y']['precision'] for t in report ])
    df_result[text_preproc + '_swrem_stem_R'] = pd.Series([ t['Y']['recall'] for t in report ])
    df_result[text_preproc + '_swrem_stem_F1'] = pd.Series([ t['Y']['f1-score'] for t in report ])

    df_result.loc['MEAN'] = df_result.mean()
    df_result = df_result[[
        text_preproc + '_lower_P', text_preproc + '_swrem_P', text_preproc + '_stem_P', text_preproc + '_swrem_stem_P',
        text_preproc + '_lower_R', text_preproc + '_swrem_R', text_preproc + '_stem_R', text_preproc + '_swrem_stem_R',
        text_preproc + '_lower_F1', text_preproc + '_swrem_F1', text_preproc + '_stem_F1', text_preproc + '_swrem_stem_F1',
    ]]

    print(df_result.round(3))

    result = f_oneway(
            df_result[text_preproc + '_lower_P'].to_numpy(),
            df_result[text_preproc + '_swrem_P'].to_numpy(),
            df_result[text_preproc + '_stem_P'].to_numpy(),
            df_result[text_preproc + '_swrem_stem_P'].to_numpy(),
            )
    print("ANNOVA P : %0.3f, %0.3f" % result)
    
    result = f_oneway(
            df_result[text_preproc + '_lower_R'].to_numpy(),
            df_result[text_preproc + '_swrem_R'].to_numpy(),
            df_result[text_preproc + '_stem_R'].to_numpy(),
            df_result[text_preproc + '_swrem_stem_R'].to_numpy(),
            )
    print("ANNOVA R : %0.3f, %0.3f" % result)

    result = f_oneway(
            df_result[text_preproc + '_lower_F1'].to_numpy(),
            df_result[text_preproc + '_swrem_F1'].to_numpy(),
            df_result[text_preproc + '_stem_F1'].to_numpy(),
            df_result[text_preproc + '_swrem_stem_F1'].to_numpy(),
            )
    print("ANNOVA F1 : %0.3f, %0.3f" % result)


   # COHRAN Q-Test
    y_tc_lower = sr_tc_lower.to_numpy()
    y_tc_swrem = sr_tc_swrem.to_numpy()
    y_tc_stem  = sr_tc_stem.to_numpy()
    y_tc_swrem_stem  = sr_tc_swrem_stem.to_numpy()
    q, p_value = cochrans_q(y, y_tc_lower, y_tc_swrem, y_tc_stem, y_tc_swrem_stem)
    print("COHRAN Q-Test: q: %0.3f, p_value: %0.3f" % (q, p_value))

    l_repr =  [ text_preproc + '_lower', text_preproc + '_swrem', text_preproc + '_stem', text_preproc + '_swrem_stem' ]
    l_rslt =  [ y_tc_lower, y_tc_swrem, y_tc_stem, y_tc_swrem_stem ]
    l_pair = list(zip(l_repr, l_rslt))

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
            print(tb)
            chi2, p = mcnemar(ary=tb, corrected=True)

            l_mcnemar_rslt.append("{chi2:.3f}".format(chi2=chi2))
            l_mcnemar_rslt.append("{p:.3f}".format(p=p))
            print(f"McNemar %s v %s:  chi2, p_value : %0.3f %0.3f" 
                    % (k0, k1, chi2, p))
    print(" ".join(l_mcnemar_rslt))
