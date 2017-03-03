# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 12:00:26 2017

@author: 21003607
"""

"""
module pour calculer le score cp du coup considere
"""


def calcul(board, node, next_node):
    
   board.push_san(node.board().san(next_node.move))
            
    engine.position(board)
    current_score = info_handler.info["score"][1].cp
    
    return current_score