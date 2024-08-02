<h1 style="text-align: center;">ANNOTATION DU CARACTERE HUMAIN DANS UN CONLLU DU FRANCAIS</h1>

<br>
## INTRODUCTION :

Ce projet a pour but l'annotation du caractère humain (anymacy=hum) d'un maximum de noms et de pronoms dans un fichier conllu du français au format SUD.


Le caractère humain a été défini comme ayant l'un des caractères suivant :

- le nom/pronom renvoie toujours à un humain (par exemple "un frère", ou les pronoms du discours "je" et "tu")

- Le nom/pronom peut être récupéré à partir de la question "qui ?". Cela nous a nottament permis de considérer comme humain des noms de groupe de personne, ou des métonymie courante comme "Matignon" dans une phrase comme "Matignon a exprimé son désaccord". En cela, nous avons annoté comme humain ce qui se comportait comme un humain ou un groupe d'humains.

- le nom est un nom propre humain

<br>

Le script d'annotation s'appuie sur 4 ressources ou axes d'annotation :

- la ressource lexicale [spiderlex](https://lexical-systems.atilf.fr/spiderlex/) qui nous a permis d'établir une liste de lexeme considérés comme sémantiquement humains

- l'outil de reconnaissance d'entité nommées de la bibliothèque python [spacy](https://spacy.io/) qui nous a permis d'annoter automatiquement les entités nommées annotées comme étant des "personnes" comme des humains.

- le dictionnaire de valences [dicovalence](https://www.ortolang.fr/market/lexicons/dicovalence) qui nous a permis d'annoter comme humain les noms communs ou pronoms lorsqu'ils occupent la place de l'argument typiquement humain d'un verbe. Par exemple, le verbe parler prend typiquement un sujet humain.

- des projections des annotations obtenues à partir des ressources précédentes en s'appuyant sur des propriétés syntaxiques. Par exemple, dans la phrase "Il est médecin.", le nom commun "médecin", attribut du sujet "il" par le biais de la copule "être" aurait été annoté comme humain à partir de la liste de lexemes humains extraites de spiderlex. Une extrapolation syntaxique nous permet d'annoter également le sujet "il" comme étant humain à partir du lien syntaxique qui existe entre lui et son attribut.

<br>
Lorsqu'un nom ou pronom est reconnu comme humain par l'un des mécanismes, il se voit attribuer un score lié à la méthode de reconnaissance. Ceci a pour but de pouvoir identifier clairement quelle(s) méthode(s) est à l'origine de l'annotation, et sers à l'évaluation du modèle ainsi qu'à indiquer un certain degré de confiance, certains scores indiquant une annotation plus fiable que d'autres.


Une fois les annotations faites, une phrase de relecture et correction a été nécessaire, nottament afin d'évaluer la précision du script. Il est à noter que seule la précision peut être évaluée : le script n'a pas vocation à être exhaustif, et tous les noms qui n'ont pas été annotées comme humain ne sont pas nécessairement non humain. Le script n'a simplement pas été capable de trancher.

<br>
La suite de ce README va suivre le plan suivant :

- organisation du dépot : rapide visite

- Retour sur ressources : explication de la façon dont elles ont été exploitées

- tableau des scores

- Phrase de relecture : illustation des guidelines suivies pour trancher lors de la correction

- Evaluation du modèle

- Point technique : bibliothèques nécessaires au fonctionnement du script, et présentation rapide des différents scripts utilisables
<br>

## ORGANISATION DU DEPOT : RAPIDE VISITE

Le dépot contient 3 sous-dossiers :

- le dossier data contient pour chaque corpus traité les fichiers conllu avant annotation, après annotation (annotation_brut), et après correction (annotation_clean), ainsi que les fichiers csv indiquant la performance du script.

- le dossier ressources contient les fichiers de spiderlex et dicovalence, ainsi que les listes des lexemes humains / des valences des verbes au format pickle extraites par les scripts pythons.

- le dossier scr contient les scripts pythons. On y trouve le script principal [add_human_layer](./scr/add_human_layer.py), ainsi que les bibliothèques de fonctions correspondants aux différentes approches utilisées : [lib_lex](./scr/lib_lex.py), [lib_nent](./scr/lib_nent.py), [lib_val](./scr/lib_val.py), et [lib_projection](./scr/lib_projection.py). On y trouve également les scripts qui ont été utilisés pour extraire la liste des lexemes humains [get_human_lexicon](./scr/get_human_lexicon.py) et la liste des différentes valences des verbes [get_valence](./scr/get_valence.py).

<br>
## RETOUR SUR LES RESSOURCES : EXPLICATION DE LA FACON DONT ELLES ONT ETE EXPLOITEES :

### SPIDERLEX

Spiderlex est une ressource lexicale mise au point par des lexicographes. Elle comporte nottament un système de classes sémantiques hierarchisées détaillé sous la forme d'un fichier xml. Chaque lexeme se voit attribuer une classe sémantique, et ces classes sémantiques fonctionnent selon un système d'inclusion : la catégorie "ETRE_HUMAIN" est ainsi incluse dans la catégorie "ETRE_ANIME", elle-même incluse dans la catégorie "ETRE_VIVANT" etc...

Afin d'obtenir une liste de noms "humains", nous avons récupérer grâce à un [script python](./scr/get_human_lexicon.py) l'ensemble des identifiants des catégories incluses dans la catégorie "être humain". Nous avons ajouté à cela toutes les catégories ayant dans leur balise xml de  description le mot "individu", afin de récupérer par exemple les noms de métiers dont la catégorie sémantique ne dépendait pas hierarchiquement de la balise "être-humain".

A partir des ces identifiants, nous avons récupéré tous les noms communs qui s'étaient vu attribuer une des classes sémantique correspondante, en choisissant de se limiter aux sens premiers. En effet, spiderlex répertorie les différents sens de chaque nom en se référant à un numéro (comme le ferait un dictionnaire). Nous avons choisi de n'extraire que les sens premiers afin d'écarter les extensions métaphoriques qui auraient été sources d'erreur.
Par exemple, dans un de ses sens, le nom commun "ordure" appartenait à une classe sémantique humaine (dans son sens d'insulte : "Quelle ordure celui là !"). Cependant, ce sens est moins courant que son sens premier (déchet), et aurait conduit à des erreurs lors de l'annotation. Il a donc été exclu.

La liste de mot a été enregistrée au format pickle et est disponible dans le dossier ressources sous le nom [liste_lex_hum](./ressources/liste_lex_hum.pickle).


<br>
### SPACY

Spacy est une bibliothèque python du NLP des plus classiques qui permet entre autre la reconnaissance des entités nommés. Dans notre cas, nous nous intéressons en priorité à l'annotation des des "personnes".

Afin d'éviter des conflits de parsing de phrase, nous avons imposé à spacy le parsing du fichier conllu. Chaque token reconnu comme une entité nommée se voyait attribuer un type d'entité nommée (PER, LOC, ORG, etc...). Les tokens annotés comme "PERS" se voyaient ensuite attribué l'annotation humain. Afin d'éviter qu'un nom propre composé de plusieurs token ne soit annoté plusieurs fois comme "humain", nous avons choisi ce faire en sorte que seul le premier soit annoté. Cela inclu autant que faire se peut les titres et les honorifiques. Par exemple, l'entité nommée "Monsieur Pierre Durand" ne sera annotée comme humain qu'une seule fois, sur le token "Monsieur".

<br>
### DICOVALENCE

Dicovalence est un dictionnaire de valence au format txt qui liste pour un ensemble de verbes les configurations argumentales qui lui sont connues.
Par exemple, le verbe "voler" aura entre autre les deux configurations suivantes :

- un seul argument (sujet) humain ou non humain : L'avion vole au dessus de la ville.
- un à trois argument(s) : sujet obligatoire et humain, objet direct optionnel non humain, objet indirect optionnel humain

L'idée est, pour chaque verbe du fichier conll, d'extraire sa configuration dans le texte en retrouvant ses arguments, et de comparer cette configuration avec celles proposées dans dicovalence afin d'identifier les arguments nécessairement humain. Le problème vient des cas d'ambiguité. Dans l'exemple proposé, le verbe voler lorsqu'il ne comporte d'un sujet peut correspondre à deux configurations différentes : dans la première le sujet n'est pas forcément humain, dans la seconde il l'est. Afin de limiter au maximum d'attribuer par erreur un attribut humain, lorsqu'un verbe avait deux configurations syntaxiquement identiques mais sémantiquement différentes, c'est la configuration qui n'imposait pas le trait humain qui a été retenue.

En raison de la complexité de la ressource, nous n'avons retenu que les arguments sujet/objet direct/objet indirect. Les autres éléments pris en compte par dicovalence (la préposition, les arguments locatifs etc... ) ont été pour l'instant laissé de coté.


Le script [get_valence](./scr/get_valence.py) a été utilisé pour extraire de dicovalence un dictionnaire de verbes ainsi que leurs configurations.

(NB : Les structures passives ont également été prises en compte dans le script général. Un verbe dont la valence indique un sujet humain verra au passif son complément d'agent annoté comme humain).

<br>
### PROJECTIONS D'ANNOTATIONS

Certaines annotations ont été extrapolées à partir des annotations déjà obtenue par les 3 méthodes précédentes. 4 règles de projections ont été ajoutées :

- projection à partir de la coordination de deux noms : lorsque deux noms sont coordonnées et que l'un est annoté comme humain, le deuxièmes se verra annoté comme humain également par projection. ex : "Ce n'est ni une terroriste, ni même une activiste de l'UCK !". "Activiste" a été reconnu comme humain parce que coordonné au nom "terroriste", déjà précédemment reconnu comme humain.

- projection à partir de la coordination de deux verbes : lorsque deux verbes sont coordonnées et partagent un argument (typiquement le sujet), si le permier verbe ne permet pas l'identification comme humain du sujet par sa valence mais que le second le peu, le sujet sera annoté comme humain.

- projection à partir de l'attribut du sujet : Lorsqu'un attribut du sujet est annoté comme humain, le sujet qu'il modifie sera lui aussi annoté comme humain. Ex : "l'Occident n'est pas seulement l'acteur, mais aussi le protagoniste des violations des droits de l'homme". "Occident" est reconnu comme humain car son attribut du sujet, "acteur", est annoté comme humain.

- projection à partir du pronom relatif : lorsqu'un pronom relatif est annoté comme humain, son antécédent sera annoté comme humain à sa place. Ex : "Je vous souhaite bonne chance ainsi qu'à toutes les autorités slovènes qui participent aux négociations." "autorités" est annoté comme humain, car il est l'antécédent d'un pronom relatif reconnu précédemment comme humain.

<br>
## TABLEAU DES SCORES

Chaque méthode d'annotation attribue un score (HUM_SCORE) au token qu'il a reconnu comme humain.
<br>

| SCORE | METHODE |
|---|---|
| 1 | annoté humain par le lexique (reconnu comme humain par spiderlex)|
| 2 | annoté humain par les entités nommées (reconnu comme une personne par Spacy)|
| 4 | annoté humain par valence (reconnu comme humain par dicovalence)|
| 10 | annoté comme humain par projection : coordination nominale |
| 20 | annoté comme humain par projection : coordination verbale |
| 40 | annoté comme humain par projection : attribut du sujet |
| 70 | annoté comme humain par projection : récupération d'antécédent|


Ce score est cumulatif : un token qui a été reconnu comme humain par deux méthodes différentes aura comme score la somme des deux scores correspondants. Par exemple, un token reconnu comme humain par valence et par entité nommée aura pour score 6 (4 +2).

<br>
## PHRASE DE RELECTURE : ILLUSTRATIONS DES GUIDELINES

Deux corpus entiers ont été annotés et corrigé : sequoia et rhapsodie. Le corpus GSD, très volumineux, n'a été que partiellement relu et corrigé.

De façon générale, deux règles ont primé :

- le token annoté renvoie-t-il clairement à un référent humain / est-il remplaçeable par un synonyme qui soit nécessairement humain ?

- le token annoté se comporte-t-il comme un humain : peut-il être la réponse à une question introduite par le pronom interrogatif "qui" et ses variations ("à qui", "de qui" etc...) ? Ex : "J'ai rencontré un étranger" (Qui ai-je rencontré ? = humain) vs "Je l'ai rencontré à l'étranger" (Où l'ai-je rencontré = non humain)


Afin de détailler les guidelines de correction suivie, nous allons procéder par catégories particulières rencontrés.

<br>
### catégorie 1 : polysémie et homonymie.

Certains lexemes ont pu être source d'erreur pour des raisons de polysémie et d'homonymie. L'arbitrage était alors en général assez simple, puisque le token annoté par erreur ne faisait pas référence à un humain ou à un groupe d'humain. Voici quelques exemples récurrents ont été repérés :

<br>

| lexeme ambigu | considéré comme humain | corrigé comme non humain |
| --- | --- | --- |
| politique | lorsqu'il fait référence à un homme ou une femme politique. "Les politiques : Roland Dumas, Édith Cresson, Jacques Chirac, Édouard Balladur, Juppé." | lorque le token faisait référence à une action/ une ligne politique. "L'affaire des diamants est une affaire politique révélée par Le Canard enchaîné [...]"|
| étranger | un étranger : fait référence à une personne étrangère | à l'étranger / de l'étranger : indique un location, une provenance...|
| garde | un soldat, un gardien : "un garde républicain"| garde à vue : expression idiomatique |
| cadre | un gradé, un chef : "les cadres du parti" | dans le cadre de : expression idiomatique |
| commission | groupe d'humain : "Je suis contraint de vous redemander d'intervenir, à vous et à la Commission,[...]"| une somme d'argent : "Il fut l'objet de plus de 500 millions de dollars de commissions [...]"|

<br>
### catégorie 2 : les noms de groupes
<br>

| catégorie | exemple ambigu | humain | non humain |
|---|  --- | --- | --- |
| groupe | assemblée | L'assemblée en tant que groupe d'humain : "[...] avant de la laisser "témoigner" devant leur assemblée." | l'assemblée en tant que réunion : "lors de l'assemblée"|
| les noms de pays | n'importe | Métonymie : le pays pour le gouvernement. "le Maroc pensait que les indépendantistes étaient tout au mieux un 5%, les militants"| "le 13 avril prochain débutera en Iran un procès à charge de treize citoyens [...]"|
| les entreprises | n'importe | agentivité humaine : "Thomson CSF a activé trois réseaux d'intermédiaires pour faire aboutir son dossier[...]" | "Ces trois réseaux apparaissent dans une série de notes internes de Thomson CSF" |
| les noms de villes | n'importe | quand elles font référence à une équipe de sport : " Metz a écrasé son rival" | "le traité de Paris"|


<br>
### catégorie 3 : les noms propres longs et les titres honorifiques

Il ne s'agit pas ici tant de vouloir corriger une erreur d'identification plus que d'éviter les annotations surnuméraires. Il existe deux cas de figure pour lesquel le script a tendance à annoter deux fois la même personnes comme humaine, faussant les résultats :

- Les titres et les honorifiques qui précèdent les noms propres identifiés par spacy sont souvent reconnu comme humain par spiderlex. Cela déclenche une double annotation pour une seule entité. Par exemple, Le Pape Pie X qui devrait n'être annoté que sur "Pape" a tendance à être annoté sur "Pape" et sur Pie (le premier composant du nom propre).

- Les noms propres à particules : "Dominique de Villepin" par exemple va souvent être annoté humain sur "Dominique" ET sur "Villepin" en raison du "de", pas toujours reconnu comme étant une partie du nom propre par spacy.

Dans un cas comme dans l'autre, la correction consiste à supprimer l'annotation en double et à ne conserver que la première.

<br>

### catégorie 4 : les personnifications

L'identification se basant sur le fait de se comporter comme un être humain (agentivité, volition, réponse à une question en "qui"), le script a nécessairement tendance à identifier les animaux (ou autre) personnifiés comme des humains. Il a été décidé de garder cette annotation humaine, nottament dans des exemples où le héro d'un conte, "Arthuro", porte un nom humain et se comporte (valence des verbes. Arthuro effectue des actions "humaines", comme le fait de parler) comme un humain syntaxiquement, bien qu'étant un corbeau.


## EVALUATION DU MODELE

Les tableaux reproduits et discutés ici sont retrouvables au format csv dans les dossiers respectifs des corpus.

<br>
### SEQUOIA

Le corpus sequoia a été annoté et corrigé en son entier.
<br>

<b> PRECISION GLOBALE POUR SEQUOIA </b>

| Token annotés | Vrai positifs | Faux positifs | précision |
| --- | --- | --- | --- |
| 4539 | 3704 | 835 | 0,82 (arrondi au centieme) |


Si l'on regarde de plus près les performances des différentes méthodes, on constate que la méthode basée sur le lexique est la plus performante avec 0.93 de précision. La moins précise est la méthode de récupération des antécédents par projection (0,56). Les autres tournent autour de 0,8, à l'exception de la reconnaissance des entités nommées, un peu en retrait à 0.73.

<b> PRECISION DES METHODES POUR SEQUOIA </b>

| Methode | Vrai positifs | Faux positifs | précision (arrondi au centieme)|
| --- | --- | --- | --- |
|lexique|2514|180|0,93|
|nent|868|329|0,73|
|valence|905|246|0,79|
|coor_nom|207|38|0,84|
|comp_pred|34|7|0,83|
|antecedent|53|42|0,56|


En ce penchant sur les données de plus près, on note cependant une différence importante de résultats entre les conllu qui contiennent du texte technique médical (notice de médical, les deux fichiers emea) et les autres fichiers.

En effet, les textes médicaux souffrent d'une mauvaise performance d'identification des entités nommées par Spacy, Spacy ayant tendance à annoter comme PERS (personne) tous les noms de médicaments et de molécules.

De plus, les notices de médicament ont tendance à utiliser le verbe de modalité "pouvoir" ("peuvent indiquer", "peuvent provoquer") en prenant pour sujet des molécules ou des constantes médicales. Or le verbe "pouvoir" est considéré comme ayant un sujet humain dans dicovalence, ce qui induit plus d'erreur que dans les autres types de texte.


Les méthodes de projections, qui s'appuient sur les 3 méthodes à ressources (lexique, entité nommée et valence), souffrent logiquement également de ces différences.
<br>

#### TEXTES MEDICAUX
<br>

<b> PRECISION GLOBALE POUR SEQUOIA MEDICAL </b>
| Token annotés | Vrai positifs | Faux positifs | précision |
| --- | --- | --- | --- |
| 894 | 537 | 357 | 0,6 (arrondi au centieme) |

<br>

<b> PRECISION DES METHODES POUR SEQUOIA MEDICAL </b>

| Methode | Vrai positifs | Faux positifs | précision (arrondi au centieme)|
| --- | --- | --- | --- |
|lexique|497|19|0,96|
|nent|38|234|0,14|
|valence|69|86|0,45|
|coor_nom|28|19|0,60|
|comp_pred|0|1|0|
|antecedent|5|8|0,38|


<br>
#### TEXTES NON MEDICAUX
<br>

<b> PRECISION GLOBALE POUR SEQUOIA NON MEDICAL</b>

| Token annotés | Vrai positifs | Faux positifs | précision |
| --- | --- | --- | --- |
| 3638 | 3161 | 477 | 0,87 (arrondi au centieme) |

<br>

<b> PRECISION DES METHODES POUR SEQUOIA NON MEDICAL </b>

| Methode | Vrai positifs | Faux positifs | précision (arrondi au centieme)|
| --- | --- | --- | --- |
|lexique|2010|161|0,93|
|nent|830|95|0,90|
|valence|852|199|0,81|
|coor_nom|179|19|0,90|
|comp_pred|35|5|0,88|
|antecedent|42|33|0,56|

<br>

Ces différences considérables indiquent que le script est sensible au type de texte annoté : les texstes médicaux se révelant être particulièrement difficiles à naviguer.
Malgré ces difficultés, le script obtient une précision de 0.82 sur l'ensemble des textes du corpus sequoia.

<br>
### RHAPSODIE

Le corpus rhapsodie a été annoté et corrigé en son entier.

<br>

<b> PRECISION GLOBALE POUR RHAPSODIE </b>

| Token annotés | Vrai positifs | Faux positifs | précision |
| --- | --- | --- | --- |
| 946 | 854 | 92 | 0,90 (arrondi au centieme) |

<br>

<b> PRECISION DES METHODES POUR RHAPSODIE </b>

| Methode | Vrai positifs | Faux positifs | précision (arrondi au centieme)|
| --- | --- | --- | --- |
|lexique|696|17|0,98|
|nent|85|35|0,71|
|valence|207|27|0,88|
|coor_nom|14|2|0,88|
|comp_pred|6|3|0,67|
|antecedent|13|9|0,59|

<br>

On constate que le script a plutôt de bonnes performances (0,90 de précision globale) sur le corpus rhapsodie. Rhapsodie étant un corpus de langue orale, il se prête assez bien à ce script :

- les pronoms du discours ("je", "tu" etc...) sont sureprésentés. Ceci explique le score de précision élevé de la méthode lexique (0.98)

- les phrases sont moins longues et moins complexes, ce qui favorise la précision de l'identification par coordination nominale.

- Les verbes employés le sont dans des constructions plus simples et prototypiques, ce qui a favorisé la précision par valence


Le corpus étant relativement "petit", il conviendrait de vérifier ces observations en applicant le script à un autre corpus de langue orale.

<br>
### GSD
<br>
Le corpus GSD étant massif, il n'a pas été corrigé dans son entier. Seul deux fichiers ont été complètement relus et corrigés.

<br>

<b>PRECISION GLOBALE POUR GSD </b>

| Token annotés | Vrai positifs | Faux positifs | précision |
| --- | --- | --- | --- |
| 2668 | 2266 | 402 | 0,85 (arrondi au centieme) |

<br>

<b> PRECISIONS DES DIFFERENTES APPROCHES POUR GSD </b>

| Methode | Vrai positifs | Faux positifs | précision (arrondi au centieme)|
| --- | --- | --- | --- |
|lexique|1216|112|0,92|
|nent|617|78|0,89|
|valence|604|187|0,76|
|coor_nom|154|31|0,83|
|comp_pred|86|6|0,93|
|antecedent|29|28|0,51|


Ces chiffres se rapprochent des résultats obtenus sur les textes non médicaux du corpus sequoia.

<br>

### CONCLUSION

<b> PRECISION GLOBALE </b>

| Token annotés | Vrai positifs | Faux positifs | précision |
| --- | --- | --- | --- |
| 8153 | 6824 | 1329 | 0,84 (arrondi au centieme) |

<br>

<b> PRECISION GLOBALE PAR METHODE </b>

| Methode | Vrai positifs | Faux positifs | précision (arrondi au centieme)|
| --- | --- | --- | --- |
|lexique|1216|112|0,92|
|nent|617|78|0,89|
|valence|604|187|0,76|
|coor_nom|154|31|0,83|
|comp_pred|86|6|0,93|
|antecedent|29|28|0,51|

<br>

La précision finale du script est de 0.84 sur l'ensemble des fichiers annotés et corrigés.

- la méthode d'identification par projection du caractère humain sur le sujet par sont attribut du sujet est la plus performante, avec une précision de 0.93. Cette méthode s'appuyant indirectement sur l'identification des noms communs, elle bénéfie des scores élevés de la méthode lexicale.

- La méthode d'identification par le lexique, via spiderlex, est la seconde plus performante avec une précision de 0.92. L'annotation des pronoms du discours, et la décision d'exclures les sens second des noms commun afin d'éviter les erreurs jouant une part non négligeable dans ce score.

- l'identification par entité nommée est la troisième (0.89). Son score serait cependant plus haut sans la présence de deux fichiers contenant du texte médical, qui s'est avéré être une grande difficilté pour l'identification d'entité nommées de Spacy. De même, une grande partie des "faux positifs" sont en réalité des redoublement d'annotation, qui ne sont pas techniquement faux.

- la méthode d'identification par projection par coordination nominale arrive en quatrième (0.83) Cette méthode s'appuyant indirectement sur l'identification des noms communs et des entités nommées, elle bénéfie des scores élevés de la méthode lexicale.

- la méthode d'identification par valence arrive en cinquième (0.76). Elle souffre sans doute d'une simplification trop grande de la ressource de base, et gagnerait à être retouchée afin de gagner en précision (et probablement en rappel).

- enfin, la méthode d'identification par récupération de l'antécédent (0.51) arrive en bonne dernière. Il s'agit probablement d'une conséquence du score d'identification par valence : les pronoms relatifs ayant été identifiés comme humains l'ayant majoritairement été par valence.




#### PISTES D'AMELIORATIONS :

- revenir sur dicovalence, en essayant d'intégrer la notion d'argument "optionnel", et les verbes à prépositions. Une meilleure performance de dicovalence devrait permettre également d'améliorer le score de récupération des antécédents.

- raffiner l'identification par entité nommée

    - en essayant de tenir compte de tous les titres et honorifiques afin d'éviter qu'une entité nommée comme "juge Armand Riberolles" ne soit à la fois annoté sur "juge" et "Armand". (le script prend pour l'instant seulement en compte le lexeme "Monsieur" afin d'annoter "Monsieur Armand Riberolles" sur "monsieur" uniquement)

    - en prenant en compte les noms à particules, souvent compris comme deux noms propres différents par spacy.

- vérifier l'intuition que le script est plus performant sur la langue orale que sur la langue écrite en annotant et corrigeant un second corpus oral et le confronter aux chiffres de rhapsodie.

- essayer d'identifier quels autres types de texte (autre que médicaux) représentent une difficulté pour le script

- rendre le script compatible avec UD. Le script est pour l'instant uniquement capable de prendre en charge les corpus au format SUD.


<br>
## POINT TECHNIQUE

### REQUIREMENTS :

Afin de fonctionner convenablement, ce script utilise les bibliothèques suivantes :

- [spacy](https://spacy.io/) pour l'annotation des entités nommées

- [conllup](https://pypi.org/project/conllup/) pour la prise en charge du format conllu

- pickle pour ouvrir les ressources extraites de spiderlex et dicovalence, enregistrées au format pickle.

<br>

### FONCTIONNEMENT GLOBAL, LANCER LES SCRIPTS


Tous les scripts se trouvent dans le dossier scr du dépot.

<br>
#### Le script principal est le script add_human_layer.py :

ATTENTION : ce script s'appuie sur des données conservées dans le dossier ressources du dépot. Il ne fonctionnera donc que si vous conservez la même arborescence en local.

usage: add_human_layer.py [-o OUTPUT_FILE] [-t OUTPUT_TABLE] input_file

- le script prend en argument un fichier input au format SUD conllu.

- le fichier output (optionnel) est un fichier conllu annoté brut, où les scores SCORE_HUM et l'annotation ANIMACY=HUM ont été rajoutés pour les tokens identifiés comme humains

- le fichier table (optionnel) est un csv destiné à relire et corriger les annotations


Ce script s'appuie sur 4 bibliothèques de fonctions locales, correspondant aux différentes méthodes d'annotations :

- lib_nent pour la fonction d'annotation par entité nommée

- lib_lex pour les fonctions d'annotation par lexique

- lib_val pour les fonctions d'annotation par valence

- lib_projection pour les fonctions d'annotation par projection

<br>
#### Si une relecture a été faite via le fichier csv, le script de correction du conllu annoté brut est add_correction.py


ATTENTION : ce script ne marchera que si les tokens dont l'annotation est fausse ont reçu la valeur "n" dans le csv dans la colonne "annotation". Toute autre valeurs que "y" ou "n" dans cette colonne sera ignorée par le script.


usage: add_correction.py [-o OUTPUT_FILE] input_file input_csv

- le script prend en argument 1 le fichier conll annoté brut et en argument 2 le csv de correction.

- le fichier output (optionnel) est le conllu corrigé, conservant SCORE_HUM et ANIMACY=HUM pour les tokens correctements annotés.

<br>
#### Si vous souhaitez une évaluation à partir des fichiers csv corrigés, utiliser evaluation_glob.py :


ATTENTION : ce script ne marchera que si les tokens dont l'annotation est fausse ont reçu la valeur "n" dans le csv dans la colonne "annotation". Toute autre valeurs que "y" ou "n" dans cette colonne sera ignorée par le script.


usage: evaluation_glob.py input_directory output_file

- le script prend en argument 1 le dossier dans lequel les csv corrigés sont enregistrés. Ces csv DOIVENT se terminer par "_1.csv" pour être pris en compte.

- le script prend en argument 2 le chemin du csv de sortie


#### Si vous souhaitez évaluer les performances de chaque méthodes à partir de vos csv corrigés : évaluation_separee.py :

ATTENTION : ce script ne marchera que si les tokens dont l'annotation est fausse ont reçu la valeur "n" dans le csv dans la colonne "annotation". Toute autre valeurs que "y" ou "n" dans cette colonne sera ignorée par le script.


usage: evaluation_separee.py input_file output_file

- le script prend en argument 1 le fichier csv input (celui obtenu par le script précédent)

- le script prend en argument 2 le fichier csv output


#### LES SCRIPTS ANNEXES :

<b> get_human_lexicon.py </b>  script ayant servi à extraire de spiderlex une liste de lexemes humains. La liste est conservée au format pickle dans le dossier ressources

<b> get_valence.py </b> script ayant servi à extraire de dicovalence un dictionnaire de verbe et de leur valence. Le dictionnaire est conservé au format pickle dans le dossier ressources









