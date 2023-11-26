#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 15:32:57 2023

@author: orane
"""

from extract_data import extract_train, extract_test, select_files, extract_test, clean_text
from collections import defaultdict

'''
Construction de dictionnaires qui ont pour clefs les partis et pour 
valeurs les textes
'''
def construct_full_corpus_train():
    dico_corpus = defaultdict(list)
    data_train_en = extract_train("../train/deft09_parlement_appr_en.xml", "en")
    data_train_fr = extract_train("../train/deft09_parlement_appr_fr.xml", "fr")
    data_train_it = extract_train("../train/deft09_parlement_appr_it.xml", "it")
    all_data = data_train_en + data_train_fr + data_train_it
    for parti, texte in all_data :
        dico_corpus[parti].append(texte)
    dico_corpus = dict(dico_corpus)
    
    x_train = [texte for textes in dico_corpus.values() for texte in textes]
    y_train = [parti for parti, textes in dico_corpus.items() for _ in textes]

    return x_train, y_train

def construct_full_corpus_test():
    dico_corpus = defaultdict(list)

    data_test_en = extract_test("en")
    data_test_fr = extract_test("fr")
    data_test_it = extract_test("it")
    all_data = data_test_en + data_test_fr + data_test_it
    for parti, texte in all_data :
        dico_corpus[parti].append(texte)
    dico_corpus = dict(dico_corpus)

    x_test = [texte for textes in dico_corpus.values() for texte in textes]
    y_test = [parti for parti, textes in dico_corpus.items() for _ in textes]
    return x_test, y_test
