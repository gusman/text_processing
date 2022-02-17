from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report 
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_validate
from sklearn.model_selection import KFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion

from . import misc

def construct_tfidf_unigrams(corpus_text):
    vectorizer = TfidfVectorizer(ngram_range=(1,1), max_features=500)
    return vectorizer.fit_transform(corpus_text), vectorizer

def construct_tfidf_bigrams(corpus_text):
    vectorizer = TfidfVectorizer(ngram_range=(2,2), max_features=500)
    return vectorizer.fit_transform(corpus_text), vectorizer

def construct_tfidf_uni_and_bigrams(corpus_text):
    vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=500)
    return vectorizer.fit_transform(corpus_text), vectorizer

def construct_bow_unigrams(corpus_text):
    vectorizer = CountVectorizer(ngram_range=(1,1), max_features=1200)
    return vectorizer.fit_transform(corpus_text), vectorizer

def construct_bow_bigrams(corpus_text):
    vectorizer = CountVectorizer(ngram_range=(2,2), max_features=1200)
    return vectorizer.fit_transform(corpus_text), vectorizer

def construct_bow_uni_and_bigrams(corpus_text):
    vectorizer = CountVectorizer(ngram_range=(1,2), max_features=1200)
    return vectorizer.fit_transform(corpus_text), vectorizer

def eval_cv(X, y, clf, bencana):
    report = []
    dict_result = {} 
    for ctr in range(1,6):
        train_index, test_index = misc.get_index(bencana, ctr)

        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        clf.fit(X_train, y_train)
        clf_result = clf.predict(X_test)

        for i,v in enumerate(test_index):
            dict_result[v] = clf_result[i]

        dict_report = classification_report(y_test, clf_result, 
                        zero_division=1, output_dict=1)
        dict_report['accuracy'] = accuracy_score(y_test, clf_result)
        report.append(dict_report)
   
    return report, dict_result
