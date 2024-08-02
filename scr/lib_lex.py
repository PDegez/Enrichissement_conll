#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 15:09:23 2024

Fonction add_lex : annotation des noms et pronoms à l'aide de la liste extraite
de spiderlex


@author: pauline
"""

def add_lex(sentence_nodes, lex):
    """
    annotation des noms et pronoms à l'aide de la liste extraite
    de spiderlex

    Parameters :
    ----------
    sentence_nodes : list
        list dictionnaries, each of them being a conll token. The whole list
        is a conll sentence
    lex : list
        list of human lexemes, extracted from spiderlex
        
    Returns :
    ----------
    sentence_nodes : list
        list dictionnaries, each of them being a conll token. The whole list
        is a conll sentence. The human tokens now have a HUM_SCORE
        
    """
    
    for token in sentence_nodes:
        if sentence_nodes[token]["UPOS"] in ["NOUN", "PROPN", "PRON"]:
            sentence_nodes[token]["MISC"]["HUM_SCORE"] = 0
            if sentence_nodes[token]["MISC"].get("NENT"):
                if sentence_nodes[token]["MISC"]["NENT"] == "PER":
                    sentence_nodes[token]["MISC"]["HUM_SCORE"] += 2
            if sentence_nodes[token]["LEMMA"] in lex:
                sentence_nodes[token]["MISC"]["HUM_SCORE"] += 1
    
    return sentence_nodes