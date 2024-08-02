#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 15:01:56 2024

full script : Add HUM_SCORE= and animacy=hum to human tokens

@author: pauline
"""

import spacy, argparse, pickle, csv
from lib_nent import add_nents, Nent
from lib_lex import add_lex
from lib_val import add_valence
from lib_projection import project_antecedent, project_nom_coor, project_val_coor, project_subj_comp
from pathlib import Path
import conllup.conllup as cup
from spacy.tokens import Doc


def custom_tokenizer(nlp, tokens_conll):
    """ impose conll parsing to spacy's pipeline"""
    spaces = [True] * (len(tokens_conll) - 1) + [False]
    return Doc(nlp.vocab, words=tokens_conll, spaces=spaces)


def clean_up(sentence_nodes):
    """clean up the data : remove unnecessary annotations"""
    
    
    for token in sentence_nodes:
        # remove HUM_SCORE if HUM_SC0RE == 0
        if str(sentence_nodes[token]["MISC"].get("HUM_SCORE")) == "0":
            del sentence_nodes[token]["MISC"]["HUM_SCORE"]
        
        # keep only the first annotation on named entitries
        if sentence_nodes[token]["MISC"].get("HUM_SCORE", 0):
            if str(sentence_nodes[token]["MISC"].get("NENT")) == "PER":
                if sentence_nodes[token]["DEPREL"] == "flat@name":
                    del sentence_nodes[token]["MISC"]["HUM_SCORE"]
        
        # remove HUM_SCORE on relative pronouns
        if sentence_nodes[token]["MISC"].get("HUM_SCORE", 0):
            if str(sentence_nodes[token]["FEATS"].get("PronType")) == "Rel":
                del sentence_nodes[token]["MISC"]["HUM_SCORE"]
                
        # remove annotations on named entities preceded by the lemma "monsieur"
        if sentence_nodes[token]["MISC"].get("HUM_SCORE", 0):
            head = str(sentence_nodes[token]["HEAD"])
            if head != "0":
                if str(sentence_nodes[head]["LEMMA"]) == "monsieur":
                    if sentence_nodes[head]["MISC"].get("HUM_SCORE"):
                        del sentence_nodes[token]["MISC"]["HUM_SCORE"]
                        
    # remove animacy=hum if no hum_score
    for token in sentence_nodes:
        if sentence_nodes[token]["MISC"].get("HUM_SCORE", 0):
            sentence_nodes[token]["MISC"]["ANIMACY"] = "HUM"
        if sentence_nodes[token]["MISC"].get("NENT", 0):
            del sentence_nodes[token]["MISC"]["NENT"]
                        
                    
    return sentence_nodes


def write_csv_evaluation(data:dict, output_table:str):
    with open(output_table, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "id_sentence_conll",
                "index_phrase",
                "index_token",
                "form",
                "lemma",
                "score",
                "annotation",
                "phrase"
            ]
                   )
        
        for index_sentence in range(len(data)):
            for index_token in data[index_sentence]["treeJson"]["nodesJson"]:
                score = data[index_sentence]["treeJson"]["nodesJson"][index_token]["MISC"].get("HUM_SCORE", 0)
                if score:
                    form = data[index_sentence]["treeJson"]["nodesJson"][index_token]["FORM"]
                    lemma = data[index_sentence]["treeJson"]["nodesJson"][index_token]["LEMMA"]
                    phrase = data[index_sentence]["metaJson"]["text"]
                    sent_id = data[index_sentence]["metaJson"]["sent_id"]
                    row = [
                        sent_id,
                        index_sentence,
                        index_token,
                        form,
                        lemma,
                        score,
                        "y",
                        phrase
                        ]
                        
                
                    writer.writerow(row)
    
    return print(f"fichier csv crée à {output_table}")
    

def main(
          input_file:str,
          output_file:str=None,
          output_table:str=None
          ):  
    
    # import data from conll file
    data = cup.readConlluFile(input_file)
    
    # import spacy French model
    nlp = spacy.load("fr_core_news_lg")
    
    # import data from spiderlex
    with open("../ressources/liste_lex_hum.pickle", 'rb') as file:
        lex = pickle.load(file)
    
    # import data from dicovalence
    with open("../ressources/dict_val.pickle", 'rb') as file:
        dicoval = pickle.load(file)
        
    sentences_json = []
    for index_sentence in range(len(data)) :
        
        # annotation conll :
        sentence_nodes = data[index_sentence]["treeJson"]["nodesJson"]
        analysis_conll = [mot["FORM"] for mot in sentence_nodes.values()]

        # annoter avec spacy :
        doc = custom_tokenizer(nlp, analysis_conll)
        for name, pipe in nlp.pipeline:
            analysis_spacy = pipe(doc)
                
        # ajout des entite nommées
        nents = [Nent(nlp(ent.text),
                        ent.label_) for ent in analysis_spacy.ents]
        if nents:
            sentence_nodes = add_nents(
            nents, analysis_conll, sentence_nodes)
        
        # ajout des annotations par lexique
        sentence_nodes = add_lex(sentence_nodes, lex)
        
        # ajout des annotation par valence
        sentence_nodes = add_valence(sentence_nodes, dicoval)
        
        # récupération des antécedents 1
        sentence_nodes = project_antecedent(sentence_nodes)
        
        # projection par coordination nominale
        sentence_nodes = project_nom_coor(sentence_nodes)
        
        # projection de coordination verbale
        sentence_nodes = project_val_coor(sentence_nodes, dicoval)
        
        # projection depuis l'attribut du sujet
        sentence_nodes = project_subj_comp(sentence_nodes)
        
        # récupération antécédent 2 (pour couvrir les nouveautés)
        sentence_nodes = project_antecedent(sentence_nodes)
        
        # nettoyage et suppression des annotations inutiles
        sentence_nodes = clean_up(sentence_nodes)
        
        data[index_sentence]["treeJson"]["nodesJson"] = sentence_nodes
        sentences_json.append(data[index_sentence])

    # écriture conll enrichi
    if not output_file:
        input_path = Path(input_file).resolve()
        input_dir = input_path.parent
        new_file_name = f"{input_path.stem}_enrichi.conll"
        output_file = input_dir / new_file_name

    cup.writeConlluFile(output_file, sentences_json, overwrite=True)
    print(f"fichier conll annoté créé à {output_file}")
    
    if output_table:
        write_csv_evaluation(data, output_table)
    

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
        "-t",
        "--output_table",
        type=str,
        help="Path to output table file",
    )

    args = parser.parse_args()

    main(args.input_file, args.output_file, args.output_table)