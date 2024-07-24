#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 15:03:03 2024

fonctions et datastructure for nents

@author: pauline
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Nent:
    """classe contenant le texte et les annotations des entités nommées"""
    text: [str]
    label: str
    start: Optional[int] = None
    end: Optional[int] = None


def add_nents(nents:list, analysis_conll:dict, sentence_conll:list)->list:
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
        for id_mot, mot in enumerate(analysis_conll):
            if str(entite.text[0]).lower() == mot.lower():
                
            #if str(entite.text[0]) == mot:
                start = id_mot
                end = id_mot+len(entite.text)-1
                end_slice = end + 1
                
                if end < len(analysis_conll):
                    if str(entite.text[-1]).lower() == str(analysis_conll[end].lower()):
                        nents_w_index.append(Nent(
                        entite.text,
                        entite.label,
                        start,
                        end_slice))
                    
    return sentence_w_nents(nents_w_index, sentence_conll)


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
                            
    return analysis_conll