#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 11:26:50 2024

Librairie des fonctions de projection : annotation de token comme humain en 
s'appuyant sur les annotations précédentes

@author: pauline
"""
import re


def grab_subj_coor_verb(sentence_nodes, id_token, dicoval):
    """
    Get the antecedent of a subject when its verb is coordinated with a verb
    whose subject is necessarily human.

    Parameters :
    ----------
    sentence_nodes : list
        list dictionnaries, each of them being a conll token. The whole list
        is a conll sentence
    id_token : str
        id of the verb
    dicoval : dictionnary
        dictionnary of valences per verbs
        
    Returns :
    ----------
    id_subj : str/0
        
    """
    args = [sentence_nodes[x]["DEPREL"] for x in sentence_nodes if str(sentence_nodes[x]["HEAD"])==id_token]
    if "subj" in args :
        return 0
    else :
        lemma_v = str(sentence_nodes[id_token]["LEMMA"])
        if dicoval.get(lemma_v, 0):
            if all(s.startswith("2") for s in dicoval[lemma_v].values()):
                id_head = str(sentence_nodes[id_token]["HEAD"])
                id_subj = 0
                if int(id_head):
                    if re.search("comp:aux", str(sentence_nodes[id_head]["DEPREL"])):
                        id_head = str(sentence_nodes[id_head]["HEAD"])
                        
                    for id_arg in sentence_nodes:
                        if str(sentence_nodes[id_arg]["HEAD"]) == id_head:
                            if str(sentence_nodes[id_arg]["DEPREL"]) == "subj":
                                id_subj = id_arg
                            else:
                                return 0
                    if id_subj:
                        return id_subj
                else :
                    return 0
            else :
                return 0


def grab_antecedent(sentence_nodes,id_token):
    """
    Get the id of the antecedent of a human relative pronoun

    Parameters :
    ----------
    sentence_nodes : list
        list dictionnaries, each of them being a conll token. The whole list
        is a conll sentence
    id_token : str
        id of the relative pronoun
        
    Returns :
    ----------
    id_antecedent : str/0
        
    """
    id_verb_rel = str(sentence_nodes[id_token]["HEAD"])
    id_antecedent = str(sentence_nodes[id_verb_rel]["HEAD"])
    if sentence_nodes[id_antecedent]["UPOS"] in ["NOUN", "PROPN", "PRON"]:
        return id_antecedent
    else:
        return 0


def project_antecedent(sentence_nodes):
    """
    Annotate antecedent as human

    Parameters :
    ----------
    sentence_nodes : list
        list dictionnaries, each of them being a conll token. The whole list
        is a conll sentence
        
    Returns :
    ----------
    sentence_nodes : list
        list dictionnaries, each of them being a conll token. The whole list
        is a conll sentence. The antecedent of human relative pronouns are now
        human
        """
    
    for id_token in sentence_nodes:
        # récupération des antécédents
        if sentence_nodes[id_token]["FEATS"].get("PronType") == "Rel":
            score_pron = int(sentence_nodes[id_token]["MISC"].get("HUM_SCORE", 0))
            if score_pron:
                id_antecedent = grab_antecedent(sentence_nodes,id_token)
                if id_antecedent:
                    score = int(sentence_nodes[id_antecedent]["MISC"].get("HUM_SCORE", 0))
                    if score < 70:
                        sentence_nodes[id_antecedent]["MISC"]["HUM_SCORE"] = int(sentence_nodes[id_antecedent]["MISC"].get("HUM_SCORE", 0))+ 70
                        del sentence_nodes[id_token]["MISC"]["HUM_SCORE"]

    return sentence_nodes
        

def project_nom_coor(sentence_nodes):
    """
    Project HUM_SCORE on nouns when they are coordinated with a noun that
    already has a HUM_SCORE

    Parameters :
    ----------
    sentence_nodes : list
        list dictionnaries, each of them being a conll token. The whole list
        is a conll sentence
        
    Returns :
    ----------
    sentence_nodes : list
        list dictionnaries, each of them being a conll token. The whole list
        is a conll sentence.
        """
    
    for id_token in sentence_nodes:
        # projection à partir des coordinations
        if sentence_nodes[id_token]["DEPREL"] == "conj:coord":
            # Noms coordonnés avec un nom annoté humain
            if sentence_nodes[id_token]["UPOS"] in ["NOUN", "PROPN", "PRON"]:
                id_head = str(sentence_nodes[id_token]["HEAD"])
                score = int(sentence_nodes[id_head]["MISC"].get("HUM_SCORE", 0))
                if score:
                    sentence_nodes[id_token]["MISC"]["HUM_SCORE"] = int(sentence_nodes[id_token]["MISC"].get("HUM_SCORE", 0))+ 10

    return sentence_nodes
     
                   
def project_val_coor(sentence_nodes, dicoval):
    """
    Project HUM_SCORE on subjects when their verb is coordinated with a verb 
    whose subject is necessarily human

    Parameters :
    ----------
    sentence_nodes : list
        list dictionnaries, each of them being a conll token. The whole list
        is a conll sentence
        
    Returns :
    ----------
    sentence_nodes : list
        list dictionnaries, each of them being a conll token. The whole list
        is a conll sentence. 
        """
    for id_token in sentence_nodes:
        # projection de la valence du second verbe coordonné si le sujet est nécessairement humain
        if sentence_nodes[id_token]["UPOS"] == "VERB":
            id_subj = grab_subj_coor_verb(sentence_nodes, id_token, dicoval)
            if id_subj:
                score = int(sentence_nodes[id_subj]["MISC"].get("HUM_SCORE", 0))
                sentence_nodes[id_subj]["MISC"]["HUM_SCORE"] = score + 20
    
    return sentence_nodes
                      

def project_subj_comp(sentence_nodes):
    """
    Project HUM_SCORE on subjects when their subject complement has a HUM_SCORE

    Parameters :
    ----------
    sentence_nodes : list
        list dictionnaries, each of them being a conll token. The whole list
        is a conll sentence
        
    Returns :
    ----------
    sentence_nodes : list
        list dictionnaries, each of them being a conll token. The whole list
        is a conll sentence. 
        """
    for id_token in sentence_nodes:
        # projection depuis un attribut du sujet humain sur le sujet :
        if str(sentence_nodes[id_token]["DEPREL"]) == "comp:pred":
            score = int(sentence_nodes[id_token]["MISC"].get("HUM_SCORE", 0))
            if score:
                for token_arg in sentence_nodes:
                    if str(sentence_nodes[token_arg]["HEAD"]) ==  str(sentence_nodes[id_token]["HEAD"]):
                        if str(sentence_nodes[token_arg]["DEPREL"]) == "subj":
                            sentence_nodes[token_arg]["MISC"]["HUM_SCORE"] = int(sentence_nodes[token_arg]["MISC"].get("HUM_SCORE", 0)) + 40

    return sentence_nodes
                                