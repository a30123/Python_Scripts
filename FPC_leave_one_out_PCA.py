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
    
def ensure_dir(f):
#    import os
    d=os.path.abspath(f)
    if not os.path.exists(d):
        os.makedirs(d)
#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
training_set_folder="C://Users//A30123.ITRI//Desktop//Tasks//FPC//processed data//IO timeout processed//leave_one_out_cross_validation//train//"
testing_set_folder="C://Users//A30123.ITRI//Desktop//Tasks//FPC//processed data//IO timeout processed//leave_one_out_cross_validation//test//"
subfolder="set 5"
#folder_to_read_from="C://Users//A30123.ITRI//Desktop//Tasks//FPC//data//sensor_csv"
trip_folder="C://Users//A30123.ITRI//Desktop//Tasks//FPC//Index//trip point//"
#flat_region_folder="C://Users//A30123.ITRI//Desktop//Tasks//FPC//Index//flat region//"
output_folder="C://Users//A30123.ITRI//Documents//Python Scripts//FPC//Try_20150916_PCA_leave_one_out//output//"
#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()
training_set_subfolder=os.path.join(training_set_folder,subfolder)
files_in_training_folder = os.listdir(training_set_subfolder)
single_training_file_path=os.path.join(training_set_subfolder,files_in_training_folder[0])
    
training_data_temp=pd.read_csv(single_training_file_path)

sensor_list=list(training_data_temp.columns.values)
time_column=sensor_list[0]
sensor_list=sensor_list[1:len(sensor_list)]
intersect_sensor_list=sensor_list

#All={0:0,1:0,2:0,3:0,4:0,5:0}
#sensor_values={0:0,1:0,2:0,3:0,4:0,5:0}
#trip_points={0:0,1:0,2:0,3:0,4:0,5:0}
#flat_regions={0:0,1:0,2:0,3:0,4:0,5:0}
no_of_runs=len(files_in_training_folder)
#no_of_runs=1


for i in range(no_of_runs):
    single_training_file_path=os.path.join(training_set_subfolder,files_in_training_folder[i])
    single_trip_file_path=os.path.join(trip_folder,files_in_training_folder[i])  
    #single_file_path3=os.path.join(flat_region_folder,files_in_folder[i]) 
        
    training_data_temp=pd.read_csv(single_training_file_path)
 
    training_data_temp=training_data_temp.convert_objects(convert_numeric=True)
    training_data_temp[sensor_list]=training_data_temp[sensor_list].astype('float32')
    

#    All[i]=All_temp
    
    
    temp_trip=get_single_column_from_csv(single_trip_file_path)
#    trip_points[i]=np.array(temp_trip)
    no_trip=(temp_trip==0)    
    subset_training_temp=training_data_temp[no_trip]

    #temp_flat=get_single_column_from_csv(single_file_path3)
    
            
    #yes_flat=(temp_flat==1)    
    #subset_All_temp=All_temp[yes_flat]
 
    
#    #delete I/O timeout rows
#    time_out_index=list(map(math.isnan,subset_All_temp[sensor_list[1]]))
#    time_in_index=(np.array(time_out_index)==False)
#    subset_All_temp=subset_All_temp[time_in_index]    
    
    
    subset_training_temp2=subset_training_temp[sensor_list]
    subset_training_temp2=subset_training_temp2.loc[:,subset_training_temp2.apply(pd.Series.nunique)!=1]
    sensor_list_temp=list(subset_training_temp2.columns.values)
    sensor_list_temp=sensor_list_temp[1:len(sensor_list_temp)] 
    intersect_sensor_list=set(intersect_sensor_list).intersection(sensor_list_temp)
    intersect_sensor_list2=list(intersect_sensor_list)
    if i==0:
        subset_training_temp3=subset_training_temp2[intersect_sensor_list2]
    else:
        subset_training_temp3=pd.concat([subset_training_temp3[intersect_sensor_list2],subset_training_temp2[intersect_sensor_list2]])
    
    
#subset_All_temp3=subset_All_temp3.loc[:,subset_All_temp3.apply(pd.Series.nunique)!=1]

mlab_pca=mlabPCA(subset_training_temp3)
scores=mlab_pca.Y
loadings=mlab_pca.Wt
training_mean=np.mean(subset_training_temp3)
training_std=np.std(subset_training_temp3)


#### load testing data set
testing_set_subfolder=os.path.join(testing_set_folder,subfolder)
files_in_testing_folder = os.listdir(testing_set_subfolder)
single_testing_file_path=os.path.join(testing_set_subfolder,files_in_testing_folder[0])    
testing_data_temp=pd.read_csv(single_testing_file_path)
testing_time_column=testing_data_temp[:][time_column]
testing_data_temp=testing_data_temp.convert_objects(convert_numeric=True)
testing_data_temp2=testing_data_temp[intersect_sensor_list2].astype('float32')
    
normalized_testing=(testing_data_temp2-training_mean)/training_std
transformed_coords_testing=np.dot(normalized_testing,loadings)

PC1_coords=transformed_coords_testing[:,0]
PC2_coords=transformed_coords_testing[:,1]
cc=list(range(PC1_coords.shape[0]))
cm=plt.cm.get_cmap('RdYlBu')
plt.style.use('ggplot')
ax=plt.scatter(PC1_coords,PC2_coords,c=cc,marker=(5,2),alpha=0.5,cmap=cm)
plt.colorbar(ax)

plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title(subfolder+"_"+files_in_testing_folder[0].replace(".csv",""))
#    ax.grid(True)
#    ax.set_xlabel('PC1')
#    ax.set_ylabel('PC2')

output_subfolder=output_folder+subfolder
ensure_dir(output_subfolder)
complete_path_to_save_figure=output_subfolder+"//"+subfolder+"_"+files_in_testing_folder[0].replace(".csv",".png")

plt.show
plt.savefig(complete_path_to_save_figure,dpi=200)
plt.clf()
#    
print('RUN TIME: %.2f secs' % (time.time()-tstart))

