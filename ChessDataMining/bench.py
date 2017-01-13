# -*- coding: utf-8 -*-
"""
Created on Sun Dec 4 20:20:44 2016

@author: joh
"""

import chess.pgn

pgn = open("data/pgn/GiuocoPiano.pgn")

"""
Premiere etape : recuperation d'une game

"""

# tenter une structure en while(chess.pgn.read_game(pgn) != none)

first_game = chess.pgn.read_game(pgn)
second_game = chess.pgn.read_game(pgn)
# chaque appel de read_game recupere une nouvelle entree de jeu
# parcours, boucle, tableau, dico

pgn.close()

# Joueurs
black1 = first_game.headers["Black"]
white1 = first_game.headers["White"]

moves = first_game.main_line()
first_game.board().variation_san(moves)

# Recuperer la liste des moves.
node = first_game
while not node.is_end():
    next_node = node.variation(0)
    print(node.board().san(next_node.move))
    node = next_node
    
    
    
black2 = second_game.headers["Black"]
white2 = second_game.headers["White"]

print(black2)
print(white2)