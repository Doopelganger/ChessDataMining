# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 10:42:11 2017

@author: doopleganger
"""

class PredictOracle:
    
    
    def __init__(self):
        self.description = "module de calcul du meilleur coup possible et du score associe"
        
    def predict(self, board, move, engine, info_handler):
        # recherche du meilleur coup a jouer selon l'Oracle
        legalmoves = board.legal_moves
        oracle_move = engine.go()   # movetime = 2000 -- init la recherche pour 2000 milliseconds -- non interessant pour l'ampleur du fichier -- 20K+ lignes
        best_move = oracle_move.bestmove
        
        score_oracle = info_handler.info["score"][1].cp
        
        for el in legalmoves:
            engine.go(searchmoves = [el])
            if str(el) == str(move):
                score_player = info_handler.info["score"][1].cp
                
        return [best_move, score_oracle, score_player]