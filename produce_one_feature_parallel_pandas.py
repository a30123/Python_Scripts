# -*- coding: utf-8 -*-
"""
Created on Fri June 30

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
import os #-------------------------------------------------------Miscellaneous operating system interfaces
import numpy as np #----------------------------------------------array manipulation, scientific computing
import csv#-------------------------------------------------------read write csv files
import re #-------------------------------------------------------regular expressions
from joblib import Parallel, delayed
import multiprocessing
import time
import pandas as pd
############################################################################################################



#########################################################################################################
#######################################   FUNCTIONS           ###########################################
#########################################################################################################


#####################################
#reference:    http://stackoverflow.com/questions/273192/check-if-a-directory-exists-and-create-it-if-necessary     
def ensure_dir(f):
#    import os
    d=os.path.abspath(f)
    if not os.path.exists(d):
        os.makedirs(d)
    
def extract_serial_number(filename):
#    import re
    extract_regular_expression=re.search('(_\d+-setpoint)',filename)
    serial_number_string=extract_regular_expression.group(0)
    serial_number_string=serial_number_string.replace('-setpoint','')
    serial_number_string=serial_number_string.replace('_','') 
    value_of_number=int(serial_number_string)
    return value_of_number
    
def write_array_to_csv(filename_path,listname):
#    import csv    
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

#######################################


#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################

#intialize "sensor variable of interest","folder to accesss", and "folder to save output to"
sensor_variables="GapSpeed"#-------------------------------------"sensor variable of interest"
folder_to_read_from="E://MovedFromD//CSV//TS1//FiveFeatures_2492runs//setpoint"#--------------------------------------------"folder to access"
folder_to_read_from2="E://MovedFromD//CSV//TS1//FiveFeatures_2492runs//current"#--------------------------------------------"folder to access"
folder_to_read_from3="E://MovedFromD//CSV//TS1//FiveFeatures_2492runs//deviation"
path_to_save_list="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150729_PLA_five_features//TS1_GapSpeed_variance.csv"#----------------------------"folder to save output to"
#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()
files_in_folder = os.listdir(folder_to_read_from) 
files_in_folder.sort(key=extract_serial_number)

no_of_runs=len(files_in_folder)

num_cores=multiprocessing.cpu_count()
percentage_list=np.zeros(no_of_runs)

    #----------------------------------------------------------------------------------plots the values and saves as png file into designated folder    

def repeat_this(i,files_in_folder,folder_to_read_from,folder_to_read_from2,folder_to_read_from3,sensor_variables):
    temp_file_name=files_in_folder[i]    
    #single_file_path=os.path.join(folder_to_read_from, temp_file_name)
    single_file_path2=os.path.join(folder_to_read_from2, temp_file_name.replace('-setpoint','-current'))
    #single_file_path3=os.path.join(folder_to_read_from3, temp_file_name.replace('-setpoint','-deviation'))

    #All=pd.read_csv(single_file_path)
    #setpoint_values=np.asarray(All[:][sensor_variables])
    
    All=pd.read_csv(single_file_path2)
    current_values=np.asarray(All[:][sensor_variables])
    
    #All=pd.read_csv(single_file_path3)
    #deviation_values=np.asarray(All[:][sensor_variables])

    
    percentage_list[i]=(np.var(current_values))  
    
    return percentage_list[i]  

if __name__=="__main__":
    cool=Parallel(n_jobs=5)(delayed(repeat_this)(i,files_in_folder,folder_to_read_from,folder_to_read_from2,folder_to_read_from3,sensor_variables) for i in range(no_of_runs))     

    write_array_to_csv(path_to_save_list,cool)

print('RUN TIME: %.2f secs' % (time.time()-tstart))