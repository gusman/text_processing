import pandas as pd 
import sys
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer 
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report 

import classifier_tool as tool

if __name__ == "__main__":
    f_in = sys.argv[1]
    df = pd.read_json(f_in)

    X = df['tc_lower']
    y = df['label'].to_numpy()
    df_result = pd.DataFrame()

    #X, vectorizer = tool.construct_bow_unigrams(df['tc_lower'])
    #report, dict_result = tool.eval_cv(5, X, y, clf)

    all_features = FeatureUnion([
                ('tfidf', TfidfVectorizer(ngram_range=(1,2), max_features=300)),
                ('cv', CountVectorizer(ngram_range=(1,1))),
            ])

    pipe = Pipeline([
                ('features', all_features),
                ('clf', MultinomialNB()),
            ])

    X_train, X_test, y_train, y_test =\
        train_test_split(X, y, test_size=0.3, random_state=0)

    pipe.fit(X_train, y_train)
    clf_result = pipe.predict(X_test)
    print(classification_report(y_test, clf_result, zero_division=1))
