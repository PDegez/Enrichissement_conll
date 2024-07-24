#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 16:08:41 2024

@author: pauline
"""
import conllup.conllup as cup
import sys

#chemin = sys.argv[1]
chemin = "../../conll/test1.conllu"

data = cup.readConlluFile(chemin)

print(data[976])
#print(data[6]['treeJson']["nodesJson"].keys())

mots = [ mot["LEMMA"] for mot in data[976]["treeJson"]["nodesJson"].values()]
print(mots)