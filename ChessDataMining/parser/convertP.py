# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:35:14 2017

@author: 21003607
"""
class ConvertP:
    
    def __init__(self):
        self.description = "module de conversion du symbole d'une piece en code (int)"
        
    def symbolP(self, piece):
        dico = {'K':'0', 'Q':'1', 'B':'2', 'R':'3', 'N':'4'}
        
        code = dico.get(piece)
        return code