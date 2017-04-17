# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 10:48:20 2017

@author: doopleganger
"""

from sklearn.feature_extraction.text import TfidfTransformer

class DenseMatrixTransformer(TfidfTransformer):

    def transform(self, X, y=None, **fit_params):
        return X.todense()
        
    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)
        
    def fit(self, X, y=None, **fit_params):
        return self