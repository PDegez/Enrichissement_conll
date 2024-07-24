#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 15:14:44 2024

@author: pauline
"""
import spacy
from dataclasses import dataclass


@dataclass
class Ner:
    """classe contenant le texte et les annotations des entités nommées"""
    text: [str]
    label: str

conll = ["j'", "aime", "les", "Crusaders", "de", "Nouvelle-Zélande"]
text = "J'aime les Crusaders de Nouvelle-Zélande"

nlp = spacy.load("fr_core_news_lg")
doc = nlp(text)

nents = []
for entite in doc.ents :
    label = entite.label_
    text = list(nlp(entite.text))
    rectification_tiret = []
    for i, token in enumerate(text):
        if str(token) == "-":
            rectification_tiret.append(i)
    
    if rectification_tiret:
        for index_token in rectification_tiret[::-1]:
            token_rectifie = (
                str(text[index_token-1])
                + str(text[index_token])
                + str(text[index_token+1])
                )
            print(token_rectifie)
            text[index_token-1] = token_rectifie
            del text[index_token+1]
            del text[index_token]
    
            nents.append(Ner(text, label))
    
for entite in nents :
    print(entite)
    for id_mot, mot in enumerate(conll):
        if str(entite.text[0]) == mot :
            debut = id_mot
            fin = id_mot+len(entite.text)
            
            if str(entite.text[-1]) == conll[fin-1]:
                print(f"longueur entite = {len(entite.text)}")
                print(f"slice : {conll[debut:fin]}")