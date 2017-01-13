# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 12:24:17 2016

@author: 21003607
"""
import chess
import chess.pgn # parsing du fichier pgn
import chess.uci # moteur de jeu

# donnes de jeu -- fichier pgn
pgn = open("data/pgn/test.pgn")


# moteur  Oracle
engine = chess.uci.popen_engine("stockfish/Linux/stockfish_8_x64")
engine.uci()

info_handler = chess.uci.InfoHandler()
engine.info_handlers.append(info_handler)


# fichier output

execute = True

while(execute):
    
    current = chess.pgn.read_game(pgn);
    
    # test pour arreter le parcours du fichier
    if (current == None):
        execute = False
        
    else :
    
        """
        Recuperation des joueurs
        """
        
        white = current.headers["White"]
        black = current.headers["Black"]
        print ("++ Game ++")
        print ("White : " + white)
        print ("Black : " + black)
        
        whiteElo = current.headers["WhiteElo"]
        blackElo = current.headers["BlackElo"]        
        
        # determination de la classe de chaque joueur
        if(whiteElo and blackElo != ''):
            if(int(whiteElo) > 2400):
                classWhite = 1
                
            else:
                classWhite = 0
                
            
            if(int(blackElo) > 2400):
                classBlack = 1
                
            else:
                classBlack = 0            
        
        # init des attributs de la partie            
        nbcoup = 0              # nombre de coup
        
        scoreW = 0              # score pour white
        scoreB = 0              # score pour black
        illegal_movesW = 0      # nombre de coups illegaux pour white
        illegal_movesB = 0      # nombre de coups illegaux pour black
        
        white_serie = 0         # plus longue serie de coups proches de l'Oracle pour white
        black_serie = 0         # plus longue serie de coups proches de l'Oracle pour black
        
        scoreGame = 0           # score cp pour la partie
        # init du board pour l'Oracle
        board = chess.Board();        
        
        """
        Parsing de la partie
        """
        
        moves = current.main_line()
        node = current
        
        while not node.is_end():
            
            """
            Recuperation du coup joue par les deux joueurs
            pour chaque coup la recuperation est faite en deux etapes
                le fichier pgn contient le node resultat du coup joue : pour le coup e2e4 le pgn contient e4
                il faut donc recuperer dans un premier temps le node
                puis demander au moteur le coup correspondant
            """
            # incrementation du nombre de coup -- a modifier
            nbcoup += nbcoup
            
            # node
            next_node = node.variation(0)
            print(node.board().san(next_node.move))
            
            # coup joue
            move = chess.Move.uci(next_node.move)
            print(move)
            
            # coups legaux du board courant
            legalmoves = board.legal_moves
            # test la legalite du coup -- support pour la classification
            if not(chess.Move.from_uci(move) in legalmoves):
                if(player == "W"):
                    illegal_movesW += 1
                else:
                    illegal_movesB += 1
            
            """
            Recuperation de l'estimation Oracle
            """
            # donner l'etat courant du board a l'Oracle
            engine.position(board)
            # recherche du meilleur coup a jouer selon l'Oracle
            oracle_move = engine.go(movetime = 2000)            
            print(oracle_move.bestmove)

            if(move == oracle_move.bestmove):
                print(1)
                if(player == "W"):
                    white_serie += 1
                else:
                    black_serie += 1
                
            
            # une fois toutes les operations executees
            # on ajoute le coup au board genere pour le moteur
            # on passe au node suivant
            board.push_san(node.board().san(next_node.move))
            
            engine.position(board)
            current_score = info_handler.info["score"][1].cp
            print(current_score)
            
            
            print("")
            break
        
            
        
            

    
            