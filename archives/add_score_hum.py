#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 14:18:16 2024

@author: pauline
"""
import argparse
from pathlib import Path
import conllup.conllup as cup
import pickle



def main(input_file, output_file=None):  
    
    with open("../../ressources/liste_lex_hum.pickle", 'rb') as file:
        lex = pickle.load(file)
    
    data = cup.readConlluFile(input_file)
    sentences_json = []
    for index_sentence in range(len(data)) :
        # annotation conll :
        sentence_nodes = data[index_sentence]["treeJson"]["nodesJson"]
        sentence_lemmas = [mot["LEMMA"] for mot in sentence_nodes.values()]
        for token in sentence_nodes:
            if sentence_nodes[token]["UPOS"] in ["NOUN", "PROPN", "PRON"]:
                sentence_nodes[token]["MISC"]["HUM_SCORE"] = 0
                if sentence_nodes[token]["MISC"].get("NENT"):
                    if sentence_nodes[token]["MISC"]["NENT"] == "PER":
                        sentence_nodes[token]["MISC"]["HUM_SCORE"] += 2
                if sentence_nodes[token]["LEMMA"] in lex:
                    sentence_nodes[token]["MISC"]["HUM_SCORE"] += 1
                #print(sentence_nodes[token]["MISC"], sentence_nodes[token]["LEMMA"], sentence_nodes[token]["UPOS"])
        sentences_json.append(data[index_sentence])

    # écriture conll entichi
    if not output_file:
        input_path = Path(input_file).resolve()
        input_dir = input_path.parent
        new_file_name = f"{input_path.stem}_scorehum.conll"
        output_file = input_dir / new_file_name

    cup.writeConlluFile(output_file, sentences_json, overwrite=True)
    
    return print(f"fichier conll crée au chemin {output_file}")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adding layers to a conll file")
    parser.add_argument(
        "input_file", type=str, help="Path to input file"
    )
    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        help="Path to output file",
    )

    args = parser.parse_args()
    main(args.input_file, args.output_file)
