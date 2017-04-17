# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:51:50 2017

@author: 21003607
"""
import pickle

class ReadPGN:
    
    def __init__(self):
        self.description = "module de parsing du fichier PGN"
        
    def build(self, file):
        pgn = open(file)
        base = open("data/output/baseplayer.txt", 'rb')
        
        playerbase = pickle.load(base)
        
        execute = True
        
        base = {}    
        
        idgame = 0    
        
        while(execute):
            try:
                    
                current = chess.pgn.read_game(pgn);
            
                # test pour arreter le parcours du fichier
                if (current == None):
                    execute = False
                    
                else :
                    game = {}
                    
                    idgame += 1
                    namegame = "game" + str(idgame)
                    
                    # recuperation des joueurs
                    whitename = current.headers['White'].lower()
                    print(whitename)
                    if whitename == "":
                        whitename = "john, doe"
                        
                    blackname = current.headers['Black'].lower()
                    if blackname == "":
                        blackname = "john, doe"
                        
                    
                    whitename = whitename.split(",")
                    blackname = blackname.split(",")
                    
                    white = whitename[0].lower() +", "+ whitename[1].lower()
                    black = blackname[0].lower() +", "+ blackname[1].lower()
    
                    # recuperation des ELO depuis le PGN
                    white_elo = current.headers['WhiteElo']
                    if white_elo == "":
                        white_elo = 0
                        
                    black_elo = current.headers['BlackElo']
                    if black_elo == "":
                        black_elo = 0
                    # recuperation des ELO, Nationalites et sexe depuis la base csv
                    for p in playerbase:
                        if playerbase[p]['name'] in white:
                            w_elo = playerbase[p]['elo']
                            white_nat = playerbase[p]['nat']
                            white_gen = playerbase[p]['sexe']
                        else:
                            w_elo = 0
                            white_nat = '175'
                            white_gen = 'M'
                           
                        if playerbase[p]['name'] in black:
                            b_elo = playerbase[p]['elo']
                            black_nat = playerbase[p]['nat']
                            black_gen = playerbase[p]['sexe']
                        else:
                            b_elo = 0
                            black_nat = '175'
                            black_gen = 'M'
                    
                    # recuperation de l'ouverture            
                    eco = current.headers["ECO"]
                    
                    # recuperation des coups joues
                    listmoves = {}
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
        
                        # coup joue
                        next_node = node.variation(0)
                        pgn_move = node.board().san(next_node.move)
                        
                        #print(pgn_move)
                        # recuperation petit roque | grand roque
                        if(pgn_move == "O-O" or pgn_move == "O-O-O"):
                            node = pgn_move
                        else : 
                            node = pgn_move
                            
                        for p in pgn_move:
                            if p == "=":
                                pgn_move = pgn_move[:-2]
                                print(pgn_move)
                                
                        if pgn_move[-1] == "=":
                            pgn_move = pgn_move[:-1]
                            print(pgn_move)
                        move = chess.Move.uci(next_node.move)

                        fullmove = {}
                        fullmove.update({'node':node, 'move':move})
                        
                        # ajout du coup au dictionnaire
                        listmoves.update({str(cpt):fullmove})
                        
                        node = next_node
                        
                        
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#            
                    
                    # ecriture de la partie
                    datas = {}
                    datas.update({"white":white, "whiteElo":max(int(white_elo), int(w_elo)), "whiteNat":white_nat, "whiteGen":white_gen, "black":black, "blackElo":max(int(black_elo), int(b_elo)), "blackNat":black_nat, "blackGen":black_gen, "eco":eco, "moves": listmoves})
        
                    # ajout de la partie dans le dictionnaire                
                    game.update({namegame:datas})
                
                base.update(game)
                
            except(KeyError):
                pass
        return base

