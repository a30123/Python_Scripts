# -*- coding: utf-8 -*-
"""
Created on Fri Feb  6 09:25:44 2015

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
    import csv
    import numpy as np      
    
    thelist=[]
    
    with open(csvpathfilename,'rU') as csvfile:
        contents=csv.reader(csvfile)
        for row in contents:
            thelist.append(float(row[0]))
        
    return np.array(thelist)    
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
    
    
def plot_and_save_list_values(valuelist,pathname,figure_filename):
    complete_dirpath_to_save_figures=os.path.normpath(os.path.join(os.getcwd(),pathname))    
    ensure_dir(complete_dirpath_to_save_figures)
    figure_filename2=figure_filename.replace('.csv','.png')
    complete_path_to_save_figure=os.path.normpath(os.path.join(complete_dirpath_to_save_figures,figure_filename2))
    
       
    plt.plot(valuelist)
    plt.savefig(complete_path_to_save_figure)
    plt.clf()    
#######################################


#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################

#intialize "sensor variable of interest","folder to accesss", and "folder to save output to"
sensor_variable="TMAl_1.source"#-------------------------------------"sensor variable of interest"
folder_to_read_from="E://MovedFromD//CSV//TS1//MO1group_2363runs//current"#--------------------------------------------"folder to access"
folder_to_read_from2="E://MovedFromD//CSV//TS1//MO1group_2363runs//deviation"#--------------------------------------------"folder to access"
folder_to_read_from3="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150512_TMAl_reconstructed_error_manipulated//Ouput3//CSV"
path_to_save_csv="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150518_relative_manipulated_error//CSV"#----------------------------"folder to save output to"
PhysMax=500
#path_to_save_png="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150430_TMAl_1_source_relative_error//TMAl_relative_error_PNG"
#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################


files_in_folder = os.listdir(folder_to_read_from) 
files_in_folder.sort(key=extract_serial_number)

for i in range(len(files_in_folder)):
    #--------------------------------------------------------------------------------file path name for single csv file
    temp_file_name=files_in_folder[i]    
    single_current_file_path=os.path.join(folder_to_read_from, temp_file_name)
    single_deviation_file_path=os.path.join(folder_to_read_from2, temp_file_name.replace('-current','-deviation'))

    #--------------------------------------------------------------------------------prints serial number
    serial_number=extract_serial_number(files_in_folder[i])
    print('Reading CSV file:',serial_number)
    
    manipulated_error_filename=str(serial_number)+'_manipulated_error.csv'
    manipulated_error_file_path=os.path.join(folder_to_read_from3, manipulated_error_filename)

    #--------------------------------------------------------------------------------reads values from csv file of specified sensor variable
    current_values=read_single_variable_as_stringlist_csv(single_current_file_path, sensor_variable)
    deviation_values=read_single_variable_as_stringlist_csv(single_deviation_file_path, sensor_variable)        
    error_values=np.array(deviation_values*PhysMax/100,dtype='float16')
    reconstructed_setpoint=np.array(current_values-error_values)   
    
    manipulated_error_values=get_single_column_from_csv(manipulated_error_file_path)  
    
    relative_manipulated_error=np.divide(manipulated_error_values,reconstructed_setpoint)
    
    relative_manipulated_error_filename=str(serial_number)+'_relative_manipulated_error.csv'
    complete_path_to_save_csv=os.path.normpath(os.path.join(path_to_save_csv,relative_manipulated_error_filename))
  
    ensure_dir(path_to_save_csv)
    write_array_to_csv(complete_path_to_save_csv,relative_manipulated_error)
   
    #----------------------------------------------------------------------------------plots the values and saves as png file into designated folder    
    
#    ensure_dir(path_to_save_png)
#    plot_and_save_list_values(relative_error,path_to_save_png,relative_error_filename)
