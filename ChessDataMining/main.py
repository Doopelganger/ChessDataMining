# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:24:02 2017

@author: 21003607
"""
import chess
import chess.uci
import chess.pgn

import parser

def main():
    
        # lecture du fichier PGN - creation du dictionnaire
        dico = build("data/pgn/large.pgn")
        
        print(dico)

if __name__ == "__main__":
    main()