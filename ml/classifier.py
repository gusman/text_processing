import pandas as pd 
import sys
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

import classifier_tool as tool

if __name__ == "__main__":
    f_in = sys.argv[1]
    df = pd.read_json(f)
  
    x_feature = tool.construct_tfidf(df['w_tokens'])    
    y_target = df['class']

    clf_svm = LinearSVC()
    #clf_rf = RandomForestClassifier(max_depth=100, random_state=0)
    #tool.eval_cv(10, x_feature, y_target, clf_rf)
    tool.eval_split(0.3, x_feature, y_target, clf_svm)
    
    clf_result = clf_svm.predict(x_feature)
    print(clf_result)
#    print(classification_report(y_target, clf_result))

#    scores = cross_validate(clf_svm, x_feature, y_target, cv=5)
#    clf_svm.fit(X_train, y_train)
#    clf_result = clf_svm.predict(X_test)
#    print(classification_report(y_test, clf_result))
