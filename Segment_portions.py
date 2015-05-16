# -*- coding: utf-8 -*-
"""
Created on Mon May  16 13:16:54 2015

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
    extract_regular_expression=re.search('(^\d+.csv)',filename)
    serial_number_string=extract_regular_expression.group(0)
    serial_number_string=serial_number_string.replace('.csv','')
 
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
folder_to_read_from2="C://Users//Mary//Music//Documents//Python Scripts//Try_20150516_portion_of_each_segment//TS1_TMAl_category_list"
path_to_save_csv="C://Users//Mary//Music//Documents//Python Scripts//Try_20150516_portion_of_each_segment//output.csv"

#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()
files_in_folder = os.listdir(folder_to_read_from2) 
files_in_folder.sort(key=extract_serial_number)
category_proportion_list=[]
for i in range(len(files_in_folder)):
    temp_file_name2=files_in_folder[i]   
    
    print(temp_file_name2)
    single_file_path2=os.path.join(folder_to_read_from2, temp_file_name2)
 
    category_values=get_single_column_from_csv(single_file_path2)
    category_values_float=np.array(category_values,dtype='float16')
          
    run_length=(len(category_values))   
    temp_list=[]
    for ii in range(1,7):
        yes_no_category=(category_values_float==ii)
        temp_list.append(sum(yes_no_category)/run_length)
                 
    
    category_proportion_list.append(temp_list)            
    
    save_this_array=np.array(category_proportion_list)
    
    
write_array_to_csv(path_to_save_csv,save_this_array)        
   

print('RUN TIME: %.2f secs' % (time.time()-tstart))

