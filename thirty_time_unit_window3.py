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
    extract_regular_expression=re.search('(^\d+_relative)',filename)
    serial_number_string=extract_regular_expression.group(0)
    serial_number_string=serial_number_string.replace('_relative','')
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

folder_to_read_from="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150518_relative_manipulated_error//CSV"#--------------------------------------------"folder to access"
#folder_to_read_from="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150518_five_consecutive_errors//Trial"
folder_to_read_category_from="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150511_TMAl_mean_reconstructed_error_segments//category_list"
window_size=30
percentage=0.5
accuracy=0.01

path_to_save_csv="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150518_five_consecutive_errors//relative_manipulated_error_thirty_time_unit_window.csv"#----------------------------"folder to save output to"
path_to_save_csv2="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150518_five_consecutive_errors//relative_manipulated_error_thirty_time_unit_window_number.csv"#----------------------------"folder to save output to"
path_to_save_csv3="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150518_five_consecutive_errors//relative_manipulated_error_thirty_time_unit_window_max.csv"#----------------------------"folder to save output to"

path_to_save_png="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150430_TMAl_1_source_relative_error//TMAl_relative_error_PNG"
#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################


files_in_folder = os.listdir(folder_to_read_from) 
files_in_folder.sort(key=extract_serial_number)

alarm_list=[]
alarm_count_list=[]
max_percentage_list=[]
for i in range(len(files_in_folder)):
    #--------------------------------------------------------------------------------file path name for single csv file
    temp_file_name=files_in_folder[i]    
    single_current_file_path=os.path.join(folder_to_read_from, temp_file_name)

    #--------------------------------------------------------------------------------prints serial number
    serial_number=extract_serial_number(files_in_folder[i])
    print('Reading CSV file:',serial_number)

    #--------------------------------------------------------------------------------reads values from csv file of specified sensor variable
    current_values=get_single_column_from_csv(single_current_file_path)
       
    
    
    temp_file_name2=str(serial_number)+'.csv' 
    single_file_path2=os.path.join(folder_to_read_category_from, temp_file_name2)
    
    category_values=get_single_column_from_csv(single_file_path2)
    
    yes_pick=(~(category_values==(-1)))
    filtered_values=current_values[yes_pick]
    run_length=len(filtered_values)  
    
    
    if run_length<window_size:
        alarm_list.append(0)
        alarm_count_list.append(0)
        max_percentage_list.append(0)
    else:
        sum_list=(filtered_values[0:(run_length-window_size+1)]>=accuracy)
        for i in range(window_size-1):
            sum_list=sum_list+(filtered_values[0+(i+1):(run_length-window_size+1+(i+1))]>=accuracy)
        
        no_of_alarms=sum((sum_list)>(percentage*window_size))
        max_percentage=max(sum_list)
        alarm_count_list.append(no_of_alarms)
        alarm_list.append((no_of_alarms>0)+0)
        max_percentage_list.append(max_percentage)



write_array_to_csv(path_to_save_csv,(alarm_list))
write_array_to_csv(path_to_save_csv2,alarm_count_list)
write_array_to_csv(path_to_save_csv3,alarm_count_list)
    #----------------------------------------------------------------------------------plots the values and saves as png file into designated folder    
    




