# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:51:50 2017

@author: 21003607
"""

def build(file):
    pgn = open(file)
    
    execute = True
    
    base = {}    
    
    idgame = 0    
    
    while(execute):
        current = chess.pgn.read_game(pgn);
    
        # test pour arreter le parcours du fichier
        if (current == None):
            execute = False
            
        else :
            game = {}
            
            idgame += 1
            namegame = "game" + str(idgame)
                        
            # recuperation des joueurs
            white = current.headers["White"]
            black = current.headers["Black"]
                    
            # recuperation des ELO
            white_elo = current.headers["WhiteElo"]
            black_elo = current.headers["BlackElo"]
            
            # recuperation de l'ouverture            
            eco = current.headers["ECO"]
            
            # init du board pour l'Oracle
            board = chess.Board();
            
            # recuperation des coups joues
            listmoves = {}
            moves = current.main_line()
            node = current
            
            cpt = 0            


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

            while not node.is_end():
            
                """
                Recuperation du coup joue par les deux joueurs
                pour chaque coup la recuperation est faite en deux etapes
                    le fichier pgn contient le node resultat du coup joue : pour le coup e2e4 le pgn contient e4
                    il faut donc recuperer dans un premier temps le node
                    puis demander au moteur le coup correspondant
                """
                
                # incrementation du nombre de coups
                cpt += 1

                # node
                next_node = node.variation(0)
                pgn_move = node.board().san(next_node.move)
                # coup joue
                move = chess.Move.uci(next_node.move)
                #print(move)
                
                # une fois toutes les operations executees
                # on ajoute le coup au board genere pour le moteur
                # on passe au node suivant
                board.push_san(node.board().san(next_node.move))
                
                listmoves.update({str(cpt):move})
                
                node = next_node
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#            
    
            datas = {}
            datas.update({"white":white, "whiteElo":white_elo, "black":black, "blackElo":black_elo, "eco":eco, "moves": listmoves})
            
            game.update({namegame:datas})
            
        
        base.update(game)
    return base