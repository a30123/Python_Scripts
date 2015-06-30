# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 2015

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
import matplotlib.pyplot as plt  #--------------------------------John Hunter's  2D plotting library
import re #-------------------------------------------------------regular expressions
from matplotlib import rc 
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
   

def read_single_variable_as_stringlist_csv(csvpathfilename, variablename):
#   import csv
#   import numpy as np      
    
    notfirst=1
    thelist=[]
    
    with open(csvpathfilename,'rU') as csvfile:
        contents=csv.reader(csvfile)
        for row in contents:
            if notfirst==1:
               whichcolumn=row.index(variablename)
               notfirst+=1
            else:
               thelist.append(float(row[(whichcolumn)]))
        
    return np.array(thelist)    
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
    wr=csv.writer(runnumberfile,quoting=csv.QUOTE_ALL)
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
sensor_variables="TMAl_1.source"#-------------------------------------"sensor variable of interest"
folder_to_read_from="E://MovedFromD//CSV//TS1//MO1group_2363runs//setpoint"#--------------------------------------------"folder to access"
folder_to_read_from2="E://MovedFromD//CSV//TS1//MO1group_2363runs//current"#--------------------------------------------"folder to access"
folder_to_read_from3="E://MovedFromD//CSV//TS1//MO1group_2363runs//deviation"
path_to_save_list="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150525_unreal_percentage//TMAl_1_source_unreal_percentage_try.csv"#----------------------------"folder to save output to"
PhysMax=500

#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()

files_in_folder = os.listdir(folder_to_read_from) 
files_in_folder.sort(key=extract_serial_number)

event_list=[]
percentage_list=[]
for i in range(len(files_in_folder)):
    #--------------------------------------------------------------------------------file path name for single csv file
    
    temp_file_name=files_in_folder[i]    
    single_file_path=os.path.join(folder_to_read_from, temp_file_name)
    single_file_path2=os.path.join(folder_to_read_from2, temp_file_name.replace('-setpoint','-current'))
    single_file_path3=os.path.join(folder_to_read_from3, temp_file_name.replace('-setpoint','-deviation'))

    #--------------------------------------------------------------------------------prints serial number
    serial_number=extract_serial_number(files_in_folder[i])
    #print('Reading CSV file:',serial_number)

    #--------------------------------------------------------------------------------reads values from csv file of specified sensor variable
#    setpoint_values=read_single_variable_as_stringlist_csv(single_file_path,sensor_variables)
#    current_values=read_single_variable_as_stringlist_csv(single_file_path2,sensor_variables)
#    deviation_values=read_single_variable_as_stringlist_csv(single_file_path3,sensor_variables)
    
    All=pd.read_csv(single_file_path)
    setpoint_values=np.asarray(All[:][sensor_variables])
    
    All=pd.read_csv(single_file_path2)
    current_values=np.asarray(All[:][sensor_variables])
    
    All=pd.read_csv(single_file_path3)
    deviation_values=np.asarray(All[:][sensor_variables])
    
    data_length=len(setpoint_values) 
    
    calculated_deviation=current_values-setpoint_values    
    
    
    boolean_value=(abs(calculated_deviation-deviation_values*PhysMax/100)>1)
    
    percentage_list.append(sum(boolean_value)/data_length)
    #----------------------------------------------------------------------------------plots the values and saves as png file into designated folder    
     
write_array_to_csv(path_to_save_list,percentage_list)

print('RUN TIME: %.2f secs' % (time.time()-tstart))