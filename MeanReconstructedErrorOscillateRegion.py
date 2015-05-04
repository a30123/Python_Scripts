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
#import matplotlib.pyplot as plt
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
#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
folder_to_read_from="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150504_TMAl_1_source_reconstructed_error//TMAl_reconstructed_error_CSV"
folder_to_read_from2="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150504_TMAl_source_setpoint_partition_rewritten//Output//CSV"
output_folder_filename="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150504_TMAl_source_mean_reconstructed_error//mean_reconstructed_error_oscillate_region.csv"
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
    
    oscillate_region_occurrence=(category_values_float==1)    
    
    if (sum(oscillate_region_occurrence)!=0):
        reconstructed_error_float=abs(np.array(reconstructed_error_values,dtype='float16'))
        reconstructed_error_to_consider=reconstructed_error_float[oscillate_region_occurrence]
        
        mean_reconstructed_error_float=np.mean(reconstructed_error_to_consider)
        mean_reconstructed_error_list.append(mean_reconstructed_error_float)
    else:
        mean_reconstructed_error_list.append(-0.5)


write_array_to_csv(output_folder_filename,mean_reconstructed_error_list)


print('RUN TIME: %.2f secs' % (time.time()-tstart))

