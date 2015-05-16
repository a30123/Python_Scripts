# -*- coding: utf-8 -*-
"""
Created on Sat May 16 21:52:27 2015

@author: Mary
"""


#########################################################################################################
###      #####  #####        #####       ###############    #   ###  ###       ###       ################
###  #########  ########  ########  ####################  #  #  ###  ###  ###  ###  ###  ################
###  #########  ########  ########  ####################  ####  ###  ###  ###  ###  ###  ################
###      #####  ########  ########       ###############  ####  ###  ###       ###       ################
#########################################################################################################

#########################################################################################################
#######################################   IMPORT LIBRARIES    ###########################################
#########################################################################################################
import time
import numpy as np
#import re
#import math
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")

from sklearn.cluster import KMeans
#########################################################################################################
#######################################   FUNCTIONS           ###########################################
#########################################################################################################
def get_matrix_from_csv(csvpathfilename):
#    import csv
#    import numpy as np      
    
    thelist=[]
    
    with open(csvpathfilename,'rU') as csvfile:
        contents=csv.reader(csvfile)
        for row in contents:
            thelist.append(row)
        
    return np.array(thelist)    
#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
file_path="C://Users//Mary//Music//Documents//Python Scripts//Try_20150516_portion_of_each_segment//output.csv"

#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()
X=get_matrix_from_csv(file_path)

kmeans=KMeans(n_clusters=4)
kmeans.fit(X)

centroids=kmeans.cluster_centers_
labels=kmeans.labels_
colors=["g.","r.","y.","k."]

for i in range(len(X)):
    plt.plot(X[i][0],X[i][3],colors[labels[i]],markersize=10)
    
plt.scatter(centroids[:,0],centroids[:,3])

print('RUN TIME: %.2f secs' % (time.time()-tstart))