#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 17:46:30 2024

@author: pauline
"""
import spacy, argparse#, re
from datastructure import Nent
from semantics import add_nents#, add_coreferee
from pathlib import Path
import conllup.conllup as cup
from spacy.tokens import Doc


def custom_tokenizer(nlp, tokens_conll):
    spaces = [True] * (len(tokens_conll) - 1) + [False]
    return Doc(nlp.vocab, words=tokens_conll, spaces=spaces)



# def main(
#         input_file:str=None,
#         output_file:str=None,
#         coreferee:bool=False,
#         semantics:str=False,
#         morphology:bool=False
#         ):
def main(
          input_file:str=None,
          output_file:str=None,
          semantics:str=False,
          ):  
    
    if not input_file:
        chemin = "../../conll/test1.conllu"
    else:
        chemin = input_file
    
    if not semantics:
    # if not coreferee and not semantics and not morphology:
#         return print("""Please pick the layer you wish to add:
#     -c to add coreferee
#     -s to add one or several semantic layer(s)
#     -m to add a morphological layer
                         
# for more information, try -h""")
        return print("""please pick the layer you wish to add :
    -s nent to add named entities
    -s wolf to add semantic information from wolf database
    -s lexf to add lexical fields to nouns""")
                         
                         
    data = cup.readConlluFile(chemin)
    nlp = spacy.load("fr_core_news_lg")
    sentences_json = []
    for index_sentence in range(len(data)) :
        
        # annotation conll :
        sentence_conll = data[index_sentence]["treeJson"]["nodesJson"]
        analysis_conll = [mot["FORM"] for mot in sentence_conll.values()]
    
        
        # if coreferee :
        #     version = spacy.__version__
        #     if not re.match("3\.[12]\.?\d*", version):
        #         return print(
        #             "This function requires the 3.1 or 3.2 version of spaCy")
        #     else :
        #         nlp.add_pipe('coreferee')
        #         doc = custom_tokenizer(nlp, analysis_conll)
        #         for name, pipe in nlp.pipeline:
        #             analysis_spacy = pipe(doc)
                
        #         chains = [chain for chain in iter(analysis_spacy._.coref_chains)]
        #         if chains :
        #             data[index_sentence]["treeJson"]["nodesJson"] = add_coreferee(
        #         chains, analysis_conll, sentence_conll)
        
        # else :
            # annoter avec spacy :
        doc = custom_tokenizer(nlp, analysis_conll)
        for name, pipe in nlp.pipeline:
            analysis_spacy = pipe(doc)
                
        if semantics:
            if semantics == "nent":
                nents = [Nent(
                        nlp(ent.text),
                        ent.label_) for ent in analysis_spacy.ents]
                if nents:
                        data[index_sentence]["treeJson"]["nodesJson"] = add_nents(
                        nents, analysis_conll, sentence_conll)
            elif semantics == "wolf":
                    pass
            elif semantics == "lexf":
                    pass
            else:
                    pass
                
            # if morphology:
            #     pass

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
    # parser.add_argument(
    #     "-c",
    #     "--coreferee",
    #     action="store_true",
    #     help="Add a coreferee layer to the conll file",
    # )
    parser.add_argument(
        "-s",
        "--semantics",
        choices=["nent","wolf","lexf", "all"],
        help="""Add a semantic layer to the conll file :\n
        'nents' : named entities\n
        'wolf' : semantic properties (import from wolf)\n
        lexf : lexical fields, based on vector distance\n
        'all' : all of the above""",
    )
    # parser.add_argument(
    #     "-m",
    #     "--morphology",
    #     action="store_true",
    #     help="Add a morphological layer to the conll file (import from)",
    # )
    args = parser.parse_args()

    # main(args.input_file, args.output_file, args.coreferee, args.semantics, args.morphology)
    main(args.input_file, args.output_file, args.semantics)
