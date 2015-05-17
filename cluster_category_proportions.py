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
import csv
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
    

    
def write_array_to_csv(filename_path,listname):
    import csv
     
    runnumberfile=open(filename_path,'w',newline='')
    wr=csv.writer(runnumberfile,quoting=csv.QUOTE_MINIMAL,delimiter=',')
    if type(listname)==list:
        for item in listname:
            wr.writerow([item])
    elif type(listname)==np.ndarray:
        if len(listname.shape)==1:
            for item in listname:
                wr.writerow([item])
        else:
            for item in listname:
                wr.writerow(item)
    else:
        print("the structure you are writing is neither a list nor an np.ndarray")
		
    runnumberfile.close()
#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
file_path="C://Users//Mary//Music//Documents//Python Scripts//Try_20150516_portion_of_each_segment//output.csv"
complete_path_to_save_figure="C://Users//Mary//Music//Documents//Python Scripts//Try_20150516_portion_of_each_segment//four_categories_two_features.png"
complete_path_to_save_figure2="C://Users//Mary//Music//Documents//Python Scripts//Try_20150516_portion_of_each_segment//four_categories_six_features.png"
complete_path_to_save_csv="C://Users//Mary//Music//Documents//Python Scripts//Try_20150516_portion_of_each_segment//category_features.csv"
#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()
X=get_matrix_from_csv(file_path)
Y=np.zeros((len(X),2))
Y[:,0]=X[:,0]
Y[:,1]=X[:,3]

kmeans=KMeans(n_clusters=4)
kmeans.fit(X)

centroids=kmeans.cluster_centers_
labels=kmeans.labels_
colors=["g.","r.","y.","k."]

for i in range(len(X)):
    plt.plot(X[i][0],X[i][3],colors[labels[i]],markersize=10)
    
plt.scatter(centroids[:,0],centroids[:,1])


plt.show
#plt.savefig(complete_path_to_save_figure)
plt.savefig(complete_path_to_save_figure2)
plt.clf()

yes_certain_category=(labels==1)
new_Y=Y[yes_certain_category]
plt.scatter(new_Y[:,0],new_Y[:,1])

category_zero_list=yes_certain_category+0
write_array_to_csv(complete_path_to_save_csv,category_zero_list)

print('RUN TIME: %.2f secs' % (time.time()-tstart))
