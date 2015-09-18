# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 11:19:24 2015

@author: A30123
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
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import pandas as pd
import csv
import math
import os
#########################################################################################################
#######################################   FUNCTIONS           ###########################################
#########################################################################################################
def get_single_column_from_csv(csvpathfilename):
#    import csv
#    import numpy as np      
    
    thelist=[]
    
    with open(csvpathfilename,'rU') as csvfile:
        contents=csv.reader(csvfile)
        for row in contents:
            thelist.append(float(row[0]))

    return np.array(thelist)  

#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
figure_folder="C://Users//A30123.ITRI//Documents//Python Scripts//FPC//Try_20150911_evaluate_discrimination_all_five//output"
folder_path="C://Users//A30123.ITRI//Documents//Python Scripts//FPC//Try_20150911_evaluate_discrimination_all_five//moving average//"
normal_index_path="C://Users//A30123.ITRI//Desktop//Tasks//FPC//Index//one third normal timeout deleted//"
abnormal_index_path="C://Users//A30123.ITRI//Desktop//Tasks//FPC//Index//one third abnormal timeout deleted//"
#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()
files_in_folder = os.listdir(folder_path)

people=files_in_folder[:-1]
single_file_path=os.path.join(folder_path,files_in_folder[0])
performance=np.ones(len(people))
performance2=np.ones(len(people))
performance3=np.ones(len(people))
#for i in range(len(files_in_folder)):
for i in range(5):
    single_file_path=os.path.join(folder_path,files_in_folder[i])
    single_file_path2=os.path.join(normal_index_path,files_in_folder[i])    
    single_file_path3=os.path.join(abnormal_index_path,files_in_folder[i])    
      
    All_temp=pd.read_csv(single_file_path,header=None)
    normal_index=get_single_column_from_csv(single_file_path2)
    abnormal_index=get_single_column_from_csv(single_file_path3)    
    
            
    yes_normal=(normal_index==1)
    yes_abnormal=(abnormal_index==1)
    
    All_temp_normal=All_temp[yes_normal]
    All_temp_abnormal=All_temp[yes_abnormal]

    subset_All_temp=All_temp.loc[:,(All_temp_normal.apply(pd.Series.nunique)!=1) & (All_temp_abnormal.apply(pd.Series.nunique)!=1)]
    sensor_list=list(subset_All_temp.columns.values)
    #sensor_list=sensor_list[1:len(sensor_list)]

    sensor_list=sensor_list[1:20]
 
    subset_All_temp=subset_All_temp.convert_objects(convert_numeric=True)
    subset_All_temp=subset_All_temp[:][sensor_list].astype('float32')

    subset_All_temp_normal=subset_All_temp[yes_normal]
    subset_All_temp_abnormal=subset_All_temp[yes_abnormal]

    feature_matrix_normal=np.asarray(subset_All_temp_normal)
    feature_matrix_abnormal=np.asarray(subset_All_temp_abnormal)

    normal_covariance=np.cov(feature_matrix_normal.T)
    abnormal_covariance=np.cov(feature_matrix_abnormal.T)

    normal_mean=np.mean(feature_matrix_normal, axis=0)
    abnormal_mean=np.mean(feature_matrix_abnormal,axis=0)


    ######Bhattacharyya distance
    temp_vector=normal_mean-abnormal_mean
    temp_matrix1=(normal_covariance+abnormal_covariance)/2
    temp_value1=np.linalg.det(temp_matrix1)
    temp_value2=np.linalg.det(normal_covariance)
    temp_value3=np.linalg.det(abnormal_covariance)
    temp_value4=temp_value1/math.sqrt(temp_value2*temp_value3)
    B_distance_value=np.dot(temp_vector.T,np.dot(np.linalg.inv(temp_matrix1),temp_vector))/8+math.log(temp_value4)/2

    #####KL-divergence of  normal set from abnormal set
    temp_matrix2=np.dot(np.linalg.inv(normal_covariance),abnormal_covariance)
    temp_matrix3=np.linalg.inv(abnormal_covariance)
    temp_value5=normal_mean.shape[0]
    temp_value6=temp_value2/temp_value3
    KL_distance_value=(np.trace(temp_matrix2)+np.dot(temp_vector.T,np.dot(temp_matrix3,temp_vector))-temp_value5+math.log(temp_value6))/2
    
    #####KL-divergence of abnormal set from normal set
    temp_matrix22=np.dot(np.linalg.inv(abnormal_covariance),normal_covariance)
    temp_matrix32=np.linalg.inv(normal_covariance)
    temp_value52=normal_mean.shape[0]
    temp_value62=temp_value3/temp_value2
    KL_distance_value2=(np.trace(temp_matrix22)+np.dot(temp_vector.T,np.dot(temp_matrix32,temp_vector))-temp_value52+math.log(temp_value62))/2

    #### Average of mahalanobis distance to normal


    performance[i]=B_distance_value
    performance2[i]=KL_distance_value
    performance3[i]=KL_distance_value2

y_pos=(np.arange(len(people)))[::-1]
plt.barh(y_pos,performance,align='center',color='DarkOliveGreen',alpha=0.4)
plt.yticks(y_pos,people)
plt.xlabel('Bhattacharyya distance')
plt.title('Similarity between normal and abnormal clusters')
complete_path_to_save_figure=figure_folder+"//"+"Bhattacharyya distance.png"
plt.show
plt.savefig(complete_path_to_save_figure,dpi=200,bbox_inches='tight')
plt.clf()


plt.barh(y_pos,performance2,align='center',color='PeachPuff',alpha=0.4)
plt.yticks(y_pos,people)
plt.xlabel('KL divergence1')
plt.title('KL-divergence of  normal set from abnormal set')
complete_path_to_save_figure=figure_folder+"//"+"KL_divergence1.png"
plt.show
plt.savefig(complete_path_to_save_figure,dpi=200,bbox_inches='tight')
plt.clf()


plt.barh(y_pos,performance3,align='center',color='PaleVioletRed',alpha=0.4)
plt.yticks(y_pos,people)
plt.xlabel('KL divergence2')
plt.title('KL-divergence of abnormal set from normal set')
complete_path_to_save_figure=figure_folder+"//"+"KL_divergence2.png"
plt.show
plt.savefig(complete_path_to_save_figure,dpi=200,bbox_inches='tight')
plt.clf()

print('RUN TIME: %.2f secs' % (time.time()-tstart))

