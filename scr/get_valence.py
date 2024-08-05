#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 14:24:22 2024

Récupérer un dictionnaire de valence de verbe depuis dicovalence.
Exemple du format : {
    "aimer":
        {"100":"200"},
    "embrasser":
        {"110":"220"}
        }

Chaque verbe est la clé de son dictionnaire de configuration. 
Chaque configuration syntaxique est la clé de sa configuration sémantique.

Par exemple, "
100" est la configuration syntaxiqure d'un verbe qui ne prend qu'un sujet
"200" est la configuration sémantique d'un verbe dont le sujet est humain

@author: pauline
"""


import re, pickle


def get_val(frame:list):
    """renvoie la valence de la construction d'entrée sous la forme d'un tuple:
        
        syn = une string de 3 chiffres.
        sem = une string de 3 chiffres.
        prep = la préposition utilisée par le modifieur le cas échéant.
        
    Les chiffres renvoient respectivement au sujet, à l'objet direct et à l'objet
    oblique"""
    
    syn = 0
    sem = 0
    for argument in frame:

        if re.search("subj:", argument):
            syn+=100
            if argument.split(":")[-1].strip() == "[hum]":
                sem+=200
            else:
                sem+=100
        elif re.search(".?obj:", argument):
            syn+=10
            if argument.split(":")[-1].strip() == "[hum]":
                sem+=20
            else:
                sem+=10
        elif re.search("objà", argument) or re.search("objde", argument):
            syn+=1
            if argument.split(":")[-1].strip() == "[hum]":
                sem+=2
            else:
                sem+=1


    syn_s = str(syn)
    sem_s = str(sem)
    if len(syn_s)<3 :
        dif = 3-len(syn_s)
        syn_s = "0"*dif +syn_s
        sem_s = "0"*dif +sem_s
    
    frame_full = (syn_s, sem_s)
    
    return frame_full
            

def compare_frame(origin, contender):
    """Compare la partie sémantique de la valence pour différencier deux
    constructions syntaxiques similaires. Cette fonction renvoie la combinaison
    sémantique la plus sure, en privilégiant le non humain afin d'éviter les
    erreur de tag"""
    
    retour = ""
    for index in range(len(origin)):
        if origin[index] =="0":
            retour += "0"
        if origin[index] =='1':
            retour += "1"
        if origin[index] == "2":
            if contender[index] == "2":
                retour += "2"
            else:
                retour += "1"
                
    return retour


def main(): 
    with open("../../ressources/dicovalence/1/données/dicovalence_100625_utf8.txt",
              "r", encoding="utf-8") as file:
        raw_str = file.read()
        raw_list = raw_str.split("\n\n")[1:-1]
            
    verbs = {}
    correctif = 0
    # Extraction des informations depuis le fichier dicovalence
    for element in raw_list:
        
        lemma = str(re.search("VERB.*?\n",
                    element).group(0).split("\t")[1].split("/")[1].strip())
        raw_frame = re.search("FRAME.*?\n", element).group(0)
        frame = raw_frame.split("\t")[1].split(", ")
        
        # syn = subj-comp:obj-comp:obl-mod
        if len(frame[-1])>1:
            frame_sud = get_val(frame)
            cle = frame_sud[0]
            sem = frame_sud[1]


            # si le verbe n'existe pas, je créé la clef lemma et
            # j'ajoute sa 1ere config
            if verbs.get(lemma,0) == 0:    
                verbs[lemma] = {}
                verbs[lemma][cle] = sem
                
            # le verbe existe
            else:
                
                # si la config existe, je la compare les frames et je prends le
                # plus safe
                if verbs[lemma].get(cle, 0) != 0:
                    correctif += 1
                    # print(verbs[lemma]["_".join(frame_sud.val)])
                    choix = compare_frame(
                        verbs[lemma][cle],
                        sem
                        )
                    verbs[lemma][cle] = choix


                # si la config n'existe pas, je l'ajoute
                else: 
                    verbs[lemma][cle] = sem

        # enregistrement de la liste des lemmes animés au format pickle
    with open("../../ressources/dict_val.pickle", 'wb') as file:
        pickle.dump(verbs, file)
    
    long=0
    nb_vb = len(verbs.keys())
    for verb in verbs.keys():
        long+=len(verbs[verb].keys())
    #print(verbs)
    print(f"La liste comporte {nb_vb} verbes et {long} configurations")
    print(f"{correctif} correctifs ont été apportés pour lever les ambiguités")
    return print("fichier créé au chemin ../../ressources/dict_val.pickle")

if __name__ == "__main__":
    main()