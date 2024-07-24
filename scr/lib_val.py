#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 15:21:28 2024

@author: pauline
"""

import re

def grab_arg_hum(cles_dict, arguments, sentence_nodes):
    arg_hum = []
    if arguments["passif"] == 0:
        if arguments.get("syn"):
            if cles_dict.get(str(arguments["syn"])):
                if re.search("2", cles_dict[arguments["syn"]]) is not None :
                    if cles_dict[str(arguments["syn"])][0] == "2":
                        if arguments.get("subj"):
                        # arg_hum.append("subj")
                            arg_hum.append(arguments.get("subj"))
                    if cles_dict[str(arguments["syn"])][1] == "2":
                        if arguments.get("comp_obj"):
                        # arg_hum.append("comp_obj")
                            arg_hum.append(arguments.get("comp_obj"))
                    if cles_dict[str(arguments["syn"])][2] == "2":
                        if arguments.get("comp_obl"):
                        # arg_hum.append("comp_obl")
                            arg_hum.append(arguments.get("comp_obl"))
    else:
        # print("passif")
        syn_pass = "110"
        if cles_dict.get(syn_pass):
            if re.search("2", cles_dict[syn_pass]) is not None :
                if cles_dict[syn_pass][0] == "2":
                     if arguments.get("comp_obl"):
                         id_prep = str(sentence_nodes[arguments.get("comp_obl")]["HEAD"])
                         if str(sentence_nodes[id_prep]["LEMMA"]) == "par":
                             arg_hum.append(arguments.get("comp_obl"))
                if cles_dict[syn_pass][1] == "2":
                     if arguments.get("subj"):
                        arg_hum.append(arguments.get("subj"))
    return arg_hum


def get_noun_obl(sentence_nodes, id_adp):
    for id_argument in sentence_nodes.keys():
        if str(sentence_nodes[id_argument]["HEAD"]) == id_adp:
            if str(sentence_nodes[id_argument]["UPOS"]) in ["NOUN", "PROPN"]:
                return id_argument


def get_argument_structure(sentence_nodes, id_verb):
    arguments = {}
    syn = 100
    
    arguments["passif"] = 0
    if sentence_nodes[id_verb]["FEATS"].get("Voice"):
        if str(sentence_nodes[id_verb]["FEATS"]["Voice"]) == "Pass":
            arguments["passif"] = 1
    if re.search("comp:aux", sentence_nodes[id_verb]["DEPREL"]) is not None:
        id_aux = str(sentence_nodes[id_verb]["HEAD"])
        if sentence_nodes[id_verb]["DEPREL"] == "comp:aux@pass":
            arguments["passif"] = 1
        for id_subj in sentence_nodes.keys():
            if str(sentence_nodes[id_subj]["HEAD"]) == id_aux:
                if sentence_nodes[id_subj]["DEPREL"] == "subj":
                    # syn += 100
                    arguments["subj"] = id_subj
                else :
                    for id_subj2 in sentence_nodes.keys():
                        if str(sentence_nodes[id_subj2]["HEAD"]) == id_subj:
                            if sentence_nodes[id_subj2]["DEPREL"] == "subj":
                                arguments["subj"] = id_subj2
    
    for id_argument in sentence_nodes.keys():
        if str(sentence_nodes[id_argument]["HEAD"]) == id_verb:
            # prep = "NULL"
            if sentence_nodes[id_argument]["DEPREL"] == "subj":
                # syn += 100
                arguments["subj"] = id_argument
            if sentence_nodes[id_argument]["DEPREL"] == "comp:obj":
                syn += 10
                arguments["comp_obj"] = id_argument
            if sentence_nodes[id_argument]["DEPREL"] in ["comp:obl", "comp:obl@agent"]:
                syn += 1
                if sentence_nodes[id_argument]["UPOS"] in [
                        "PRON", "NOUN", "PROPN"]:
                    arguments["comp_obl"] = id_argument
                else:
                    if sentence_nodes[id_argument]["UPOS"] == "ADP":
                        id_noun = get_noun_obl(sentence_nodes, id_argument)
                        arguments["comp_obl"] = id_noun
                        
            if len(str(syn))<3 :
                
                syn_s = "0"*(3-len(str(syn))) + str(syn)
            else:
                syn_s = str(syn)
                
            arguments["syn"] = str(syn_s)
    
    return arguments
        


def add_valence(sentence_nodes, dicoval):

    for id_token in sentence_nodes:
        if sentence_nodes[id_token]["UPOS"] == "VERB":
            lemma = sentence_nodes[id_token]["LEMMA"]
            cles_dict = dicoval.get(lemma)
            arguments = get_argument_structure(sentence_nodes, id_token
                    )
            if cles_dict:
                arg_hum=grab_arg_hum(cles_dict, arguments, sentence_nodes)
                for arg in arg_hum :
                    sentence_nodes[arg]["MISC"]["HUM_SCORE"] = int(sentence_nodes[arg]["MISC"].get("HUM_SCORE", 0))+4

    
    return sentence_nodes
