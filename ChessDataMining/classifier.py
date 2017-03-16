# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 10:27:27 2017

@author: 21003607
"""

from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import datasets
from sklearn import svm
from sklearn import metrics


data = open("data/output/testElo", 'r')

continuer = True

X = []
Y = []

while(continuer):
    
    line = data.readline()
    if(line == ""):
        continuer = False
    else:
        line = line.rstrip()
        line = line.split(";")
  
        Y.append(line[0])
        line.remove(line[0])
        X.append(line)
        
        
# print("features : ",X)
# print("classes : ",Y)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)

test1 = clf.predict(['0.30', '3', '80', '350', '3'])
test2 = clf.predict(['0.27', '4', '63', '350', '3'])
test3 = clf.predict(['0.45', '6', '48', '353', '4'])
print('')

print(test1)
print(test2)
print(test3)
print('')
print("Classification pour Training Dummy : ", max(test1, test2, test3))
print('')

# separation des donnees pour test
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0)

clf = svm.SVC(kernel='linear', C=1)

# jeu de precision sur 5 tests
scores = cross_val_score(clf, X, Y, cv=6)
print("scores : ", scores)

precision = "{0:.2f}".format(scores.mean())
print("precision : ", precision)

ecart_type = "{0:.2f}".format(scores.std()*2)
print("ecart_type (confidence interval) : ", ecart_type)

print('')



# rappel = nombre de doc correctement attribués a la classe i / nombre de doc de classe i
# rappel = nbCorrect / nbClasse


# precision = nombre de doc correctement attribues a la classe i / nombre de document attribues
# precision = nbCorrect / nbAttClasse