#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 17:10:49 2024
évaluation
@author: pauline
"""

import conllup.conllup as cup
import argparse, csv


def data_calcul_separe(dico:dict, cat:str)->dict:
    
    solo={}
    for element in dico:
        if str(element)[-1] in ["1", "3", "5", "7"]:
            solo["lex"] = solo.get("lex", 0) + int(dico[element])
        if str(element)[-1] in ["2", "3", "6", "7"]:
            solo["nent"] = solo.get("nent", 0) + int(dico[element])
        if str(element)[-1] in ["4", "6", "5", "7", "8"]: 
            solo["val"] = solo.get("val", 0) + int(dico[element])
        if len(element)>1:
            if str(element)[0] in ["1", "3", "5", "8"]:
                solo["coor_n"] = solo.get("coor_n", 0) + int(dico[element])
            elif str(element)[0] in ["2", "3", "6", "9"]:
                solo["coor_v"] = solo.get("coor_v", 0) + int(dico[element])
            elif str(element)[0] in ["4"]:
                solo["cop"] = solo.get("cop", 0) + int(dico[element])
            elif str(element)[0] in ["7", "8", "9"]:
                solo["rel"] = solo.get("rel", 0) + int(dico[element])
    
    return solo


def main(input_file:str, output_file:str=None, output_data:bool=False):
    
    safe = ["moi", "toi", "soi", "lui", "vous", "on"]
    vp = {}  
    fp = {}
    fp_data = []
    
    data = cup.readConlluFile(input_file)
     
    sentences_json = []
    for index_sentence in range(len(data)):
        sentence_nodes = data[index_sentence]["treeJson"]["nodesJson"]
        for token in sentence_nodes:
            if sentence_nodes[token]["MISC"].get("HUM_SCORE"):
                score = str(sentence_nodes[token]["MISC"]["HUM_SCORE"])
                if sentence_nodes[token]["LEMMA"] in safe:
                    vp[score] = vp.get(score, 0) + 1
                else:
                    candidat = str(sentence_nodes[token]["LEMMA"]).upper() + "\n"
                    forms = [ form for form in sentence_nodes.keys()]
                    start = " ".join([str(sentence_nodes[token]["FORM"]) for token in forms[0:int(token)-1]])
                    candidat_f = " " + str(sentence_nodes[token]["FORM"]).upper() + " "
                    end = " ".join([str(sentence_nodes[token]["FORM"]) for token in forms[int(token):-1]])
                    res = input(candidat + start + candidat_f + end +"\n")
                    if res != "f":
                        vp[score] = vp.get(score, 0) + 1
                    else:
                        fp[score] = fp.get(score, 0) + 1
                        total = start + candidat_f + end
                        fp_data.append(total)
                        del sentence_nodes[token]["MISC"]["HUM_SCORE"]
        data[index_sentence]["treeJson"]["nodesJson"] = sentence_nodes
        sentences_json.append(data[index_sentence])
    
    # composants mélangés
    # print(vp)
    sorted_vp = dict(sorted(vp.items()))
    sorted_fp = dict(sorted(fp.items()))
    
    # composants séparés
    solo_vp = data_calcul_separe(sorted_vp, "vp")
    solo_fp = data_calcul_separe(sorted_fp, "fp")
    
    if output_file:
        cup.writeConlluFile(output_file, sentences_json, overwrite=True)
    
    if output_data:
        name = input_file.split("/")[-1].split(".")[0]
        dossier_corpus = input_file.split("/")[-3]
        with open(
        f"../data/{dossier_corpus}/false_positives/{name}.txt", "w") as file:
            file.writelines(fp_data)
            
        with open(f"../stats/{dossier_corpus}/{name}_combined.csv", "w",
                  newline="", encoding="utf-8") as file_csv:
            writer = csv.writer(file_csv)
            writer.writerow(
                        [
                            "score",
                            "true_positive",
                            "false_positive"
                        ]
                        )
            for score in sorted_vp:
                row = [score, sorted_vp.get(score, 0), sorted_fp.get(score, 0)]
                writer.writerow(row)

        with open(f"../stats/{dossier_corpus}/{name}_separe.csv", "w",
                  newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                        [
                            "score",
                            "true_positive",
                            "false_positive"
                        ]
                    )
            for score in solo_vp:
                row = [score, solo_vp.get(score, 0), solo_fp.get(score, 0)]
                writer.writerow(row)

        

    
    print(f"vrai positifs par combinaison : {sorted_vp}")
    print(f"faux positifs par combinaison: {sorted_fp}")
    print(f"positifs par catégories uniques : {solo_vp}")
    print(f"negatif par catégories uniques : {solo_fp}")

            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="humanity_score to a conll file")
    parser.add_argument(
        "input_file", type=str, help="Path to input file"
        )
    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        help="Path to output file",
    )
    parser.add_argument(
        "-d",
        "--output_data",
        action= "store_true",
        help="generate a stat file, and a data file with the false positive",
        )
    args = parser.parse_args()
    
    main(args.input_file, args.output_file, args.output_data)
           