# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:24:02 2017

@author: 21003607
"""
import chess
import chess.uci
import chess.pgn

import pickle

from parser import *
#from classifier import *


def main():
    
        # lecture du fichier PGN - creation du dictionnaire
        dico = build("data/pgn/train.pgn")
        output = open("data/output/codex.txt", 'ab+')
        
        # ecriture du dictionnaire
        pickle.dump(dico, output)
        output.close
        
        # recuperation du dictionnaire
        intels = open('data/output/codex.txt', 'rb')
        gamedic = pickle.load(intels)
        
        #print(len(gamedic))
        #print('')
        for i in gamedic :
            print(i)
            #print("")
            #print(gamedic[i])
            
        
        
        engine = chess.uci.popen_engine("stockfish/Linux/stockfish_8_x64")
        engine.uci()
        
        info_handler = chess.uci.InfoHandler()
        engine.info_handlers.append(info_handler)
        
        board = chess.Board(); 
        
        board.push_san("e2e4")
        print(board)
        print('')
        
        engine.position(board)
        oracle_move = engine.go()   # movetime = 2000 -- init la recherche pour 2000 milliseconds -- non interessant pour l'ampleur du fichier -- 20K+ lignes
        best_move = oracle_move.bestmove
        print(best_move)
        print('')
        
        boardA = board
        boardB = board
        
        boardA.push(best_move)
        engine.position(boardA)
        current_scoreA = info_handler.info["score"][1].cp
        print(current_scoreA)
        
        boardB.push_san("e4e5")
        engine.position(boardB)
        current_scoreB = info_handler.info["score"][1].cp
        print(current_scoreB)
        
        
        
if __name__ == "__main__":
    main()