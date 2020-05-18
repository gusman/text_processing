import pandas as pd 
import sys
from sklearn.svm import SVC

import classifier_tool as tool


def test_rep(rep, df, clf, fold=10):
    X = tool.construct_tfidf_unigrams(df[rep])
    y = df['class']
    report = tool.eval_cv(fold, X, y, clf)
    
    y_report = [ d['Y'] for d in report ]
    n_report = [ d['N'] for d in report ]
    
    df_y = pd.DataFrame(y_report)
    df_n = pd.DataFrame(n_report)
    df_y.loc['avg'] = df_y.mean()
    df_n.loc['avg'] = df_n.mean()
    df_y_avg = df_y.loc[['avg']]
    df_y_avg = df_y_avg.rename(
                columns={
                    'precision' : 'y_prec', 
                    'recall':'y_recall', 
                    'f1-score' : 'y_f1', 
                    'support' : 'y_support'}
                )
    
    return df_y_avg, df_y, df_n

if __name__ == "__main__":
    f_in = sys.argv[1]
    df = pd.read_json(f_in)
    
    rep_list = [
        't_lower', 'c_lower', 'tc_lower',
        't_swrem', 'c_swrem', 'tc_swrem',
        't_stem', 'c_stem', 'tc_stem',
        't_swrem_stem', 'c_swrem_stem', 'tc_swrem_stem',
    ]
    
    f_base = f_in.replace('.json', '')
    df = pd.read_json(f_in)
    
    clf = SVC()
    df_summary = pd.DataFrame()

    for rep in rep_list:
        df_y_avg, df_y, df_n = test_rep(rep, df, clf)
        df_summary[rep] = df_y_avg.loc['avg']
   
        f_y_report = f_base + '_repr_test_' + rep + '_Y.xlsx'
        f_n_report = f_base + '_repr_test_' + rep + '_N.xlsx'
        df_y.to_excel(f_y_report)
        df_y.to_excel(f_n_report)
   
    f_sum_report = f_base + '_repr_test_Y_SUM.xlsx'
    df_summary.to_excel(f_sum_report)
    