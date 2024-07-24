#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 17:05:32 2024

@author: pauline
"""
import spacy, re

version = spacy.__version__

if re.match("3\.[12]\.?\d*", version):
    print("yolo")
else:
    print("bleh")