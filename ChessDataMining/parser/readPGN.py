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
            
            datas = {}
            datas.update({"white":white, "whiteElo":white_elo, "black":black, "blackElo":black_elo, "eco":eco})
            
            game.update({namegame:datas})
            
        
        base.update(game)
    return base