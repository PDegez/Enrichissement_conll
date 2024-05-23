#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 19:48:55 2024

@author: pauline
"""

import spacy
nlp = spacy.load('fr_core_news_lg')
nlp.add_pipe('coreferee')

# doc = nlp("Même si elle était très occupée par son travail, Julie en avait marre. Alors, elle et son mari décidèrent qu'ils avaient besoin de vacances. Ils allèrent en Espagne car ils adoraient le pays")

doc = nlp("Ils ne citent pas son nom, parce que depuis les institutions on n'attaque pas un membre de la famille royale, mais c'est à lui qu'ils s'en prennent.")

plop = doc._.coref_chains
# for nb_chaine in range(len(plop)) :
#     for id_element in range(len(plop[nb_chaine])):
#         print(f"chaine numéro {nb_chaine} : {plop[nb_chaine][id_element]}")

#print(plop, "\n", plop[0])
#plop.print()
# for chaine in iter(plop):
#     for token in iter(chaine):
#         for index in token :
#             print(index)
plop.print()
chaines = []
for chaine in iter(plop):
    essai = [index[0] if len(index) == 1 else index for index in iter(chaine)]
    print(essai)
