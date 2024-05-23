#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 15:25:19 2024

@author: pauline
"""

import conllup.conllup as cup
import spacy
from dataclasses import dataclass
#import sys


@dataclass
class Ner:
    """classe contenant le texte et les annotations des entités nommées"""
    text: [str]
    label: str
    debut: None
    fin: None

#chemin = sys.argv[1]
chemin = "../../conll/test1.conllu"

data = cup.readConlluFile(chemin)
nlp = spacy.load("fr_core_news_lg")

def extract_NER(NER:list, texte_list)->list:
    NER_enrichi = []
    for entite in NER:
        liste = list(entite.text)
        rectif=[]
        for i, tok in enumerate(liste) :
            if str(tok) == "-":
                rectif.append(i)
        
        if rectif :
            for index in rectif[::-1] :
                new_tok = str(entite.text[index-1]) + str(entite.text[index]) + str(entite.text[index+1])
                liste[index-1]= new_tok
                del liste[index+1]
                del liste[index]
                    
        for id_mot, mot in enumerate(texte_list):
            if str(liste[0]) == mot:
                debut = id_mot
                fin = id_mot+len(liste)-1
                fin_slice = fin + 1
                
                if str(liste[-1]) == texte_list[fin]:
                    print(
                    f"span de {entite.label} = {id_mot}-{id_mot+len(entite.text)-1}")
                    print(f"slice : {texte_list[debut:fin_slice]}")
                    NER_enrichi.append(Ner(entite.text, entite.label, debut, fin_slice))
    return NER_enrichi

def enrichissement_phrase(NER_enrichi:list, phrase_analyse_cnl)->list:
    if NER_enrichi:
        for NER in NER_enrichi:
            for token_i in phrase_analyse_cnl.keys():
                 if int(token_i) in range(NER.debut+1, NER.fin+1):
                     phrase_analyse_cnl[token_i]["MISC"]["NER"] = str(NER.label)
                 else:
                     phrase_analyse_cnl[token_i]["MISC"]["NER"] = "None"
    else:
         for token_i in phrase_analyse_cnl.keys():
             phrase_analyse_cnl[token_i]["MISC"]["NER"] = "None"
            
    return phrase_analyse_cnl


sentences_json = []
n = 1
for index_phrase in range(1000) :
    # annoter avec spacy :
    texte = data[index_phrase]["metaJson"]["text"]
    texte_nlp = nlp(texte)
    NER = [Ner(nlp(ent.text), ent.label_, None, None) for ent in texte_nlp.ents]
    
    # annotation conll :
    phrase_analyse_cnl = data[index_phrase]["treeJson"]["nodesJson"]
    texte_list = [mot["FORM"] for mot in phrase_analyse_cnl.values()]
    NER_enrichi = extract_NER(NER, texte_list)
    data[index_phrase]["treeJson"]["nodesJson"] = enrichissement_phrase(NER_enrichi, phrase_analyse_cnl)
    sentences_json.append(data[index_phrase])
    n+=1
    
print("analyse = OK")
cup.writeConlluFile("res_con.conllu", sentences_json)
    
