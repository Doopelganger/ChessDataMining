# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 16:28:15 2017

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

from sklearn.externals.six import StringIO  

from sklearn import tree

import numpy as np

import pydotplus

from IPython.display import Image


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


class ArbreGraph:
    
    
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
        
        count_vect = CountVectorizer()
        X_train = count_vect.fit_transform(X_train)        
        
        tf_transformer = TfidfTransformer(use_idf=False).fit(X_train)
        X_train = tf_transformer.transform(X_train)
        
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(X_train, y_train)
        dot_data = StringIO() 
        tree.export_graphviz(clf, out_file=dot_data) 
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue()) 
        graph.write_pdf("data/tree/iris.pdf") 
        