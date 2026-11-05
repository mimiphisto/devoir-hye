# Mini-analyste pandas : arménien classique (HYE)

L'objectif est d'analyser le corpus arménien classique HYE avec pandas et de répondre à des questions.Les scripts font le travail ; les agents les lancent et lisent leurs résumés.

## Règles
- Exécuter Python avec `uv run python scripts/...`. Jamais `pip`, `python`seul ni `python -c`. 
- Tous les résultats doivent être calculés à partir des fichiers présents dans data/.
- Tout chiffre vient de pandas : `evaluer.py`, ou une analyse lancée par `analyser.py`.
- Utiliser uniquement les fonctions pandas autorisées dans la skill pandas-tuto.
- Ne pas lire les données de test pour construire le dictionnaire.
- Ne jamais utiliser de boucle for pour parcourir les lignes d'un DataFrame.

## Rôle
- L'agent `analyste.toml` analyse les données avec pandas et répond aux questions présentes sur `RAPPORT.md`.

## Repères
- Données : `data/HYE_train.tsv`, `data/HYE_test_in-domain.tsv`, `data/HYE_test_out-of-domain.tsv`, colonnes `text_form form lemma pos`.
- Tagset : `data/HYE_tagset.txt` (étiquette, tabulation, définition).