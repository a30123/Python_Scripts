# -*- coding: utf-8 -*-
"""
Created on Mon May 18 13:25:42 2015

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
    
 
def extract_serial_number(filename):
#    import re
    extract_regular_expression=re.search('(^\d+_current)',filename)
    serial_number_string=extract_regular_expression.group(0)
    serial_number_string=serial_number_string.replace('_current','')
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
folder_to_read_from="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150518_TMAl_1_source_unreal_relative_error//TMAl_unreal_relative_error_CSV"#--------------------------------------------"folder to access"
#folder_to_read_from="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150518_five_consecutive_errors//Trial"
how_many_consecutive=6
accuracy=0.01

path_to_save_csv="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150518_five_consecutive_errors//unreal_relative_error_five_consecutive.csv"#----------------------------"folder to save output to"
path_to_save_csv2="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150518_five_consecutive_errors//unreal_relative_error_five_consecutive_number.csv"#----------------------------"folder to save output to"

path_to_save_png="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150430_TMAl_1_source_relative_error//TMAl_relative_error_PNG"
#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################


files_in_folder = os.listdir(folder_to_read_from) 
files_in_folder.sort(key=extract_serial_number)

alarm_list=[]
alarm_count_list=[]

for i in range(len(files_in_folder)):
    #--------------------------------------------------------------------------------file path name for single csv file
    temp_file_name=files_in_folder[i]    
    single_current_file_path=os.path.join(folder_to_read_from, temp_file_name)

    #--------------------------------------------------------------------------------prints serial number
    serial_number=extract_serial_number(files_in_folder[i])
    print('Reading CSV file:',serial_number)

    #--------------------------------------------------------------------------------reads values from csv file of specified sensor variable
    current_values=get_single_column_from_csv(single_current_file_path)
    run_length=len(current_values)    
    
    
    if run_length<how_many_consecutive:
        alarm_list.append(0)
        alarm_count_list.append(0)
    else:
        yes_no_list=(current_values[0:(run_length-how_many_consecutive+1)]>=accuracy)
        for i in range(how_many_consecutive-1):
            yes_no_list=np.multiply(yes_no_list,(current_values[0+(i+1):(run_length-how_many_consecutive+1+(i+1))]>=accuracy))
        
        no_of_alarms=sum(yes_no_list)
        alarm_count_list.append(no_of_alarms)
        alarm_list.append((no_of_alarms>0)+0)



write_array_to_csv(path_to_save_csv,(alarm_list))
write_array_to_csv(path_to_save_csv2,alarm_count_list)
    #----------------------------------------------------------------------------------plots the values and saves as png file into designated folder    
    




