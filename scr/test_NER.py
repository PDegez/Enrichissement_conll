import spacy
from dataclasses import dataclass


@dataclass
class Ner:
    """classe contenant le texte et les annotations des entités nommées"""
    text: [str]
    label: str


text = "J'aime les Crusaders de Nouvelle-Zélande"

nlp = spacy.load("fr_core_news_lg")
doc = nlp(text)

# for token in doc:
#     print(token.idx, token.text)

NER = [Ner(nlp(ent.text), ent.label_) for ent in doc.ents]
#print(NER[0].text, NER[0].label)

essai = ["j'", "aime", "les", "Crusaders", "de", "Nouvelle-Zélande"]
for entite in NER:
    liste = list(entite.text)
    rectif=[]
    for i, tok in enumerate(liste) :
        if str(tok) == "-":
            rectif.append(i)
    
    if rectif :
        for index in rectif[::-1] :
            new_tok = str(entite.text[index-1]) + str(entite.text[index]) + str(entite.text[index+1])
            liste[index-1]= new_tok
            del liste[index+1]
            del liste[index]
                
    for id_mot, mot in enumerate(essai):
        if str(liste[0]) == mot:
            debut = id_mot
            fin = id_mot+len(liste)-1
            fin_slice = fin + 1
            
            if str(liste[-1]) == essai[fin]:
                 print(
                     f"span de {entite.label} = {id_mot}-{id_mot+len(entite.text)-1}")
                 print(f"slice : {essai[debut:fin_slice]}")
