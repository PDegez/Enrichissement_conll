#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 18:33:29 2024

@author: pauline
"""

# from coreferee.data_model import Chain
from dataclasses import dataclass
from typing import Optional


@dataclass
class Nent:
    """classe contenant le texte et les annotations des entités nommées"""
    text: [str]
    label: str
    start: Optional[int] = None
    end: Optional[int] = None
    

# @dataclass
# class Chainloc:
#     """the actual chain and the list of indexes of its components"""
#     chain: Chain
#     indexes: list
    