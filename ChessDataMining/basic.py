# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 12:24:17 2016

@author: 21003607

Objectif : 
    - parser un fichier PGN pour extraire des informations sur des parties d'echec
    - construire une table de traits a partir de ces informations pour caracteriser des classes de joueurs
    - tester ces donnees sur un moteur d'apprentissage
    
"""
import chess
import chess.pgn # parsing du fichier pgn
import chess.uci # moteur de jeu

# donnes de jeu -- fichier pgn
pgn = open("data/pgn/large.pgn")

# fichier de sortie avec les tables
output = open("data/output/test2", "w")

# moteur  Oracle
engine = chess.uci.popen_engine("stockfish/Linux/stockfish_8_x64")
engine.uci()

info_handler = chess.uci.InfoHandler()
engine.info_handlers.append(info_handler)

# flag pour la duree de vie du traitement
execute = True

while(execute):
    
    current = chess.pgn.read_game(pgn);
    
    # test pour arreter le parcours du fichier
    if (current == None):
        execute = False
        
    else :
    
        """
        Recuperation des joueurs
        Initialisation des variables pour classifier la partie
        """
        
        white = current.headers["White"]
        black = current.headers["Black"]

        print ("++ Game ++")
        print ("White : " + white)
        print ("Black : " + black)

        whiteElo = current.headers["WhiteElo"]
        blackElo = current.headers["BlackElo"]        
        
        # determination de la classe de chaque joueur -- necessite que le ELO des joueurs soient indiques dans le PGN
        classWhite = "0"
        classBlack = "0"
        if(whiteElo and blackElo != ''):
            if(int(whiteElo) > 2400):
                classWhite = 1
                
            else:
                classWhite = 0
                
            if(int(blackElo) > 2400):
                classBlack = 1
                
            else:
                classBlack = 0 
        else:
            # statement pour passer automatiquement à la prochaine entree de partie si les ELO ne sont pas indiques
            continue
        
        #init des attributs de la partie     
        
        # nombre de coup
        nbcoup = 0
        nbW = 0
        nbB = 0              
        
        # score Oracle -- represente en moyenne pour la partie le ratio de coup Joueur proches des coups Oracle
        scoreW = 0              
        scoreB = 0
        
        # nombre de coups illegaux pour white
        illegal_movesW = 0      
        illegal_movesB = 0
        
        # plus longue serie de coups proches de l'Oracle
        white_serie = 0
        maxW = 0         
        black_serie = 0         
        maxB = 0
        # moyenne du score cp pour la partie
        scoreGame = 0           
        
        # coup servant d'ouverture pour la partie
        eco = current.headers["ECO"]
        
        # premiere piece superieure 
        firstW = ""
        firstB = ""
        
   
        """
        Parsing de la partie
        """
        # init du board pour l'Oracle
        board = chess.Board();        
        
        moves = current.main_line()
        node = current
        
        colors = ["W", "B"]
        i = 0
        
        while not node.is_end():
            
            """
            Recuperation du coup joue par les deux joueurs
            pour chaque coup la recuperation est faite en deux etapes
                le fichier pgn contient le node resultat du coup joue : pour le coup e2e4 le pgn contient e4
                il faut donc recuperer dans un premier temps le node
                puis demander au moteur le coup correspondant
            """
            # incrementation du nombre de coup -- a modifier
            nbcoup += 1
            player = colors[i]
            
            if(player == "W"):
                nbW += 1
            else:
                nbB += 1
    
            #print(nbcoup)
            # node
            next_node = node.variation(0)
            pgn_move = node.board().san(next_node.move)
            #print(node.board().san(next_node.move))
            
            # coup joue
            move = chess.Move.uci(next_node.move)
            # print(move)
            
            # recuperation de la premiere piece sup jouee
            pieces = 'KQRBN'
            for p in pgn_move :
                if(p in pieces):
                    if(player == "W" and firstW ==""):
                        firstW = p
                    elif(firstB == ""):
                        firstB = p
                        
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
            oracle_move = engine.go()   # movetime = 2000 -- init la recherche pour 2000 milliseconds -- non interessant pour l'ampleur du fichier -- 20K+ lignes
            best_move = oracle_move.bestmove
            if(str(move) == str(best_move)):
                # print("best")
                # si le coup joue correspond au coup oracle
                # on augmente de 1 le score Oracle du joueur
                # on augmente de 1 la serie de coup en accord avec l'Oracle
                if(player == "W"):
                    scoreW += 1
                    white_serie += 1
                else:
                    scoreB += 1
                    black_serie += 1
                # print("w" + str(white_serie))
                # print("b" + str(black_serie))
            else:
                # si le coup joue ne correspond pas
                # on fixe un max temporaire et on reset la serie
                if(player == "W"):
                    if(maxW < white_serie):
                        maxW = white_serie
                    white_serie = 0
                else:
                    if(maxB < black_serie):
                        maxB = black_serie
                    black_serie = 0
                
            
            # une fois toutes les operations executees
            # on ajoute le coup au board genere pour le moteur
            # on passe au node suivant
            board.push_san(node.board().san(next_node.move))
            
            engine.position(board)
            current_score = info_handler.info["score"][1].cp
            #print(current_score)
            
            #print("")
            i = (i+1)%2
            node = next_node
        
        
        """
        calcul des donnees
        """
        print(scoreW)
        print(white_serie)
        print(maxW)        
        scoreW =  float("{0:.2f}".format(scoreW / nbW))
        scoreB = float("{0:.2f}".format(scoreB / nbB))
        
        # traduction de l'icon de la premiere piece jouee en code
        codepW = 0
        codepB = 0
        
        if(firstW == 'K'):
            codepW = 0
        elif(firstW == 'Q'):
            codepW = 1
        elif(firstW == 'R'):
            codepW = 2
        elif(firstW == 'B'):
            codepW = 3
        elif(firstW == 'N'):
            codepW = 4
                
            
        if(firstB == 'K'):
            codepB = 0
        elif(firstB == 'Q'):
            codepB = 1
        elif(firstB == 'R'):
            codepB = 2
        elif(firstB == 'B'):
            codepB = 3
        elif(firstB == 'N'):
            codepB = 4
                
        """
        ecriture des resultats
        structure : Classe ; moyenneOracle ; pluslongueserie ; nombrecoups ; ouverture ; premierepiece ; 
        """
        lineW = str(classWhite) + ";" + str(scoreW) + ";" + str(max(white_serie, maxW)) + ";" + str(nbW) + ";" + str(eco) + ";" + str(codepW) + "\n"
        lineB = str(classBlack) + ";" + str(scoreB) + ";" + str(max(black_serie, maxB)) + ";" + str(nbB) + ";" + str(eco) + ";" + str(codepB) + "\n"
        
        output.write(lineW)
        output.write(lineB)
        
output.close()
engine.quit()
        
        
            

    
            