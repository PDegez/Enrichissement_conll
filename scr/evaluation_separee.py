#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 19:26:27 2024

Creation d'un fichier csv pour récupérer les vrai positifs et faux positifs
annotés par chaque méthodes afin de comparer la précision de chaque méthode.
ATTENTION : un token pouvant être annoté par 4 méthodes différentes, la some
des annotations de ce fichier n'est pas le nombre de tokens annotés, mais le
nombre d'annotations.

@author: pauline
"""

import pandas as pd
from collections import Counter
import numpy as np
import csv, argparse


def main(input_file, output_file):
    faux = {}
    vrai = {}
    df = pd.read_csv(input_file)
    scores = df['score'].tolist()
    pos_glob = df['vrai_positif'].tolist()
    neg_glob = df['faux_positif'].tolist()
    
    for index_score in range(len(scores)) :
        if str(scores[index_score])[-1] in ["1", "3", "5", "7"]:
            vrai["lexique"] = vrai.get("lexique", 0) + pos_glob[index_score]
            faux["lexique"] = faux.get("lexique", 0) + neg_glob[index_score]
        
        if str(scores[index_score])[-1] in ["2", "3", "6", "7"]:
            vrai["nent"] = vrai.get("nent", 0) + pos_glob[index_score]
            faux["nent"] = faux.get("nent", 0) + neg_glob[index_score]
        
        if str(scores[index_score])[-1] in ["4", "5", "7"]:
            vrai["valence"] = vrai.get("valence", 0) + pos_glob[index_score]
            faux["valence"] = faux.get("valence", 0) + neg_glob[index_score]
        
        if len(str(scores[index_score])) == 2:
            if str(scores[index_score])[0] in ["1", "3", "5", "8"]:
                vrai["coor_nom"] = vrai.get("coor_nom", 0) + pos_glob[index_score]
                faux["coor_nom"] = faux.get("coor_nom", 0) + neg_glob[index_score]
        
            if str(scores[index_score])[0] in ["2", "3", "6", "9"]:
                vrai["coor_verb"] = vrai.get("coor_verb", 0) + pos_glob[index_score]
                faux["coor_verb"] = faux.get("coor_verb", 0) + neg_glob[index_score]
                
            if str(scores[index_score])[0] in ["4", "5", "6"]:
                vrai["comp_pred"] = vrai.get("comp_pred", 0) + pos_glob[index_score]
                faux["comp_pred"] = faux.get("comp_pred", 0) + neg_glob[index_score]
                
            if str(scores[index_score])[0] in ["7", "8", "9"]:
                vrai["antecedent"] = vrai.get("antecedent", 0) + pos_glob[index_score]
                faux["antecedent"] = faux.get("antecedent", 0) + neg_glob[index_score]
                
        if len(str(scores[index_score])) > 2:
                vrai["comp_pred"] = vrai.get("comp_pred", 0) + pos_glob[index_score]
                faux["comp_pred"] = faux.get("comp_pred", 0) + neg_glob[index_score]
                vrai["antecedent"] = vrai.get("antecedent", 0) + pos_glob[index_score]
                faux["antecedent"] = faux.get("antecedent", 0) + neg_glob[index_score]
    
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "score",
                "vrai_positif",
                "faux_positif",

            ]
                   )
        
        for key in ["lexique", "nent", "valence", "coor_nom", "comp_pred", "antecedent"]:
            row = [
                key,
                vrai.get(key, 0),
                faux.get(key, 0)
                ]
                        
            writer.writerow(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="humanity_score to a conll file")
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to input csv"
    )
    parser.add_argument(
        "output_file",
        type=str,
        help="Path to output csv file",
    )

    args = parser.parse_args()
    
    
    main(args.input_file, args.output_file)