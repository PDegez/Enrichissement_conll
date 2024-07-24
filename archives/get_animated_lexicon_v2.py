#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 14:45:13 2024

@author: pauline

Récupérer une liste de lexèmes nominaux considérés comme des êtres animés par
spiderlex
v2
"""

from lxml import etree
import re
import pandas as pd
import pickle


class FileLoader:
    def load(self, path):
        df = pd.read_csv(path,delimiter="\t")
        rows, columns = df.shape
        print(f"Loading dataset of dimensions {rows} x {columns}")
        return df

    def display(self, df, n=None):
        if n is not None:
            if n >= 0:
                print(df.head(n))
            else:
                print(df.tail(-n))
        else:
            print(df)


def find_element_with_name(root, name_value):
    """trouver la balise "ETRE_ANIME"""
    
    for element in root.iter():
        if element.get('name') == name_value:
            return element
    return None


def find_element_with_name_part(root, recherche):
    """trouver les balises dont la description inclu le terme "individu"""
    instances = root.xpath(".//class/instance[contains(@name, 'individu')]") 
    individus = [instance.get('id') for instance in instances]
    
    return individus


def get_sub_elements(element, level=0):
    """extraire les identifiants des classes dépendantes des éléments 
    indiqués"""
    liste = []
    for sub_element in element:
        normalised_id = sub_element.get("id")
        liste.append(normalised_id)
        
        # Appel récursif pour s'enfoncer dans les niveaux
        sub_list = get_sub_elements(sub_element, level + 1)
        
        # Ajouter les nouvelles classes à la liste
        liste.extend(sub_list)
        
    return liste


def get_nodes(df, classes):
    """extraire les identifiants des nodes dont la classe sémantique appartient
    aux classes animées précedemment extraites"""
    data = df[["node", "label", "%"]]

    nodes_animes = data.loc[df['label'].isin(classes), 'node']
    nodes = nodes_animes.tolist()
    
    return nodes


def get_lemmas(df, nodes):
    """extraire les lemmes dont les nodes appartiennent à une classe 
    sémantique animée, et dont le sens est premier est animé (pour écarter les 
    noms qui ne réfèrent que rarement à des animés)"""
    
    lexnum_cond = [
        "I", "I.1", "1", "I.a", "1.a", "a", "", " ", "I.1.a", "1a", "I.1a"
        ]
    data = df[["id","entry", "lexnum", "status",
               "%", "update_date", "update_time", "lexname"]]
    
    filtered_data = data[data['id'].isin(nodes) & 
                         (data['lexnum'].isin(lexnum_cond) | 
                          data['lexnum'].isna())]
    lemmas_sales = filtered_data['lexname'].tolist()
    lemmas = [re.search("namingform\'>(.+?)<", plop).group(1).lower() 
              for plop in lemmas_sales]

    return lemmas


def main(): 
    # création de l'arbre, récupération de la racine    
    file_path = '../../ressources/lexical-system-fr/9/ls-fr-V3/09-lssemlabel-model.xml'
    tree = etree.parse(file_path)
    root = tree.getroot()
    
    # récupération de la balise "ETRE_ANIME" et des balises qui réfèrent à un
    # "individu"
    etre_anime_element = find_element_with_name(root, "ÊTRE_ANIMÉ")
    etre_metier = find_element_with_name_part(root, "individu")
    
    # récupération des classes sémantiques animées
    classes = list(set(get_sub_elements(etre_anime_element)+etre_metier))
    # print(classes)
    
    # récupération des nodes dont les labels sémantiques sont animés
    loader = FileLoader()
    file = loader.load(
        "../../ressources/lexical-system-fr/9/ls-fr-V3/10-lssemlabel-rel.csv"
        )
    nodes = get_nodes(file, classes)
        
    # récupération des lemmes dont les nodes ont des labels sémantiques animés
    file = loader.load(
        "../../ressources/lexical-system-fr/9/ls-fr-V3/01-lsnodes.csv")
    lemmas = get_lemmas(file, nodes)
    # print(lemmas)
    # print(len(lemmas))
        
    # with open(
    # "../../ressources/liste_lex_v2_explo.txt", "w", encoding="utf-8"
    # ) as plop:
    #     plop.writelines(lemmas)
    
    # enregistrement de la liste des lemmes animés au format pickle
    with open("../../ressources/liste_lex_v2.pickle", 'wb') as file:
        pickle.dump(lemmas, file)
        

if __name__ == "__main__":
    main()