#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 15:25:19 2024

@author: pauline
"""

import conllup.conllup as cup
import spacy
from dataclasses import dataclass
from typing import Optional
#import sys


@dataclass
class Nent:
    """classe contenant le texte et les annotations des entités nommées"""
    text: [str]
    label: str
    start: Optional[int] = None
    end: Optional[int] = None

#chemin = sys.argv[1]
chemin = "../../conll/test1.conllu"

data = cup.readConlluFile(chemin)
nlp = spacy.load("fr_core_news_lg")


def extract_nents_index(nents:list, analysis_conll:list)->list:
    """ Extract the spacy indexes of the first and last token for each named 
    entity
    
    Parameters :
    ----------
    nents : list
        list of named entities (object nent) without start nor end values
    analysis_conll : list
        list of token, extracted from the input conll file
        
    Returns :
    ----------
    nents_w_index : list
        list of named entities with start and end values
    """
    
    nents_w_index = []
    for entite in nents:
        liste = list(entite.text)
        rectif=[]
        for i, tok in enumerate(liste) :
            if str(tok) == "-":
                rectif.append(i)
        
        if rectif :
            for index in rectif[::-1] :
                new_tok = (str(
                    entite.text[index-1]) 
                    + str(entite.text[index]) 
                    + str(entite.text[index+1])
                    )
                liste[index-1]= new_tok
                del liste[index+1]
                del liste[index]
                    
        for id_mot, mot in enumerate(analysis_conll):
            if str(liste[0]) == mot:
                start = id_mot
                end = id_mot+len(liste)-1
                end_slice = end + 1
                
                if str(liste[-1]) == analysis_conll[end]:
                    # print(
                    # f""""pan {entite.label} 
                    # = {id_mot}-{id_mot+len(entite.text)-1}""")
                    # print(f"slice : {texte_list[debut:fin_slice]}")
                    nents_w_index.append(Nent(
                        entite.text,
                        entite.label,
                        start,
                        end_slice))
                    
    return nents_w_index


def sentence_w_nents(nents_w_index:list, analysis_conll:dict)->list:
    """ inject the NER analysis from spaCy into the input conll file
    
    Parameters :
    ----------
    nents_w_index : list
        list of named entities and their indexes (object nent)
    analysis_conll : list
        list of token, extracted from the input conll file
        
    Returns :
    ----------
    analysis_conll : list
        list of tokens with the nents labels added
    """
    
    if nents_w_index:
        for entity in nents_w_index:
            for token_i in analysis_conll.keys():
                 if int(token_i) in range(entity.start+1, entity.end+1):
                     analysis_conll[token_i]["MISC"]["NENT"] = str(
                         entity.label)
    #              else:
    #                  analysis_conll[token_i]["MISC"]["NER"] = "None"
    # else:
    #      for token_i in analysis_conll.keys():
    #          analysis_conll[token_i]["MISC"]["NER"] = "None"
            
    return analysis_conll


sentences_json = []
for index_sentence in range(1000) :
    
    # annoter avec spacy :
    text_raw = data[index_sentence]["metaJson"]["text"]
    analysis_spacy = nlp(text_raw)
    nents = [Nent(nlp(ent.text), ent.label_) for ent in analysis_spacy.ents]
    
    # annotation conll :
    sentence_conll = data[index_sentence]["treeJson"]["nodesJson"]
    analysis_conll = [mot["FORM"] for mot in sentence_conll.values()]
    
    # enrichir les nents avec leurs indexs
    nents_w_index = extract_nents_index(nents, analysis_conll)
    
    # enrichir les phrases conll
    data[index_sentence]["treeJson"]["nodesJson"] = sentence_w_nents(
        nents_w_index, sentence_conll)
    sentences_json.append(data[index_sentence])

print("analyse = OK")

# écriture conll entichi    
cup.writeConlluFile("res_con.conllu", sentences_json)
print("fichier conll crée")
    
