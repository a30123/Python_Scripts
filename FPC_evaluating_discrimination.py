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
people=('Tom','Dick','Harry','Slim','Jim')
figure_folder="C://Users//A30123.ITRI//Documents//Python Scripts//FPC//Try_20150907_evaluate_discrimination//output"
folder_path="C://Users//A30123.ITRI//Documents//Python Scripts//FPC//Try_20150907_evaluate_discrimination//mean//"
normal_index_path="C://Users//A30123.ITRI//Desktop//Tasks//FPC//Index//one third normal//"
abnormal_index_path="C://Users//A30123.ITRI//Desktop//Tasks//FPC//Index//one third abnormal//"
#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()
single_file_path=folder_path+"slide window-7350MAbr(20110329).csv"
single_file_path2=normal_index_path+"7350MAbr(20110329).csv"
single_file_path3=abnormal_index_path+"7350MAbr(20110329).csv"


All_temp=pd.read_csv(single_file_path,header=None)


normal_index=get_single_column_from_csv(single_file_path2)
abnormal_index=get_single_column_from_csv(single_file_path3)
    
            
yes_normal=(normal_index==1)
yes_abnormal=(abnormal_index==1)
    
All_temp_normal=All_temp[yes_normal]
All_temp_abnormal=All_temp[yes_abnormal]

subset_All_temp=All_temp.loc[:,(All_temp_normal.apply(pd.Series.nunique)!=1) & (All_temp_abnormal.apply(pd.Series.nunique)!=1)]
sensor_list=list(subset_All_temp.columns.values)
sensor_list=sensor_list[1:len(sensor_list)]
 
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



distance_value=np.dot((normal_mean-abnormal_mean).T,np.dot(np.linalg.inv((normal_covariance+abnormal_covariance)/2),(normal_mean-abnormal_mean)))/8+math.log(np.linalg.det((normal_covariance+abnormal_covariance)/2)/math.sqrt(np.linalg.det(normal_covariance)*np.linalg.det(abnormal_covariance)))/2

y_pos=np.arange(len(people))
performance=distance_value*np.ones(len(people))

plt.barh(y_pos,performance,align='center',color='DarkOliveGreen',alpha=0.4)
plt.yticks(y_pos,people)
plt.xlabel('Bhattacharyya distance')
plt.title('How fast do you want to go today')


complete_path_to_save_figure=figure_folder+"//"+"try.png"


plt.show
plt.savefig(complete_path_to_save_figure,dpi=200)
plt.clf()




print('RUN TIME: %.2f secs' % (time.time()-tstart))

