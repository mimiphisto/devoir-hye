## Questions

`scripts/analyser.py` doit afficher, sous un titre `Q1` à `Q5`, la réponse aux questions suivantes :

1. Quelles sont les 5 catégories (`pos`) les plus fréquentes dans le train ?

Q1 : 5 categories (pos) les plus fréquentes dans le train
pos
V         1008
N+Com      786
I+Conj     745
I+Prep     310
A          295

2. Quelle proportion des mots du train sont des formes composées (`@` dans `pos`) ? Quelles sont les 5 combinaisons les plus fréquentes ?

Q2 : proportion de formes composees (@ dans pos) et top 5 des etiquettes composees
proportion : 0.142 soit 669 mots sur 4712
pos
N+Com@PRO+Dem           166
I+Prep@N+Com            164
I+Prep@N+Com@PRO+Dem     76
A@PRO+Dem                41
I+Prep@PRO+Dem           37

3. Combien de mots du train se terminent par l'article suffixé (`pos` qui finit par `@PRO+Dem`) ? Combien commencent par la préposition `զ` (`lemma` qui commence par `զ@`) ?

Q3 : article suffixe et preposition з
pos finissant par @PRO+Dem : 383
lemma commençant par «զ@» : 339

4. Quelles étiquettes du train **ne figurent pas** dans `HYE_tagset.txt`, et combien de fois chacune apparaît-elle ? Attention à deux pièges :
   - certains noms d'étiquettes du tagset se terminent par une espace ;
   - une étiquette composée est valide si chacune de ses parties l'est.

Q4 : etiquettes du train absentes du tagset (avec effectifs)
pos
PRO+Pos3    10
note : PRO+Pos3 et ∅ figurent dans le gold mais pas dans le tagset ; ils sont signales ci-dessus sans etre comptes contre le modele.

5. Refaites le **dictionnaire** de la partie 12 du notebook, avec le train arménien. Quel score obtient-il sur le test `in-domain`, puis sur le test `out-of-domain` ? Le score baisse-t-il autant qu'en grec (0,73 contre 0,51) ?

Q5 : dictionnaire form -> pos majoritaire (train uniquement) puis scores
pos la plus frequente du train (repli pour formes inconnues) : V
formes dans le dictionnaire : 2014
score in-domain : 0.6767
score out-of-domain : 0.6242
baisse : 0.0525 (grec : 0,73 -> 0,51, baisse de 0,22)


Qu'est-ce que l'agent apporte ici par rapport au notebook ? Qu'est-ce qu'il coûte ?

L'agent permet de poser des questions en langage naturel et génère automatiquement un script pandas pour effectuer les analyses alors que le notebook demande d'exécuter manuellement les cellules. Mais il coûte du temps de configuration et peut commettre des erreurs qu'il faut corriger. 

## Consigne donnée à l'agent

Lis les fichiers AGENTS.md, .vibe/agents/analyste.toml et les skills disponibles.

Utilise le sous-agent analyste pour répondre aux cinq questions du devoir sur le corpus HYE.

Tu dois écrire scripts/analyser.py, puis l'exécuter avec la commande autorisée.

Respecte toutes les contraintes du projet :
- Utiliser uniquement pandas et les fonctions autorisées par le skill.
- Ne pas parcourir les lignes avec une boucle for.
- Construire le dictionnaire uniquement à partir du train.
- Vérifier correctement les étiquettes composées pour Q4.
- Afficher les réponses sous les titres Q1, Q2, Q3, Q4 et Q5

Vérifie les calculs et corrige les erreurs éventuelles.

## Une erreur de l'agent

L'agent a commis deux erreurs dans la question 5 : il ne choisissait pas toujours l'étiquette la plus fréquente pour chaque forme en cas d'égalité, et il utilisait directement les étiquette du test. 
J'ai demandé à vibe de corriger sa méthode dans analyser.py

