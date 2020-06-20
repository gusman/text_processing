from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report 
from sklearn.metrics import precision_score
from sklearn.model_selection import cross_validate
from sklearn.model_selection import KFold
from sklearn.feature_extraction.text import TfidfVectorizer

def construct_tfidf_unigrams(corpus_text):
    vectorizer = TfidfVectorizer(ngram_range=(1,1), max_features=300)
    return vectorizer.fit_transform(corpus_text), vectorizer

def construct_tfidf_bigrams(corpus_text):
    vectorizer = TfidfVectorizer(ngram_range=(2,2), max_features=300)
    return vectorizer.fit_transform(corpus_text), vectorizer

def construct_tfidf_uni_and_bigrams(corpus_text):
    vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=300)
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


def eval_cv(n_splits, X, y, clf):
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=1)
    report = []
    dict_result = {} 
    ctr = 1
    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        
        clf.fit(X_train, y_train)
        
        clf_result = clf.predict(X_test)
        for i,v in enumerate(test_index):
            dict_result[v] = clf_result[i]

        dict_report = classification_report(y_test, clf_result, 
                        zero_division=1, output_dict=1)
        ctr += 1
        report.append(dict_report)
   
    return report, dict_result
    
        
    
def eval_split(test_size, X, y, clf):
    X_train, X_test, y_train, y_test =\
        train_test_split(X, y, test_size=test_size, random_state=0) 
    
    clf.fit(X_train, y_train)
    clf_result = clf.predict(X_test)
    print(classification_report(y_test, clf_result))
    
