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
#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
folder_to_read_from="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150430_TMAl_1_source_relative_error//TMAl_source_relative_error_CSV"
output_folder_filename="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150504_feature_mean_relative_error//mean_relative_error.csv"
#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()
files_in_folder = os.listdir(folder_to_read_from) 

mean_relative_error_list=[]
for i in range(len(files_in_folder)):
    temp_file_name=files_in_folder[i]    
    print(temp_file_name)
    single_file_path=os.path.join(folder_to_read_from, temp_file_name)
 
    relative_error_values=get_single_column_from_csv(single_file_path)
    
    relative_error_float=np.array(relative_error_values,dtype='float16')
    mean_relative_error_float=np.mean(relative_error_float)
 
    mean_relative_error_list.append(mean_relative_error_float)


write_array_to_csv(output_folder_filename,mean_relative_error_list)


print('RUN TIME: %.2f secs' % (time.time()-tstart))

