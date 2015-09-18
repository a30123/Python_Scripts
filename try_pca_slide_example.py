# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 09:56:40 2015

@author: A30123
"""
import numpy as np
from matplotlib.mlab import PCA as mlabPCA
import math

X=np.asarray([173,155,175,171,166,167,163,155,159,168,166,169,159,154,160,66,49,72,68,63,64,61,52,55,65,61,73,57,49,60])
X=np.transpose(np.reshape(X,(2,15)))

np.mean(X,axis=0)
np.std(X,axis=0)
length=X.shape[0]
length
X_prime_prime=(X-np.mean(X,axis=0))/np.std(X,axis=0)*math.sqrt((length-1)/length)  
X_prime_prime

X_prime_prime2=(X-np.mean(X,axis=0))/np.std(X,axis=0)
X_prime_prime2


mlab_pca_test=mlabPCA(X)
scores=mlab_pca_test.Y
scores.shape
scores[:,0]
scores[:,1]

loadings=mlab_pca_test.Wt
loadings.shape
loadings


from sklearn.decomposition import PCA as sklearnPCA
sklearn_pca = sklearnPCA(n_components=2)
sklearn_transf = sklearn_pca.fit_transform(X)
sklearn_transf

sklearn_transf_prime=sklearn_pca.fit_transform(X_prime_prime)
sklearn_transf_prime