# JOURNAL


## OBJECTIFS STAGE :

Création d'une pipeline pour ajouter 3 couches d'annotation supplémentaires dans un fichier conll :

- une couche de coréférence

- une couche sémantique double :

    - 1ere partie : projeter un lexique depuis eurowordnet ou WOLF

    - 2eme partie : vectoriser à partir de *fasttext* afin d'extraire les tokens sémantiquement similaires (répliquer Autolex). Dans l'idéal à la fin, pouvoir en tirer des catégorie sémantiques (lieu, temps etc)

- une couche morphologique (si assez de temps). Annotation depuis un lexique des eventuelles dérivations


## REMARQUES :

L'annotation des coréférences se fait majoritairement sur les NP (NP complets, Pronoms référentiels etc).

Travail sur GSD français. Ne pas hésiter à utiliser PUD pour les essai (mille phrases de chaque langue).

Scripts sous forme modulaire : un script main qui appelle les autres.

Travail avec Pytest.

Travail avec conllup.

<br>

### LOGS :

### 1 - 10 MAI :

<u> FAIT </u> :

- lecture des articles de Zeldes sur le corpus GUM.

- recherche sur le corpus GUM et sa couche d'annotation sémantique basée sur les entités :

    - information status : renvoie à *l'information packaging*. Indique entre autre si l'information est nouvelle ou ancienne.

    - Type d'entité : personne, lieu, organisation, objet, événement, temps, substance, animal, plante, notion abstraite.

    - Saillance (ou non) de l'entité

    - co-référence : anaphore, cataphore, apposition, coréférence prédicative, coréférence lexicale, discourse deixis.


The coreference scheme is loosely based on the design principles of the OntoNotes coreferece scheme (Weischedel et al. 2012) but with more unrestricted coreference criteria (as in ARRAU, Poesio & Artstein 2008), and with specific relation types, inspired by the TüBa-D/Z coreference scheme (Teljohann et al. 2012), which can be used to include or exclude certain phenomena in the data. A major design principle is that coreference should serve to identify the discourse referent referred to by underspecified expressions such as pronouns, and allow us to track the behavior of discourse referents as their expressions evolve over the course of a discourse, including all mentions of any kind (i.e. not excluding predication or compound modifiers if relevant).

There are two major types of coreference links: coreference proper, and bridging anaphora. Coreference contains six different subtypes of cases which are automatically derived from the 'coref' type, and bridging covers at least three types of cases:

<u>coreference :</u>

- ana - anaphoric, a pronoun referring back to something: [the woman] <-ana-- [she]. This is automatically generated from the 'coref' type when the anaphor is a pronoun.

- cata - cataphotic, a pronoun referring forward to something: [it]'s impossible [to know] ([it]--cata->[to know]). Automatically generated when the first member of a chain is a non-accessible pronoun.

- appos - apposition, same as in syntax: [Your neighbor],<-appos-- [the lawyer] came by earlier. Generated automatically

- pred - predicative coreference with an indefinite copula or xcomp predicate ([John] is [a teacher]), but not incuding identificational predication ([Elizabeth] is [the Queen of England]), which is seen as identity coreference

- disc - discourse deixis, reference to a non-nominal antecedent such as a sentence, VP or similar ([Kim arrived.] [This] was fortunate)

- lexical coref - all types of coreference, including lexical mention: [Obama] .... <-coref-- [President Obama] from coref using the syntax trees.

<u> bridge </u>

- bridging proper - some inferrable part-whole relationship, which requires no introduction for the anaphor thanks to the antecedent: [a car] <-bridge-- [the driver]

- non co-referential anaphora - cases in which the bridged anaphor is not part of the antecedent, but is underspecificed can only be interpreted thanks to mention of the antecedent: [a Chinese restaurant] <-bridge-- [an Italian one]

- split antecedent: [John] met [Mary] <-bridge-- [They] took a table together (in these cases the anaphor has multiple antecedents, but coreference only applies between the last mention and all previous mentions)

<u> A FAIRE </u> :

RDV avec Santiago pour lancer la partie technique.

_____________________________________________________________________________
### 10 MAI :
<u> FAIT <u> :

- RDV avec Santiago

- Set up d'un github pour le projet

- création d'un environnement virtuel pour le projet

- installation des bibliothèques python conllup, fasttext et Pytest.

<u> A FAIRE </u>

- Envoyer un mail à Loïc Grobol

- Prendre en main la bibliothèque conllup

- Prendre en main Pytest

