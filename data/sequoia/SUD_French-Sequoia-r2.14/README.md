# SUD_French-Sequoia

Since version 2.12 (May 2023), this treebank is maintained in [SUD](https://surfacesyntacticud.github.io/) in the [SUD_French-Sequoia](https://github.com/surfacesyntacticud/SUD_French-Sequoia) github repository.
It was converted from the [data](https://gitlab.inria.fr/sequoia/deep-sequoia) available in the [Deep-Sequoia](http://deep-sequoia.inria.fr), with the rewriting system [DSQtoSUD](https://gitlab.inria.fr/grew/dsqtosud).

A UD version is available in [UD released data](https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-5150) or on [UD_French-Sequoia](https://github.com/UniversalDependencies/UD_French-Sequoia).

## Origin
The first version of the Sequoia Corpus was presented in [(Candito & Seddah, 2012)](https://hal-univ-diderot.archives-ouvertes.fr/hal-00698938/).

## Data
The whole corpus contains 70,546 tokens in 3,099 sentences.

The original sentences of the corpus are taken from:

 - French Europarl
   - `Europar.550.conllu` (561 sentences, 15,732 tokens)
 - Wikipédia Fr
   - `frwiki_50.1000.conllu` (996 sentences, 23,127 tokens)
 - Newspaper *Est Républicain* 
    - `annodis.er.conllu` (524 sentences, 11,723 tokens)
 - European Medicines Agency
    - `emea-fr-dev.conllu` (574 sentences, 9,722 tokens)
    - `emea-fr-test.conllu` (444 sentences, 10,242 tokens)


In **UD_French-Sequoia**, data were randomly split into:

 * `fr_sequoia-ud-test.conllu`: 10,044 tokens in 456 sentences
 * `fr_sequoia-ud-dev.conllu`: 9,999 tokens in 412 sentences
 * `fr_sequoia-ud-train.conllu`: 50,503 tokens in 2,231 sentences


# Acknowledgments

The conversion has been performed by with the Graph Rewriting System [described here](https://gitlab.inria.fr/grew/DSQtoSUD) developed by Guy Perrier.

The Sequoia Corpus was presented in [(Candito & Seddah, 2012)](https://hal-univ-diderot.archives-ouvertes.fr/hal-00698938/) and revised later, notably during the project of deep annotation described in [(Candito & al. 2014)](http://hal.inria.fr/docs/00/97/15/74/PDF/deep_sequoia.final_with_keywords.pdf) and [(Perrier & al. 2014)](http://talc2.loria.fr/deep-sequoia/papers/syntaxe_profonde.pdf).

# References
**(Candito & Seddah, 2012)** Marie Candito, Djamé Seddah. [Le corpus Sequoia : annotation syntaxique et exploitation pour l'adaptation d'analyseur par pont lexical](https://hal-univ-diderot.archives-ouvertes.fr/hal-00698938/). TALN 2012 - 19e conférence sur le Traitement Automatique des Langues Naturelles, Jun 2012, Grenoble, France. 2012.

**(Candito & al. 2014)** Marie Candito, Guy Perrier, Bruno Guillaume, Corentin Ribeyre, Karën Fort, Djamé Seddah and Éric de la Clergerie. (2014) [Deep Syntax Annotation of the Sequoia French Treebank](http://hal.inria.fr/docs/00/97/15/74/PDF/deep_sequoia.final_with_keywords.pdf). *Proc. of LREC 2014*, Reykjavík, Iceland.

**(Perrier & al. 2014)** Guy Perrier, Marie Candito, Bruno Guillaume, Corentin Ribeyre, Karën Fort and Djamé Seddah. (2014) [Un schéma d'annotation en dépendances syntaxiques profondes pour le français](http://talc2.loria.fr/deep-sequoia/papers/syntaxe_profonde.pdf). *Proc. of TALN 2014*, Marseille, France.

**(Bonfante & al. 2018)** Guillaume Bonfante, Bruno Guillaume, Guy Perrier. [Application of Graph Rewriting to Natural Language Processing](https://hal.inria.fr/hal-01814386). ISTE Wiley, 1, pp.272, 2018, Logic, Linguistics and Computer Science Set.

# Changelog
* 2023-05-15 v2.12
  * The treebank is now maintained in SUD and converted to UD. See https://github.com/surfacesyntacticud/SUD_French-Sequoia

In the older releases, the process was different (conversion to UD first and from UD to SUD in a second time).
For changelog of earlier versions, see [UD Changelog](https://github.com/UniversalDependencies/UD_French-Sequoia/blob/master/README.md#changelog)
