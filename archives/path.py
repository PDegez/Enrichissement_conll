#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 19:02:00 2024

@author: pauline
"""

from pathlib import Path


plop = "../../essai.txt"
# Convertir le chemin d'entrée en objet Path
input_path = Path(plop).resolve()
    
# Récupérer le répertoire contenant le fichier d'entrée
input_dir = input_path.parent
    
# Définir le nouveau nom de fichier
new_file_name = f"{input_path.stem}_modifie.txt"
    
# Construire le chemin complet pour le nouveau fichier
new_file_path = input_dir / new_file_name
    
with open(new_file_path, "w", encoding="utf-8") as file:
    file.write("yoloooooo")
    
    
    