#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 00:46:17 2023

@author: orane
"""

from extract_data import extract_train, extract_test, select_files, extract_test, clean_text
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

def construct_full_corpus():
    dico_corpus = defaultdict(list)
    data_train_en = extract_train("../train/deft09_parlement_appr_en.xml", "en")
    data_train_fr = extract_train("../train/deft09_parlement_appr_fr.xml", "fr")
    data_train_it = extract_train("../train/deft09_parlement_appr_it.xml", "it")
    for data, lang in [(data_train_en, "EN"), (data_train_fr, "FR"), (data_train_it, "IT")]:
        for parti, texte in data:
            dico_corpus[(parti, lang)].append(texte)

    return dict(dico_corpus)

def construct_full_corpus_test():
    dico_corpus = defaultdict(list)

    data_test_en = extract_test("en")
    data_test_fr = extract_test("fr")
    data_test_it = extract_test("it")
    all_data = data_test_en + data_test_fr + data_test_it
    for data, lang in [(data_test_en, "EN"), (data_test_fr, "FR"), (data_test_it, "IT")]:
        for parti, texte in data:
            dico_corpus[(parti, lang)].append(texte)

    return dico_corpus


corpus = construct_full_corpus()
corpus_test = construct_full_corpus_test()

def show_side_by_side_histogram(corpus_train, corpus_test):

    def calculate_counts(corpus):
        count_by_parti_lang = defaultdict(lambda: defaultdict(int))
        for (parti, lang), textes in corpus.items():
            count_by_parti_lang[parti][lang] += len(textes)
        return count_by_parti_lang
    
    count_train = calculate_counts(corpus_train)
    count_test = calculate_counts(corpus_test)
    partis_train = sorted(count_train.keys())
    partis_test = sorted(count_test.keys())
    lang_counts_train = {"EN": [], "FR": [], "IT": []}
    lang_counts_test = {"EN": [], "FR": [], "IT": []}

    for parti in partis_train:
        for lang in ["EN", "FR", "IT"]:
            lang_counts_train[lang].append(count_train[parti][lang])
    for parti in partis_test:
        for lang in ["EN", "FR", "IT"]:
            lang_counts_test[lang].append(count_test[parti][lang])

    bar_width = 0.35
    index_train = np.arange(len(partis_train))
    index_test = np.arange(len(partis_test)) + len(partis_train) + bar_width

    fig, ax = plt.subplots(figsize=(15, 7))
    ax.bar(index_train, lang_counts_train["EN"], bar_width, label="EN Train")
    ax.bar(index_train, lang_counts_train["FR"], bar_width, bottom=lang_counts_train["EN"], label="FR Train")
    ax.bar(index_train, lang_counts_train["IT"], bar_width, bottom=[i+j for i,j in zip(lang_counts_train["EN"], lang_counts_train["FR"])], label="IT Train")

    ax.bar(index_test, lang_counts_test["EN"], bar_width, label="EN Test")
    ax.bar(index_test, lang_counts_test["FR"], bar_width, bottom=lang_counts_test["EN"], label="FR Test")
    ax.bar(index_test, lang_counts_test["IT"], bar_width, bottom=[i+j for i,j in zip(lang_counts_test["EN"], lang_counts_test["FR"])], label="IT Test")

    ax.set_xlabel('Partis')
    ax.set_ylabel('Nombre de textes')
    ax.set_xticks(list(index_train) + list(index_test))
    ax.set_xticklabels([parti for parti in partis_train] + [parti for parti in partis_test], rotation=45)
    ax.legend()
    plt.tight_layout()

    return fig

fig = show_side_by_side_histogram(corpus, corpus_test)

plt.show()



    