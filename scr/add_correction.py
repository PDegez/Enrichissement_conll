#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 13:50:49 2024

Correction d'un fichier conllu annoté brut à l'aide d'un csv corrigé.
L'ouput est un fichier conllu dont les HUM_SCORE et le trait ANIMACY=HUM ont
été retiré des tokens faux positifs

@author: pauline
"""
import argparse
import pandas as pd
import conllup.conllup as cup




def grab_corrections(input_csv):
    """récupération de la liste des tuples (index phrase, index token) 
    pour les token indiqués comme faux positif ("n") dans le csv de 
    correction"""
    
    df = pd.read_csv(input_csv)
    rows = ["index_phrase", "index_token", "annotation"]
    df_adapte = df[rows]
    df_filtre = df_adapte[df_adapte['annotation'] == "n"]
    correction = list(df_filtre[['index_phrase', 'index_token']].itertuples(index=False, name=None))
    
    return correction
    


def main(input_conll, input_csv, output_conll = None ):
    """correction d'un fichier conllu annoté brut à l'aide d'un csv corrigé"""
    
    data = cup.readConlluFile(input_conll)
    correction = grab_corrections(input_csv)
    
    for couple in correction :
        del data[int(couple[0])]["treeJson"]["nodesJson"][str(couple[1])]["MISC"]["HUM_SCORE"]
        del data[int(couple[0])]["treeJson"]["nodesJson"][str(couple[1])]["MISC"]["ANIMACY"]
        
    sentences_json = [data[index_sentence] for index_sentence in range(len(data))]
    cup.writeConlluFile(output_conll, sentences_json, overwrite=True)
    print(f"fichier conll annoté créé à {output_conll}")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="humanity_score to a conll file")
    parser.add_argument(
        "input_file", type=str, help="Path to input file"
    )
    parser.add_argument(
        "input_csv",
        type=str,
        help="Path to input table file",
    )
    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        help="Path to output file",
    )

    args = parser.parse_args()

    main(args.input_file, args.input_csv, args.output_file)