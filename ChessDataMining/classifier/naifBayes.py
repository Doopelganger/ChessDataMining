# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 17:28:31 2017

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

from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB


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


class NaifBayes:
    
    def convert(self, label):
        labelEncoder = LabelEncoder()
        code = labelEncoder.fit_transform(label)
        return code
    
    def classify(self, vectors, classes, output):
        """
        Lecture du fichier
        """
        data = np.genfromtxt(vectors, delimiter ="\t", dtype=None)
        # classes
        y = data[:,0:-1]
        # traits
        X = data[:,-1]
        
        outfile = open(output, 'a')
        """
        Decoupage des donnees - 30% training | 70% test
        """
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)
        y_test = y_test.ravel()


        #####################################################################


        """
        Naive Bayesien - Gauss
        """
        clf_bayes_gauss = Pipeline([('vect', CountVectorizer()), ('tfidf', DenseMatrixTransformer()), ('clf', GaussianNB()),])
        bgauss = clf_bayes_gauss.fit(X_train, y_train)
        bgauss_predict = bgauss.predict(X_test)
        
        # calculs
        matrix = confusion_matrix(y_test, bgauss_predict)
        cross = cross_val_score(clf_bayes_gauss, X_test, y_test, cv=5)
        avg_prec = cross.mean()
        ecart = cross.std()*2
        score_ROC = '{0:.2f}'.format(roc_auc_score(self.convert(y_test), self.convert(bgauss_predict)))
        report = classification_report(y_test, bgauss_predict,target_names=['good', 'spam'])
        
        # affichage resultats
        print('+'*50, file = outfile)
        print("Classifieur : Naive Bayesien methode Gauss", file = outfile)
        print("Precision sur 5 tests :", cross, file = outfile)
        print("Precision_moyenne : %0.2f (+/- %0.2f)" %(avg_prec, ecart), file = outfile)
        print("Matrice de confusion : ", matrix, file = outfile)
        print("Aire sous ROC : ", score_ROC, file = outfile)
        print("Rapport Eval :", report, file = outfile)
        print('+'*50, file = outfile)
        print(''*50, file = outfile)
        
        
        #####################################################################
        
        """
        Naive Bayesien - Multinomial
        """
        clf_bayes_multi = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB()),])
        bmulti = clf_bayes_multi.fit(X_train, y_train)
        bmulti_predict = bmulti.predict(X_test)
        
        # calculs
        matrix = confusion_matrix(y_test, bmulti_predict)
        cross = cross_val_score(clf_bayes_multi, X_test, y_test, cv=5)
        avg_prec = cross.mean()
        ecart = cross.std()*2
        score_ROC = '{0:.2f}'.format(roc_auc_score(self.convert(y_test), self.convert(bmulti_predict)))
        report = classification_report(y_test, bmulti_predict,target_names=['good', 'spam'])
        
        # affichage resultats
        print('+'*50, file = outfile)
        print("Classifieur : Naive Bayesien methode Multinomial", file = outfile)
        print("Precision sur 5 tests :", cross, file = outfile)
        print("Precision_moyenne : %0.2f (+/- %0.2f)" %(avg_prec, ecart), file = outfile)
        print("Matrice de confusion : ", matrix, file = outfile)
        print("Aire sous ROC : ", score_ROC, file = outfile)
        print("Rapport Eval :", report, file = outfile)
        print('+'*50, file = outfile)
        print(''*50, file = outfile)
        
        
        #####################################################################
        
        """
        Naive Bayesien - Bernoulli
        """
        clf_bayes_bern = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', BernoulliNB()),])
        bbern = clf_bayes_bern.fit(X_train, y_train)
        bbern_predict = bbern.predict(X_test)
        
        # calculs
        matrix = confusion_matrix(y_test, bbern_predict)
        cross = cross_val_score(clf_bayes_bern, X_test, y_test, cv=5)
        avg_prec = cross.mean()
        ecart = cross.std()*2
        score_ROC = '{0:.2f}'.format(roc_auc_score(self.convert(y_test), self.convert(bbern_predict)))
        report = classification_report(y_test, bbern_predict,target_names=['good', 'spam'])
        
        # affichage resultats
        print('+'*50, file = outfile)
        print("Classifieur : Naive Bayesien methode Bernoulli", file = outfile)
        print("Precision sur 5 tests :", cross, file = outfile)
        print("Precision_moyenne : %0.2f (+/- %0.2f)" %(avg_prec, ecart), file = outfile)
        print("Matrice de confusion : ", matrix, file = outfile)
        print("Aire sous ROC : ", score_ROC, file = outfile)
        print("Rapport Eval :", report, file = outfile)
        print('+'*50, file = outfile)
        print(''*50, file = outfile)
        
        outfile.close()