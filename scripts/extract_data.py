#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 22:26:15 2023

@author: orane
"""

import xml.etree.ElementTree as ET
import argparse



def extract_train(xml_file):
    data = []
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for doc in root.findall(".//doc") :
        for child in doc.findall(".//") :
                if child.tag == "PARTI":
                    parti_name = child.attrib["valeur"]
                    print(parti_name)
                elif child.tag == "texte" :
                    doc_text = ""
                    text_elem = child
                    for paragraph in text_elem.findall(".//p") :
                            doc_text += extract_text(paragraph)
        data.append((parti_name,doc_text))
    return data
        

def extract_test(language):
    """
    Extraction des données du set de test et des partis correspondants dans les références
    La fonction prend en argument la langue considérée
    """
    xml_file,ref = select_files(language)
    dico_ref = {}
    with open(ref, "r") as file :
        lines = file.readlines()
        for line in lines :
            num, parti = line.split("\t")
            dico_ref[num] = parti
    data = []
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for doc in root.findall(".//doc") :
        num = doc.attrib["id"]
        parti = dico_ref[num].strip()
        doc_text = ""
        for paragraph in doc.findall(".//p") :
                doc_text += extract_text(paragraph)
        data.append((parti,doc_text))
    return data


def extract_text(element):
    """
    Fonction pour gérer les balises <anonym/> dans l'ensemble de test
    Permet de récupérer tous le texte d'un élément XML y compris le texte des sous-éléments
    """
    text = ""
    if element.text:
        text += element.text.strip()
    for subelement in element:
        text += extract_text(subelement)
        if subelement.tail:
            text += subelement.tail.strip()
    return text

def select_files(language):
    """
    Retourne le chemin des fichiers pour extraire les données de test 
    en fonction de la langue désirée.
    """
    if language == "fr":
        xml_file = "../test/deft09_parlement_test_fr.xml"
        ref = "../ref/deft09_parlement_ref_fr.txt"
    elif language == "en":
        xml_file = "../test/deft09_parlement_test_en.xml"
        ref = "../ref/deft09_parlement_ref_en.txt"
    elif language == "it":
        xml_file = "../test/deft09_parlement_test_it.xml"
        ref = "../ref/deft09_parlement_ref_it.txt"
    else :
        return "Ce langage n'existe pas"
    return (xml_file, ref)

test_it = extract_test("it")
print(test_it[313])


        




                
    