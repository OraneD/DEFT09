#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 14:39:09 2023

@author: orane
"""

from construct_corpus import construct_full_corpus_train, construct_full_corpus_test
from collections import defaultdict
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt



def main():
    x_train, y_train = construct_full_corpus_train()
    x_test, y_test = construct_full_corpus_test()
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LogisticRegression(max_iter=1000, 
                                   class_weight='balanced'))
    ])
    
    pipeline.fit(x_train, y_train)
    class_names = pipeline.named_steps['clf'].classes_
    y_pred = pipeline.predict(x_test)
    print(classification_report(y_test, y_pred))
    conf_matrix = confusion_matrix(y_test, y_pred)
    sns.heatmap(conf_matrix, annot=True, fmt='g', cmap='Blues',xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')
    plt.title('Confusion Matrix')
    plt.show()
    
if __name__ == "__main__":
    main()