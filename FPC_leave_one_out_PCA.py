# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 10:35:29 2015

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
import pandas as pd
import numpy as np
import os
import csv
import math
from matplotlib import pyplot as plt
from matplotlib.mlab import PCA as mlabPCA
#from ggplot import *
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
training_set_folder="C://Users//A30123.ITRI//Desktop//Tasks//FPC//processed data//IO timeout processed//leave_one_out_cross_validation//train//"
testing_set_folder="C://Users//A30123.ITRI//Desktop//Tasks//FPC//processed data//IO timeout processed//leave_one_out_cross_validation//test//"
subfolder="set 1"
folder_to_read_from="C://Users//A30123.ITRI//Desktop//Tasks//FPC//data//sensor_csv"
figure_folder="C://Users//A30123.ITRI//Documents//Python Scripts//FPC//Try_20150903_PCA//output"
index_folder="C://Users//A30123.ITRI//Desktop//Tasks//FPC//Index//trip point//"
flat_region_folder="C://Users//A30123.ITRI//Desktop//Tasks//FPC//Index//flat region//"

#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()
training_set_subfolder=os.path.join(training_set_folder,subfolder)

files_in_folder = os.listdir(training_set_subfolder)


single_file_path=os.path.join(training_set_subfolder,files_in_folder[0])
    
All_temp=pd.read_csv(single_file_path)

sensor_list=list(All_temp.columns.values)
sensor_list=sensor_list[1:len(sensor_list)]
intersect_sensor_list=sensor_list

#All={0:0,1:0,2:0,3:0,4:0,5:0}
#sensor_values={0:0,1:0,2:0,3:0,4:0,5:0}
#trip_points={0:0,1:0,2:0,3:0,4:0,5:0}
#flat_regions={0:0,1:0,2:0,3:0,4:0,5:0}
no_of_runs=len(files_in_folder)
#no_of_runs=1


for i in range(no_of_runs):
    single_file_path=os.path.join(training_set_subfolder,files_in_folder[i])
    single_file_path2=os.path.join(index_folder,files_in_folder[i])  
    #single_file_path3=os.path.join(flat_region_folder,files_in_folder[i]) 
        
    All_temp=pd.read_csv(single_file_path)
 
    All_temp=All_temp.convert_objects(convert_numeric=True)
    All_temp[sensor_list]=All_temp[sensor_list].astype('float32')
    

#    All[i]=All_temp
    
    
    temp_trip=get_single_column_from_csv(single_file_path2)
#    trip_points[i]=np.array(temp_trip)
    no_trip=(temp_trip==0)    
    subset_All_temp=All_temp[no_trip]

    #temp_flat=get_single_column_from_csv(single_file_path3)
    
            
    #yes_flat=(temp_flat==1)    
    #subset_All_temp=All_temp[yes_flat]
 
    
#    #delete I/O timeout rows
#    time_out_index=list(map(math.isnan,subset_All_temp[sensor_list[1]]))
#    time_in_index=(np.array(time_out_index)==False)
#    subset_All_temp=subset_All_temp[time_in_index]    
    
    
    subset_All_temp2=subset_All_temp[sensor_list]
    subset_All_temp2=subset_All_temp2.loc[:,subset_All_temp2.apply(pd.Series.nunique)!=1]
    sensor_list_temp=list(subset_All_temp2.columns.values)
    sensor_list_temp=sensor_list_temp[1:len(sensor_list_temp)] 
    intersect_sensor_list=set(intersect_sensor_list).intersection(sensor_list_temp)
    intersect_sensor_list2=list(intersect_sensor_list)
    if i==0:
        subset_All_temp3=subset_All_temp2[intersect_sensor_list2]
    else:
        subset_All_temp3=pd.concat([subset_All_temp3[intersect_sensor_list2],subset_All_temp2[intersect_sensor_list2]])
    
    
#subset_All_temp3=subset_All_temp3.loc[:,subset_All_temp3.apply(pd.Series.nunique)!=1]

mlab_pca=mlabPCA(subset_All_temp3)
scores=mlab_pca.Y
  
cc=list(range(scores.shape[0]))
cm=plt.cm.get_cmap('RdYlBu')
plt.style.use('ggplot')
ax=plt.scatter(scores[:,0],scores[:,1],c=cc,marker=(5,2),alpha=0.5,cmap=cm)
plt.colorbar(ax)

plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title(files_in_folder[i].replace(".csv",""))
#    ax.grid(True)
#    ax.set_xlabel('PC1')
#    ax.set_ylabel('PC2')
 
complete_path_to_save_figure=figure_folder+"//PCA_"+files_in_folder[i].replace("csv","png")

plt.show
plt.savefig(complete_path_to_save_figure,dpi=200)
plt.clf()
#    
print('RUN TIME: %.2f secs' % (time.time()-tstart))

