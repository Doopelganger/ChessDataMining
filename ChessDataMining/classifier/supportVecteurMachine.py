# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 16:21:25 2017

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

from sklearn.svm import SVC
from sklearn.svm import LinearSVC

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


class SupportVecteurMachine:
    
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
        Support Vecteur Machine - linear kernel
        """
        # construction classifieur
        clf_svm_lkernel = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', SVC(kernel='linear', C=1.0)),])
        svm_lkernel = clf_svm_lkernel.fit(X_train, y_train)
        svm_kernel_predict = svm_lkernel.predict(X_test)
        
        # calculs
        matrix = confusion_matrix(y_test, svm_kernel_predict)
        cross = cross_val_score(clf_svm_lkernel, X_test, y_test, cv=5)
        avg_prec = cross.mean()
        ecart = cross.std()*2
        score_ROC = '{0:.2f}'.format(roc_auc_score(self.convert(y_test), self.convert(svm_kernel_predict)))
        report = classification_report(y_test, svm_kernel_predict,target_names=classes)
        
        # affichage resultats
        print('+'*50, file = outfile)
        print("Classifieur : SVM linear kernel", file = outfile)
        print("Precision sur 5 tests :", cross, file = outfile)
        print("Precision_moyenne : %0.2f (+/- %0.2f)" %(avg_prec, ecart), file = outfile)
        print("Matrice de confusion : ", matrix, file = outfile)
        print("Aire sous ROC : ", score_ROC, file = outfile)
        print("Rapport Eval :", report, file = outfile)
        print('+'*50, file = outfile)
        print(''*50, file = outfile)
        
        
        #####################################################################
        
        
        """
        Support Vecteur Machine - linear SVC
        """
        clf_svm_lsvc = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', LinearSVC(C=1.0, dual=False, tol=0.001)),])
        svm_lsvc = clf_svm_lsvc .fit(X_train, y_train)
        svm_lsvc_predict = svm_lsvc.predict(X_test)
        
        # calculs
        matrix = confusion_matrix(y_test, svm_lsvc_predict)
        cross = cross_val_score(clf_svm_lsvc, X_test, y_test, cv=5)
        avg_prec = cross.mean()
        ecart = cross.std()*2
        score_ROC = '{0:.2f}'.format(roc_auc_score(self.convert(y_test), self.convert(svm_lsvc_predict)))
        report = classification_report(y_test, svm_lsvc_predict,target_names=classes)
        
        # affichage resultats
        print('+'*50, file = outfile)
        print("Classifieur : SVM linear SVC", file = outfile)
        print("Precision sur 5 tests :", cross, file = outfile)
        print("Precision_moyenne : %0.2f (+/- %0.2f)" %(avg_prec, ecart), file = outfile)
        print("Matrice de confusion : ", matrix, file = outfile)
        print("Aire sous ROC : ", score_ROC, file = outfile)
        print("Rapport Eval :", report, file = outfile)
        print('+'*50, file = outfile)
        print(''*50, file = outfile)
        
        
        #####################################################################
        
        
        """
        Support Vecteur Machine - SVC gaussien
        """
        clf_svm_gauss = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', SVC(kernel='rbf', C=1.0, gamma=0.8)),])
        svm_gauss = clf_svm_gauss.fit(X_train, y_train)
        gauss_predict = svm_gauss.predict(X_test)
        
        # calculs
        matrix = confusion_matrix(y_test, gauss_predict)
        cross = cross_val_score(clf_svm_gauss, X_test, y_test, cv=5)
        avg_prec = cross.mean()
        ecart = cross.std()*2
        score_ROC = '{0:.2f}'.format(roc_auc_score(self.convert(y_test), self.convert(gauss_predict)))
        report = classification_report(y_test, gauss_predict,target_names=classes)
        
        # affichage resultats
        print('+'*50, file = outfile)
        print("Classifieur : SVM SVC gaussien", file = outfile)
        print("Precision sur 5 tests :", cross, file = outfile)
        print("Precision_moyenne : %0.2f (+/- %0.2f)" %(avg_prec, ecart), file = outfile)
        print("Matrice de confusion : ", matrix, file = outfile)
        print("Aire sous ROC : ", score_ROC, file = outfile)
        print("Rapport Eval :", report, file = outfile)
        print('+'*50, file = outfile)
        print(''*50, file = outfile)
        
        
        #####################################################################
        
        
        """
        Support Vecteur Machine - SVC polynomial
        """
        clf_svm_poly = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', SVC(kernel='poly', C=1.0, degree=7, gamma=0.8)),])
        svm_poly = clf_svm_poly.fit(X_train, y_train)
        poly_predict = svm_poly.predict(X_test)
        
        # calculs
        matrix = confusion_matrix(y_test, poly_predict)
        ecart = cross.std()*2
        cross = cross_val_score(clf_svm_poly, X_test, y_test, cv=5)
        avg_prec = cross.mean()
        score_ROC = '{0:.2f}'.format(roc_auc_score(self.convert(y_test), self.convert(poly_predict)))
        report = classification_report(y_test, poly_predict,target_names=classes)
        
        # affichage resultats
        print('+'*50, file = outfile)
        print("Classifieur : SVM SVC polynomial", file = outfile)
        print("Precision sur 5 tests :", cross, file = outfile)
        print("Precision_moyenne : %0.2f (+/- %0.2f)" %(avg_prec, ecart), file = outfile)
        print("Matrice de confusion : ", matrix, file = outfile)
        print("Aire sous ROC : ", score_ROC, file = outfile)
        print("Rapport Eval :", report, file = outfile)
        print('+'*50, file = outfile)
        print(''*50, file = outfile)
        
        
        #####################################################################
        outfile.close()