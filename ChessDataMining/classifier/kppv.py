# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 17:25:21 2017

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

from sklearn.neighbors import KNeighborsClassifier

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


class KPPV:
    
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
        K-plus proche voisins - methode uniform
        """
        clf_kppv_uniform = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', KNeighborsClassifier(15, weights='uniform')),])
        kppv_uniform = clf_kppv_uniform.fit(X_train, y_train)
        uniform_predict = kppv_uniform.predict(X_test)
        
        # calculs
        matrix = confusion_matrix(y_test, uniform_predict)
        cross = cross_val_score(clf_kppv_uniform, X_test, y_test, cv=5)
        avg_prec = cross.mean()
        ecart = cross.std()*2
        score_ROC = '{0:.2f}'.format(roc_auc_score(self.convert(y_test), self.convert(uniform_predict)))
        report = classification_report(y_test, uniform_predict,target_names=['good', 'spam'])
        
        # affichage resultats
        print('+'*50)
        print("Classifieur : SVM KPPV methode uniform")
        print("Precision sur 5 tests :", cross)
        print("Precision_moyenne : %0.2f (+/- %0.2f)" %(avg_prec, ecart))
        print("Matrice de confusion : ", matrix)
        print("Aire sous ROC : ", score_ROC)
        print("Rapport Eval :", report)
        print('+'*50)
        print(''*50)
        
        
        #####################################################################

        
        """
        K-plus proche voisins - methode distance
        """
        clf_kppv_distance = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', KNeighborsClassifier(15, weights='distance')),])
        kppv_distance = clf_kppv_distance.fit(X_train, y_train)
        distance_predict = kppv_distance.predict(X_test)
        
        # calculs
        matrix = confusion_matrix(y_test, distance_predict)
        cross = cross_val_score(clf_kppv_distance, X_test, y_test, cv=5)
        avg_prec = cross.mean()
        ecart = cross.std()*2
        score_ROC = '{0:.2f}'.format(roc_auc_score(self.convert(y_test), self.convert(distance_predict)))
        report = classification_report(y_test, distance_predict,target_names=['good', 'spam'])
        
        # affichage resultats
        print('+'*50)
        print("Classifieur : SVM KPPV methode distance")
        print("Precision sur 5 tests :", cross)
        print("Precision_moyenne : %0.2f (+/- %0.2f)" %(avg_prec, ecart))
        print("Matrice de confusion : ", matrix)
        print("Aire sous ROC : ", score_ROC)
        print("Rapport Eval :", report)
        print('+'*50)
        print(''*50)
        
        
        #####################################################################