# ChessDataMining
Projet de fouille de données sur les parties de jeu d'échecs
Réalisé en Python 3.5
Nécessite Python-chess(module inclus), sklearn, numpy

Pour lancer le script principal, lancer main.py
Main.py comprend 3 fonctionnalités:
- parsing
- calculs avec Stockfish
- classification

Pour utiliser l'une ou l'autre des fonctionnalités, changer de fonction, par défaut, sur classify()

- build() : parsing
- main() : calculs
- classify() : classification

Pour lancer le script principal, il sera d'abord nécessaire d'appeler chacun des autres scripts, problème d'import non fixé pour l'heure


Modules
Parser : contient les scripts utilisés pour l'analyse des fichiers PGN
classify : contient les scripts nécessaires pour la classification aprés analyse

Bases de travail et résultats
Les fichiers PGN utilisés sont gardés dans le répertoire data/pgn
Les dictionnaires Python obtenus après parsing sont gardés dans le répertoire data/output
Les vecteurs obtenus après caculs sont gardés dans le répertoire data/vectors
Les résultats des classifications sont gardés dans le répertoire data/classification
L'arbre de décision généré est sauvegardé dans le répertoire data/tree
