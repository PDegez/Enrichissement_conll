#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 18:34:01 2024

Creation d'un fichier csv pour récupérer les vrai positifs et faux positifs
de tous les différents HUM_SCORE à partir d'un csv de correction. Permet
de calculer le nombres de tokens vrais positifs/faux positifs du documents'

@author: pauline
"""

import glob, re
import pandas as pd
from collections import Counter
import numpy as np
import csv
import argparse

def main(input_directory, output_csv):
    path = input_directory + "*.csv"
    all_files = glob.glob(path)
    faux = {}
    vrai = {}
    for path in all_files:
        if re.search("_1.csv", path):
            print("yes")
            df = pd.read_csv(path)
            rows = ["score", "annotation"]
            df_adapte = df[rows]
            df_vrai = df_adapte[df_adapte['annotation'] == "y"]
            df_faux = df_adapte[df_adapte['annotation'] == "n"]
            
            token_vrai = dict(Counter(df_vrai['score'].to_list()))
            token_faux = dict(Counter(df_faux['score'].to_list()))
            
            for key in token_vrai:
                vrai[key] = int(vrai.get(key, 0)) + int(token_vrai[key])
            
            for key in token_faux:
                faux[key] = int(faux.get(key, 0)) + int(token_faux[key])

    values = [int(value) for value in vrai.values()]
    
    vrai_keys = list(vrai.keys())
    faux_keys = list(faux.keys())
    total_keys = set(vrai_keys + faux_keys)
    
    print(np.sum(values))
    print(vrai)
    
    with open(output_csv, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "score",
                "vrai_positif",
                "faux_positif",

            ]
                   )
        
        for key in total_keys:
            row = [
                key,
                vrai.get(key, 0),
                faux.get(key, 0)
                ]
                        
            writer.writerow(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluate the global precision of the main script")
    parser.add_argument(
        "input_directory",
        type=str,
        help="Path to input directory. Csv files must end with _1.csv"
    )
    parser.add_argument(
        "output_file",
        type=str,
        help="Path to output csv file",
    )

    args = parser.parse_args()
    main(args.input_directory, args.output_file)