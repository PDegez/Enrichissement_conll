#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 14:24:22 2024

@author: pauline
"""


import re, pandas, csv
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Verbe:
    verb : str
    val : list
    hum : list

@dataclass
class Argument:
    function : str
    sem : str

@dataclass 
class Frame:
    val : list
    config : list
    
@dataclass 
class Frame2:
    syn: str
    sem: str

# def frame_SUD(frame:list)->list:
#     frame_sud = []
#     for index, argument in enumerate(frame):
#         if argument == "P0":
#             frame_sud.append("subj")
#         if argument == "pseudo_se":
#             frame_sud.append(argument)
#         if argument in ["P1", "(P1)"]:
#             frame_sud.append("comp:obj")
#         if argument in ["P2", "(P2)"]:
#             frame_sud.append("comp:obl")
#         if re.search("PP", argument):
#             argument_raw = ''
#             index_dep = index
#             while not re.search(">", argument_raw):
#                 argument_raw += " " +frame[index_dep]
#                 index_dep+=1
            
#             prep = re.search("<(.*?)>", argument_raw).group(1)
#             frame_sud.append(f"mod:{prep}")
    
#     return frame_sud
        

def get_sud(frame:list):
    frame_sud =[]
    val = []
    for argument in frame:
        if argument == "pseudo_se":
            frame_sud.append(Argument("comp:se", frame[1].split(":")[-1]))
            val.append("comp:se")
        elif re.match("subj", argument):
            sem = argument.split(":")[-1].strip()
            frame_sud.append(Argument("subj", sem))
            val.append("subj")
        elif re.match("obj:", argument):
            sem = argument.split(":")[-1].strip()
            frame_sud.append(Argument("comp:obj", sem))
            val.append("comp:obj")
        elif re.search("objà", argument) or re.search("objde", argument):
            sem = argument.split(":")[-1].strip()
            frame_sud.append(Argument("comp:obl", sem))
            val.append("comp:obl")
        elif re.search("objp", argument):
            prep = re.search("<(.*?)>", argument).group(1)
            sem = argument.split(":")[-1].strip()
            frame_sud.append(Argument(f"mod:{prep}", sem))
            val.append("mod")
            
    frame_full = Frame(val, frame_sud)
    
    return frame_full

def get_sud_2(frame:list):
    syn = 0
    sem = 0
    prep = ""
    for argument in frame:
        # if argument == "pseudo_se":
        #     # récupérer le semantisme du sujet
        #     frame_sud.append(Argument("comp:se", frame[1].split(":")[-1]))
        #     val.append("comp:se")
        if re.search("subj", argument):
            syn+=1000
            if argument.split(":")[-1].strip() == "[hum]":
                sem+=2000
            else:
                sem+=1000
        elif re.match("obj:", argument):
            syn+=100
            if argument.split(":")[-1].strip() == "[hum]":
                sem+=200
            else:
                sem+=100
        elif re.search("objà", argument) or re.search("objde", argument):
            syn+=10
            if argument.split(":")[-1].strip() == "[hum]":
                sem+=20
            else:
                sem+=10
        elif re.search("objp", argument):
            prep = re.search("<(.*?)>", argument).group(1)
            syn+=1
            if argument.split(":")[-1].strip() == "[hum]":
                sem+=2
            else:
                sem+=1

    syn_s = str(syn)
    sem_s = str(sem)
    if len(syn_s)<4 :
        dif = 4-len(syn_s)
        syn_s = "0"*dif +syn_s
        sem_s = "0"*dif +sem_s
    
    if prep != "":
        frame_full = (syn_s, sem_s, prep)
    else:
        frame_full = (syn_s, sem_s)
    
    return frame_full
            

def compare_frame(origin, contender):
    retour = []
    for index, argument in enumerate(origin):
        if argument.sem =="[hum]":
            if contender[index].sem =='[hum]':
                retour.append("[hum]") 
            else :
                retour.append("[nhum]")
        else:
            retour.append("[nhum]")
                
    return retour


def main(): 
    with open("../../ressources/dicovalence/1/données/dicovalence_100625_utf8.txt", "r", encoding="utf-8") as file:
        raw_str = file.read()
        raw_list = raw_str.split("\n\n")[1:-1]
    
    # verbs = []
    # for element in raw_list[0:20]:
    #     humain = []
    #     raw_frame = re.search("FRAME.*?\n", element).group(0)
    #     if re.search("\[hum\]", raw_frame):
    #         frame = raw_frame.split("\t")[1].split(", ")
    #         verb = re.search("VERB.*?\n", element).group(0).split("\t")[1].split("/")[1].strip()
    #         val = re.search("VAL.*?\n", element).group(0).split("\t")[1].split(":")[1].split()
    #         print(verb)
    #         print(val)
    #         for argument in frame:
    #             function = argument.split(":")[0].strip()
    #             semantique = argument.split(":")[-1].strip()
    #             if semantique in ["[hum]", "[hum,?abs]"]:
    #                 humain.append(function)
    #         verbs.append(
    #             Verbe(
    #                 verb, val, humain))
    
    # print(verbs)
    
    # verbs = {}
    # for element in raw_list[0:20]:
    #     lemma = re.search("VERB.*?\n", element).group(0).split("\t")[1].split("/")[1].strip()
    #     raw_frame = re.search("FRAME.*?\n", element).group(0)
    #     val = re.search("VAL.*?\n", element).group(0).split("\t")[1].split(":")[1].split()
    #     val_sud = frame_SUD(val)
    #     if len(val_sud) != 0:
    #         print(lemma)
    #         print(val_sud)
            
    verbs = {}
    correctif = 0
    for element in raw_list:
        lemma = str(re.search("VERB.*?\n", element).group(0).split("\t")[1].split("/")[1].strip())
        raw_frame = re.search("FRAME.*?\n", element).group(0)
        frame = raw_frame.split("\t")[1].split(", ")
        if len(frame[-1])>1:
            frame_sud = get_sud(frame)
            cle = "_".join(sorted(frame_sud.val))
            # print(frame_sud)
            
            # si le verbe n'existe pas, je créé la clef lemma et j'ajoute sa 1ere config
            if verbs.get(lemma,0) == 0:    
                verbs[lemma] = {}
                verbs[lemma][cle]=frame_sud.config
            
            # le verbe existe
            else:
                # si la config existe, je la compare les frames et je prends le
                # plus safe
                if verbs[lemma].get(cle, 0) != 0:
                    correctif += 1
                    # print(verbs[lemma]["_".join(frame_sud.val)])
                    choix = compare_frame(
                        verbs[lemma]["_".join(sorted(frame_sud.val))],
                        frame_sud.config
                        )
                    config=[]
                    for index, element in enumerate(verbs[lemma][cle]):

                        config.append(Argument(element.function, choix[index]))
                        verbs[lemma]["_".join(sorted(frame_sud.val))]=config

                # si la config n'existe pas, je l'ajoute
                else: 
                    verbs[lemma][cle]=frame_sud.config
                    # print(verbs[lemma]["_".join(frame_sud.val)])


        # if not verbs.get(f"{lemma}"):
        #     verbs[lemma]= {}
        # verbs[lemma][frame_sud.val]=frame_sud.config
    
    long=0
    for verb in verbs.keys():
        long+=len(verbs[verb])
    # print(verbs)
    # print(long)
    # print(correctif)
    # print(verbs["abaisser"])
    # print(len(verbs["abaisser"]))
    return print("done")

if __name__ == "__main__":
    main()