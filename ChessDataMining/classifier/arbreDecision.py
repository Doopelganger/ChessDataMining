# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 11:35:18 2017

@author: doopleganger
"""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.preprocessing import LabelEncoder

from sklearn.pipeline import Pipeline

from sklearn.model_selection import train_test_split

from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import classification_report

from sklearn.tree import DecisionTreeClassifier

import numpy as np

import warnings as wa
wa.filterwarnings('ignore')


class DenseMatrixTransformer(TfidfTransformer):

    def transform(self, X, y=None, **fit_params):
        return X.todense()
        
    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)
        
    def fit(self, X, y=None, **fit_params):
        return self


class ArbreDecision:
    
    def convert(self, label):
        labelEncoder = LabelEncoder()
        code = labelEncoder.fit_transform(label)
        return code
    
    def classify(self, vectors, classes, features):
        """
        Lecture du fichier
        """
        data = np.genfromtxt(vectors, delimiter ="\t", dtype=None)
        # classes
        y = data[:,0:-1]
        # traits
        X = data[:,-1]
        
        """
        Decoupage des donnees - 30% training | 70% test
        """
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)
        y_test = y_test.ravel()

        """
        Arbre de decision - methode entropie de Shannon
        """
        # construction classifieur
        clf_tree_entropy = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', DecisionTreeClassifier('entropy')),])   
        tree_entropy = clf_tree_entropy.fit(X_train, y_train)
        entropy_predict = tree_entropy.predict(X_test)
        
        # calculs
        matrix = confusion_matrix(y_test, entropy_predict)
        cross = cross_val_score(clf_tree_entropy, X_test, y_test, cv=5)
        avg_prec = cross.mean()
        ecart = cross.std()*2
        score_ROC = '{0:.2f}'.format(roc_auc_score(self.convert(y_test), self.convert(entropy_predict)))
        report = classification_report(y_test, entropy_predict,target_names=classes)
        
        # affichage resultats
        print('+'*50)
        print("Classifieur : Arbre de Decision avec Entropie de Shannon")
        print("Precision sur 5 tests :", cross)
        print("Precision_moyenne : %0.2f (+/- %0.2f)" %(avg_prec, ecart))
        print("Matrice de confusion : ", matrix)
        print("Aire sous ROC : ", score_ROC)
        print("Rapport Eval :", report)
        print('+'*50)
        print(''*50)
        
        
        #####################################################################


        """
        Arbre de decision - methode index de Gini
        """
        # construction classifieur
        clf_tree_gini = Pipeline([('vect', CountVectorizer()), ('tfid', TfidfTransformer()), ('clf', DecisionTreeClassifier('gini')),])
        tree_gini = clf_tree_gini.fit(X_train, y_train)
        gini_predict = tree_gini.predict(X_test)
        
        # calculs
        matrix = confusion_matrix(y_test, gini_predict)
        cross = cross_val_score(clf_tree_gini, X_test, y_test, cv=5)
        avg_prec = cross.mean()
        ecart = cross.std()*2
        score_ROC = '{0:.2f}'.format(roc_auc_score(self.convert(y_test), self.convert(gini_predict)))
        report = classification_report(y_test, gini_predict,target_names=classes)
        
        # affichage resultats
        print('+'*50)
        print("Classifieur : Arbre de Decision avec index de Gini")
        print("Precision sur 5 tests :", cross)
        print("Precision_moyenne : %0.2f (+/- %0.2f)" %(avg_prec, ecart))
        print("Matrice de confusion : ", matrix)
        print("Aire sous ROC : ", score_ROC)
        print("Rapport Eval :", report)
        print('+'*50)
        print(''*50)
        
        
        #####################################################################