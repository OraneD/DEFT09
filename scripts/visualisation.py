#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 00:46:17 2023

@author: orane
"""

from extract_data import extract_train, extract_test, select_files, extract_test, clean_text
from collections import defaultdict
import matplotlib.pyplot as plt

def construct_full_corpus():
    dico_corpus = defaultdict(list)
    data_train_en = extract_train("../train/deft09_parlement_appr_en.xml", "en")
    data_train_fr = extract_train("../train/deft09_parlement_appr_fr.xml", "fr")
    data_train_it = extract_train("../train/deft09_parlement_appr_it.xml", "it")
    for data, lang in [(data_train_en, "EN"), (data_train_fr, "FR"), (data_train_it, "IT")]:
        for parti, texte in data:
            dico_corpus[(parti, lang)].append(texte)

    return dict(dico_corpus)


def show_histogram(corpus):
    count_by_parti_lang = defaultdict(lambda: defaultdict(int))
    for (parti, lang), textes in corpus.items():
        count_by_parti_lang[parti][lang] += len(textes)
    partis = count_by_parti_lang.keys()
    lang_counts = {"EN": [], "FR": [], "IT": []}

    for parti in partis:
        for lang in ["EN", "FR", "IT"]:
            lang_counts[lang].append(count_by_parti_lang[parti][lang])

    bar_width = 0.35
    index = range(len(partis))

    plt.bar(index, lang_counts["EN"], bar_width, label="EN")
    plt.bar(index, lang_counts["FR"], bar_width, bottom=lang_counts["EN"], label="FR")
    plt.bar(index, lang_counts["IT"], bar_width, bottom=[i+j for i,j in zip(lang_counts["EN"], lang_counts["FR"])], label="IT")

    plt.xlabel('Partis')
    plt.ylabel('Nombre de textes')
    plt.title('Nombre de textes par parti et par langue')
    plt.xticks(index, partis)
    plt.legend()

    plt.tight_layout()
    plt.show()
    