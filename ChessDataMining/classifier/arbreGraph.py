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



import pydotplus



import warnings as wa
wa.filterwarnings('ignore')



class ArbreGraph:
    

    def classify(self, vectors, classes, features):
        """
        Lecture du fichier
        """
        
        data = open(vectors, 'r')
        X = []
        y = []
        
        data_lines = data.readlines()
        for i in range(len(data_lines)):
            line = data_lines[i].rstrip()
            line = data_lines[i].split('\t')
            y.append(line[0])
            X.append(line[1][:-1])
        
        count_vect = CountVectorizer()
        X = count_vect.fit_transform(X)        
        
        tf_transformer = TfidfTransformer(use_idf=True).fit(X)
        X = tf_transformer.transform(X)
     
        
        clf = tree.DecisionTreeClassifier('gini')
        clf = clf.fit(X, y)
        dot_data = StringIO() 
        tree.export_graphviz(clf, out_file=dot_data, class_names=classes, filled=True, rounded=True) 
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue()) 
        graph.write_pdf("data/tree/iris.pdf") 
        