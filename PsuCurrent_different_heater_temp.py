# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15

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
def get_single_column_from_csv(csvpathfilename):
#    import csv
#    import numpy as np      
    
    thelist=[]
    
    with open(csvpathfilename,'rU') as csvfile:
        contents=csv.reader(csvfile)
        for row in contents:
            thelist.append(row[0])
        
    return np.array(thelist)    
#
#def read_single_variable_as_stringlist_csv(csvpathfilename, variablename):
##   import csv
##   import numpy as np      
#    
#    notfirst=1
#    thelist=[]
#    
#    with open(csvpathfilename,'rU') as csvfile:
#        contents=csv.reader(csvfile)
#        for row in contents:
#            if notfirst==1:
#               whichcolumn=row.index(variablename)
#               notfirst+=1
#            else:
#               thelist.append(float(row[(whichcolumn)]))
#        
#    return np.array(thelist)    
def extract_serial_number(filename):
#    import re
    extract_regular_expression=re.search('(_\d+-current)',filename)
    serial_number_string=extract_regular_expression.group(0)
    serial_number_string=serial_number_string.replace('-current','')
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
#sensor_variables="TMAl_1.source"#-------------------------------------"sensor variable of interest"
#folder_to_read_from="E://MovedFromD//CSV//TS1//MO1group_2363runs//setpoint"#--------------------------------------------"folder to access"
#folder_to_read_from2="E://MovedFromD//CSV//TS1//MO1group_2363runs//current"#--------------------------------------------"folder to access"
#folder_to_read_from3="E://MovedFromD//CSV//TS1//MO1group_2363runs//deviation"
#path_to_save_list="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150525_unreal_percentage//TMAl_1_source_unreal_percentage_try.csv"#----------------------------"folder to save output to"
#PhysMax=500


category_folder="E://Data//Processed//TS1//Segmentations//Heater_temp_20150815//CSV"
current_folder='E://Data//CSV//TS1//VoltageCurrent_2492runs//current//'
sensor_variable="Psu6Current"
path_to_save_list="E://Python scripts//Try_20150815_PsuCurrent_different_heater_temp//output//average_current.csv"

#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()

files_in_folder = os.listdir(current_folder) 
files_in_folder.sort(key=extract_serial_number)

no_of_runs=len(files_in_folder)

files_in_folder2 = os.listdir(category_folder)
extract_serial_short=lambda x: int(x.replace('.csv',''))
file2_numbers=np.asarray(list(map(extract_serial_short,files_in_folder2)))

event_list=[]
feature_list=["" for i in range(no_of_runs)]
#for i in range(3):
for i in range(len(files_in_folder)):
    #--------------------------------------------------------------------------------file path name for single csv file
    
    temp_file_name=files_in_folder[i]    
    serial_number=extract_serial_number(temp_file_name)    

    if (sum(file2_numbers==serial_number)==1):
        single_file_path=os.path.join(current_folder, temp_file_name)
        single_file_path2=os.path.join(category_folder, str(serial_number)+'.csv')
#    single_file_path3=os.path.join(folder_to_read_from3, temp_file_name.replace('-setpoint','-deviation'))

    #--------------------------------------------------------------------------------prints serial number
    
        print('Reading CSV file:',serial_number)

    #--------------------------------------------------------------------------------reads values from csv file of specified sensor variable
#    setpoint_values=read_single_variable_as_stringlist_csv(single_file_path,sensor_variables)
#    current_values=read_single_variable_as_stringlist_csv(single_file_path2,sensor_variables)
#    deviation_values=read_single_variable_as_stringlist_csv(single_file_path3,sensor_variables)
    
        All=pd.read_csv(single_file_path)
        current_values=np.asarray(All[:][sensor_variable])
    
        category_values=get_single_column_from_csv(single_file_path2)
        category_values_float=np.array(category_values,dtype='float16')
    
        yes_steep_ascending=(category_values_float==3)
        filtered_current=current_values[yes_steep_ascending]

        if (len(filtered_current)>1):
            feature_list[i]=np.mean(filtered_current)
        

    #----------------------------------------------------------------------------------plots the values and saves as png file into designated folder    
     
write_array_to_csv(path_to_save_list,feature_list)

print('RUN TIME: %.2f secs' % (time.time()-tstart))