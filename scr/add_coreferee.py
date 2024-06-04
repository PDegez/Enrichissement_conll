#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 16:39:27 2024

@author: pauline
"""

import spacy, argparse, re
from pathlib import Path
import conllup.conllup as cup
from spacy.tokens import Doc
from dataclasses import dataclass
from coreferee.data_model import Chain


@dataclass
class Chainloc:
    """the actual chain and the list of indexes of its components"""
    chain: Chain
    indexes: list


def add_coreferee(chains:list, analysis_conll:list, sentence_conll:dict)->dict:
    """ Add the coreferee to a conll sentence
    
    Parameters :
    ----------
    chains : list
        list of ChainLoc objects (local chain object) AKA the chains and the
        list of indexes
    analysis_conll : list
        list of token, extracted from the input conll file
    sentence_conll : dict
        sentence analysis in the conll format as a dictionnary
        
    Returns :
    ----------
    sentence_conll : dict
        conll sentence as a dictionnary with the added coreferee
    """
    
    chains_w_index = []
    for chain in chains :
        indexes_coreferee= [index[0] 
                         if len(index) == 1 
                         else sous_index for index in chain 
                         for sous_index in (
                                 index if len(index) > 1 else [index])]
        #indexes_coreferee = [index[0] for index in chain]
        chains_w_index.append(Chainloc(chain, indexes_coreferee))
      
    def sentence_w_coreferee(chains_w_index:list, sentence_conll:dict)->list:
        
        for chain in chains_w_index:
            for index in chain.indexes:
                sentence_conll[str(index+1)]["MISC"]["COREF"] = chain.chain.pretty_representation[3:]
                
        return sentence_conll
        
    return sentence_w_coreferee(chains_w_index, sentence_conll)


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


def main(
        input_file:str=None,
        output_file:str=None):
    
    version = spacy.__version__
    if not re.match("3\.[12]\.?\d*", version):
        return print(
            "This function requires the 3.1 or 3.2 version of spaCy")
    
    if not input_file:
        chemin = "../../conll/test1.conllu"
    else:
        chemin = input_file
    
    data = cup.readConlluFile(chemin)
    nlp = spacy.load("fr_core_news_lg")
    nlp.add_pipe('coreferee')
    sentences_json = []
    for index_sentence in range(len(data)) :
        
        # annotation conll :
        sentence_conll = data[index_sentence]["treeJson"]["nodesJson"]
        analysis_conll = [mot["FORM"] for mot in sentence_conll.values()]
    
        # annotation spacy :
        doc = custom_tokenizer(nlp, analysis_conll)
        for name, pipe in nlp.pipeline:
            analysis_spacy = pipe(doc)
                
        chains = [chain for chain in iter(analysis_spacy._.coref_chains)]
        if chains :
            data[index_sentence]["treeJson"]["nodesJson"] = add_coreferee(
                chains, analysis_conll, sentence_conll)
        
        sentences_json.append(data[index_sentence])

    # écriture conll entichi
    if not output_file:
        input_path = Path(input_file).resolve()
        input_dir = input_path.parent
        new_file_name = f"{input_path.stem}_enrichi.conll"
        output_file = input_dir / new_file_name

    cup.writeConlluFile(output_file, sentences_json, overwrite=True)
    
    return print("fichier conll crée")
    

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
    