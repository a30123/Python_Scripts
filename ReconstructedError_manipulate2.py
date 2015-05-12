# -*- coding: utf-8 -*-
"""
Created on Mon May  4 13:16:54 2015

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
import os
import csv
import numpy as np
import re
#import math
import matplotlib.pyplot as plt
#########################################################################################################
#######################################   FUNCTIONS           ###########################################
#########################################################################################################
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
def write_array_to_csv(filename_path,listname):
    import csv
     
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
    
def extract_serial_number(filename):
#    import re
    extract_regular_expression=re.search('(^\d+_reconstructed)',filename)
    serial_number_string=extract_regular_expression.group(0)
    serial_number_string=serial_number_string.replace('_reconstructed','')
 
    value_of_number=int(serial_number_string)
    return value_of_number
    
def get_positions(list_name,value_in_list):
    increments=np.array(range(len(list_name)))
    yes_equals_value=(list_name==value_in_list)
    return_this=increments[yes_equals_value]
    
    return return_this
    
        
def plot_and_save_list_values(valuelist,pathname,figure_filename):
    complete_dirpath_to_save_figures=os.path.normpath(os.path.join(os.getcwd(),pathname))    
    ensure_dir(complete_dirpath_to_save_figures)
    figure_filename2=figure_filename.replace('.csv','.png')
    complete_path_to_save_figure=os.path.normpath(os.path.join(complete_dirpath_to_save_figures,figure_filename2))
    
       
    plt.plot(valuelist)
    plt.savefig(complete_path_to_save_figure)
    plt.clf()   
#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
#folder_to_read_from="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150504_TMAl_source_mean_reconstructed_error//setpoint"
#folder_to_read_from="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150504_TMAl_1_source_reconstructed_error//TMAl_reconstructed_error_CSV"
#folder_to_read_from2="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150504_TMAl_source_setpoint_partition_rewritten//Output//CSV"
#output_folder_filename="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150504_TMAl_source_mean_reconstructed_error//mean_reconstructed_error_flat_region.csv"
folder_to_read_from="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150504_TMAl_1_source_reconstructed_error//TMAl_reconstructed_error_CSV"
folder_to_read_from2="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150511_TMAl_mean_reconstructed_error_segments//category_list"
path_to_save_csv="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150512_TMAl_reconstructed_error_manipulated//Ouput2//CSV"
path_to_save_png="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150512_TMAl_reconstructed_error_manipulated//Ouput2//PNG"

adjust_by={1:5,2:5,3:5,4:0,5:0,6:0}
#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()
files_in_folder = os.listdir(folder_to_read_from) 
files_in_folder.sort(key=extract_serial_number)
mean_reconstructed_error_list=[]
for i in range(len(files_in_folder)):
    temp_file_name=files_in_folder[i]   
    serial_number=extract_serial_number(files_in_folder[i])
    temp_file_name2=str(serial_number)+'.csv'    
    print(temp_file_name)
    single_file_path=os.path.join(folder_to_read_from, temp_file_name)
    single_file_path2=os.path.join(folder_to_read_from2, temp_file_name2)
 
    reconstructed_error_values=get_single_column_from_csv(single_file_path)
    category_values=get_single_column_from_csv(single_file_path2)
    category_values_float=np.array(category_values,dtype='float16')
    reconstructed_error_float=abs(np.array(reconstructed_error_values,dtype='float16'))
       
    new_error_float=reconstructed_error_float
    
    for ii in range(1,5):
        the_positions=get_positions(category_values_float,ii)
        for cc in the_positions:
            if(reconstructed_error_float[cc]>adjust_by[ii]):
                new_error_float[cc]=reconstructed_error_float[cc]-adjust_by[ii]          
                
    manipulate_error_filename=str(serial_number)+'_manipulated_error.csv'
    complete_path_to_save_csv=os.path.normpath(os.path.join(path_to_save_csv,manipulate_error_filename))
  
    ensure_dir(path_to_save_csv)
    ensure_dir(path_to_save_png)
    write_array_to_csv(complete_path_to_save_csv,new_error_float)        
    plot_and_save_list_values(new_error_float,path_to_save_png,manipulate_error_filename)


print('RUN TIME: %.2f secs' % (time.time()-tstart))

