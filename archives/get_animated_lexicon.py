#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:56:43 2024

@author: pauline

Récupérer une liste de lexèmes nominaux considérés comme des êtres animés par
spiderlex
"""

from lxml import etree
import re
import pandas as pd
import pickle

file_path = '../../ressources/lexical-system-fr/9/ls-fr-V3/09-lssemlabel-model.xml'

tree = etree.parse(file_path)
root = tree.getroot()


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


# Trouver la balise avec l'attribut name="ÊTRE_ANIMÉ"
def find_element_with_name(root, name_value):
    for element in root.iter():
        if element.get('name') == name_value:
            return element
    return None



def find_element_with_name_part(root, recherche):
    instances = root.xpath(".//class/instance[contains(@name, 'individu')]") 
    individus = [instance.get('id') for instance in instances]
    
    return individus

def get_sub_elements(element, level=0):
    liste = []
    for sub_element in element:
        # normalised_id = sub_element.get("id").replace("cl", "")
        normalised_id = sub_element.get("id")

        liste.append(normalised_id)
        
        # Ensure the recursive call also returns a list
        sub_list = get_sub_elements(sub_element, level + 1)
        
        # Extend the main list with the returned sub-list
        liste.extend(sub_list)
        
    return liste


def get_nodes(df, classes):
    data = df[["node", "label", "%"]]

    nodes_animes = data.loc[df['label'].isin(classes), 'node']
    nodes = nodes_animes.tolist()
    
    return nodes


def get_entries(df, nodes):
    data = df[["id","entry", "lexnum", "status", "%", "update_date", "update_time", "lexname"]]

    entries_animes = data.loc[df['id'].isin(nodes), 'entry']
    entries = entries_animes.tolist() 
    
    return entries


def get_lemmas(df, entries):
    data = df[["id","addtoname", "name", "subscript", "superscript", "status", "%"]]

    lemmas_animes = data.loc[df['id'].isin(entries), 'name']
    lemmas = lemmas_animes.tolist() 
    
    return lemmas


def main():
    
    # création de l'arbre depuis fichier xml desd catégories sémantiques
    # extraire les id des classes sémantiques :
        # qui sont sous éléments de la classe "etre animé"
        # ou qui réfèrent à un "individu"
    
    file_path = '../../ressources/lexical-system-fr/9/ls-fr-V3/09-lssemlabel-model.xml'
    tree = etree.parse(file_path)
    root = tree.getroot()
    
    etre_anime_element = find_element_with_name(root, "ÊTRE_ANIMÉ")
    etre_metier = find_element_with_name_part(root, "individu")
    
    if etre_anime_element is not None:
        # print(f"Balise trouvée : {etre_anime_element.tag}")
        classes = list(set(get_sub_elements(etre_anime_element)+etre_metier))
        # print(classes)
    
        loader = FileLoader()
        file = loader.load("../../ressources/lexical-system-fr/9/ls-fr-V3/10-lssemlabel-rel.csv")
        nodes = get_nodes(file, classes)
        
        file = loader.load("../../ressources/lexical-system-fr/9/ls-fr-V3/01-lsnodes.csv")
        entries = get_entries(file, nodes)
        
        file = loader.load("../../ressources/lexical-system-fr/9/ls-fr-V3/02-lsentries.csv")
        lemmas = get_lemmas(file, entries)

        with open("../../ressources/liste_lex.pickle", 'wb') as file:
            pickle.dump(lemmas, file)
        
    else:
        print("Aucune balise avec name=\"ÊTRE_ANIMÉ\" trouvée.")
        

if __name__ == "__main__":
    main()