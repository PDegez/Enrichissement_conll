#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 16:20:15 2024

@author: pauline
"""

import conllup.conllup as cup
import sys

#chemin = sys.argv[1]
chemin = "res_con.conllu"

data = cup.readConlluFile(chemin)

for sentence in data:
    for token_k, token_it in sentence["treeJson"]["nodesJson"].items():
        if token_it["MISC"]["NER"] != "None":
            print(token_it["FORM"], token_it["MISC"]["NER"])
