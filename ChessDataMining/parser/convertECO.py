# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 12:23:55 2017

@author: 21003607
"""
class ConvertECO:
    
    def __init__(self):
        self.description = "module de conversion du code ECO en int"
    
    def convert(self, ch):
        code = ch[:1]
            
        dico = {'A':'1', 'B':'2', 'C':'3', 'D':'4', 'E':'5', 'F':'6', 'G':'7', 'H':'8', 'I':'9', 'J':'10', 'K':'11', 'L':'12', 'M':'13', 'N':'14', 'O':'15', 'P':'16', 'Q':'17', 'R':'18', 'S':'19', 'T':'20', 'U':'21', 'V':'22', 'W':'23', 'X':'24', 'Y':'25', 'Z':'26'}
        
        alpha = dico.keys()
        
        for i in alpha:
            if i == code:
                index = dico[i]
                
        eco = index + ch[1:]
        
        return eco