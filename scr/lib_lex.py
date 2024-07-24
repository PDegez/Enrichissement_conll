#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 15:09:23 2024

@author: pauline
"""

def add_lex(sentence_nodes, lex):  
    
    for token in sentence_nodes:
        if sentence_nodes[token]["UPOS"] in ["NOUN", "PROPN", "PRON"]:
            sentence_nodes[token]["MISC"]["HUM_SCORE"] = 0
            if sentence_nodes[token]["MISC"].get("NENT"):
                if sentence_nodes[token]["MISC"]["NENT"] == "PER":
                    sentence_nodes[token]["MISC"]["HUM_SCORE"] += 2
            if sentence_nodes[token]["LEMMA"] in lex:
                sentence_nodes[token]["MISC"]["HUM_SCORE"] += 1
    
    return sentence_nodes