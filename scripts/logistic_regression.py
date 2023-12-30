#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 14:39:09 2023

@author: orane
"""
import pandas as pd
from construct_corpus import construct_full_corpus_train, construct_full_corpus_test
from extract_data import load_stopwords
from collections import defaultdict
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
import seaborn as sns
import matplotlib.pyplot as plt




stopwords = load_stopwords("../utils/stopwords_all.txt")
x_train, y_train = construct_full_corpus_train()
x_test, y_test = construct_full_corpus_test()
param_grid = {
'tfidf__max_df': [0.5, 0.75, 1.0],
'tfidf__ngram_range': [(1, 1), (1, 2)],
'clf__C': [0.1, 1, 10],
'clf__solver': ['liblinear', 'lbfgs']
}
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words=stopwords)),
    ('clf', LogisticRegression(max_iter=1000, 
                               class_weight='balanced'))
])
grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=1, verbose=2)
grid_search.fit(x_train, y_train)
print("Meilleurs paramètres: ", grid_search.best_params_)
print("Meilleur score: ", grid_search.best_score_)

results = pd.DataFrame(grid_search.cv_results_)
results = results.sort_values(by='rank_test_score')
results.to_csv('../utils/grid_search_results.csv', index=False)


class_names = pipeline.named_steps['clf'].classes_
y_pred = grid_search.predict(x_test)
print(classification_report(y_test, y_pred))
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='g', cmap='Blues',xticklabels=class_names, yticklabels=class_names)
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix')
plt.show()
    
