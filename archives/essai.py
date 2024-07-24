#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 15:44:18 2024

@author: pauline
"""

import argparse, pickle, re
from pathlib import Path
import conllup.conllup as cup


def grab_subj_coor_verb(sentence_nodes, id_token, dicoval):
    args = [sentence_nodes[x]["DEPREL"] for x in sentence_nodes if str(sentence_nodes[x]["HEAD"])==id_token]
    if "subj" in args :
        # print("V2 a déjà un sujet")
        return 0
    else :
        lemma_v = str(sentence_nodes[id_token]["LEMMA"])
        if dicoval.get(lemma_v, 0):
            if all(s.startswith("2") for s in dicoval[lemma_v].values()):
                id_head = str(sentence_nodes[id_token]["HEAD"])
                id_subj = 0
                if re.search("comp:aux", str(sentence_nodes[id_head]["DEPREL"])):
                    id_head = str(sentence_nodes[id_head]["HEAD"])
                        
                for id_arg in sentence_nodes:
                    if str(sentence_nodes[id_arg]["HEAD"]) == id_head:
                        if str(sentence_nodes[id_arg]["DEPREL"]) == "subj":
                            id_subj = id_arg
                            print(sentence_nodes[id_subj]["LEMMA"])
                        else:
                            return 0
                if id_subj:
                    return id_subj
            else :
                return 0
        else :
            return 0


def grab_antecedent(sentence_nodes,id_token):
    id_verb_rel = str(sentence_nodes[id_token]["HEAD"])
    id_antecedent = str(sentence_nodes[id_verb_rel]["HEAD"])
    if sentence_nodes[id_antecedent]["UPOS"] in ["NOUN", "PROPN", "PRON"]:
        return id_antecedent
    else:
        return 0


def main(input_file, output_file=None):
    with open("../../ressources/dict_val.pickle", 'rb') as file:
        dicoval = pickle.load(file)
        
    data = cup.readConlluFile(input_file)
    sentences_json = []
    for index_sentence in range(len(data)) :

        # annotation conll :
        sentence_nodes = data[index_sentence]["treeJson"]["nodesJson"]
        for id_token in sentence_nodes:
            
            # récupération des antécédents
            if sentence_nodes[id_token]["FEATS"].get("PronType") == "Rel":
                if int(sentence_nodes[id_token]["MISC"].get("HUM_SCORE", 0)):
                    id_antecedent = grab_antecedent(sentence_nodes,id_token)
                    if id_antecedent:
                        sentence_nodes[id_antecedent]["MISC"]["HUM_SCORE"] = int(sentence_nodes[id_antecedent]["MISC"].get("HUM_SCORE", 0))+ 8
                        data[index_sentence]["treeJson"]["nodesJson"][id_antecedent]["MISC"]["HUM_SCORE"] = int(data[index_sentence]["treeJson"]["nodesJson"][id_antecedent]["MISC"].get("HUM_SCORE", 0))+ 8
    
    for index_sentence in range(len(data)):
        sentence_nodes = data[index_sentence]["treeJson"]["nodesJson"]
        for id_token in sentence_nodes:
            # projection à partir des coordinations
            if str(sentence_nodes[id_token]["DEPREL"]) == "conj:coord":
                
                # Noms coordonnés avec un nom annoté humain
                if sentence_nodes[id_token]["UPOS"] in ["NOUN", "PROPN", "PRON"]:
                    id_head = str(sentence_nodes[id_token]["HEAD"])
                    if int(sentence_nodes[id_head]["MISC"].get("HUM_SCORE", 0)):
                        sentence_nodes[id_token]["MISC"]["HUM_SCORE"] = int(sentence_nodes[id_token]["MISC"].get("HUM_SCORE", 0))+ 8
                        data[index_sentence]["treeJson"]["nodesJson"][id_token]["MISC"]["HUM_SCORE"] = int(data[index_sentence]["treeJson"]["nodesJson"][id_token]["MISC"].get("HUM_SCORE", 0))+ 8

                # projection de la valence du second verbe coordonné si le sujet est nécessairement humain
                if sentence_nodes[id_token]["UPOS"] == "VERB":
                    id_subj = grab_subj_coor_verb(sentence_nodes, id_token, dicoval)
                    if id_subj:
                        sentence_nodes[id_subj]["MISC"]["HUM_SCORE"] = int(sentence_nodes[id_subj]["MISC"].get("HUM_SCORE", 0))+ 8
                        data[index_sentence]["treeJson"]["nodesJson"][id_subj]["MISC"]["HUM_SCORE"] = int(data[index_sentence]["treeJson"]["nodesJson"][id_subj]["MISC"].get("HUM_SCORE", 0))+ 8
        
    sentences_json.append(data[index_sentence])
                

    # écriture conll enrichi
    if not output_file:
        input_path = Path(input_file).resolve()
        input_dir = input_path.parent
        new_file_name = f"{input_path.stem}_score_hum.conll"
        output_file = input_dir / new_file_name

    cup.writeConlluFile(output_file, sentences_json, overwrite=True)
    
if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Adding layers to a conll file")
    # parser.add_argument(
    #     "input_file", type=str, help="Path to input file"
    # )
    # parser.add_argument(
    #     "-o",
    #     "--output_file",
    #     type=str,
    #     help="Path to output file",
    # )

    # args = parser.parse_args()
    # main(args.input_file, args.output_file)
    main("../../conll/rhaps1_hum.conll")