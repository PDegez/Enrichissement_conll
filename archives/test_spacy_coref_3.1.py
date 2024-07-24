#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 14:09:43 2024

@author: pauline

Tester le module coreferee de spacy 3.1 sur un corpus de texte et non de
phrases
"""

import spacy, argparse, re, sys
from pathlib import Path
import conllup.conllup as cup
from spacy.tokens import Doc

#chemin = sys.argv[1]
chemin = "../../conll/SUD_French-ParisStories-r2.13/ParisStories_2022_chienGourmand.conllu"
data = cup.readConlluFile(chemin)

# print(data[0])
# print(len(data[0]["treeJson"]["nodesJson"].keys()))
# print(data[0]["treeJson"]["nodesJson"]["1"]["FORM"])
# token = [token["FORM"] for token in data[0]["treeJson"]["nodesJson"].keys()]


def custom_tokenizer(nlp, tokens_conll:list)->Doc:
    """ Use the tokenisation from conll file
    
    Parameters :
    ----------
    nlp : spacy pipeline
        spacy pipeline
    tokens_conll : list
        list of token, extracted from the input conll file
        
    Returns :
    ----------
    Doc_object : Doc
        Doc object to be treated as a document with a preset tokenization 
        by spacy
    """
    
    spaces = [True] * (len(tokens_conll) - 1) + [False]
    return Doc(nlp.vocab, words=tokens_conll, spaces=spaces)


full_text = [token["FORM"] for sentence in data for token in sentence["treeJson"]["nodesJson"].values()]


debut = 0 
fin = 0 

for id_sentence, sentence in enumerate(data):
    debut = fin
    len_sent = len(data[id_sentence]["treeJson"]["nodesJson"].keys())
    fin = debut + len_sent
    print(f"phrase {id_sentence+1} \tdébut : {debut}, \tfin : {fin}")
    print(full_text[debut:fin])
    

full_text = [token["FORM"] for sentence in data for token in sentence["treeJson"]["nodesJson"].values()]

nlp = spacy.load("fr_core_news_lg")
nlp.add_pipe('coreferee')

doc = custom_tokenizer(nlp, full_text)
for name, pipe in nlp.pipeline:
    analysis_spacy = pipe(doc)
                
chains = [chain for chain in iter(analysis_spacy._.coref_chains)]
for chain in chains:
    print(chain.pretty_representation)