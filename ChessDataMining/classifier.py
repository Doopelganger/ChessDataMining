# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 10:27:27 2017

@author: 21003607
"""

from sklearn import tree

data = open("data/output/test2", 'r')

continuer = True

base = []

while(continuer):
    
    line = data.readline()
    
    if(line == ""):
        continuer = False
    else:
        line.strip('\n')
        line = line.split(";")
        for i in line:
            i.replace('\n', '')
        base.append(line)
        
        
print(base)

Y = ['0', '0.60', '5', '32', 'C50', '4']

clf = tree.DecisionTreeClassifier()
#clf = clf.fit(base, Y)