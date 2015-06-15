# -*- coding: utf-8 -*-
"""
Created on Mon Jun  11 16:32:36 2015

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
import statistics
import scipy.stats

#########################################################################################################
#######################################   FUNCTIONS           ###########################################
#########################################################################################################

def get_single_column_from_csv(csvpathfilename):
    import csv
    import numpy as np      
    
    thelist=[]
    
    with open(csvpathfilename,'rU') as csvfile:
        contents=csv.reader(csvfile)
        for row in contents:
            thelist.append(float(row[0]))
        
    return np.array(thelist)   
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


    
def get_positions(list_name,value_in_list):
#    import numpy as np    
    increments=np.array(range(len(list_name)))
    yes_equals_value=(list_name==value_in_list)
    return_this=increments[yes_equals_value]
    
    return return_this
#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
directory_filename="E://all_bonus_features"
label_index_filename="C://Users//A30123.ITRI//Desktop//Tasks//Variable Selection//index//Events//replacement_points.csv"
output_directory_filename="E://all_cummulative_features//"

#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()

files_in_folder = os.listdir(directory_filename) 
replacement_labels=get_single_column_from_csv(label_index_filename)


for filename in files_in_folder:
    cummulative_value_list=[]
    cummulative_value=0
    complete_file_path=os.path.join(directory_filename, filename)
    original_feature_values=get_single_column_from_csv(complete_file_path)
    
    
    print(filename)
    for i in range(len(replacement_labels)):
        if(replacement_labels[i]==1):
            cummulative_value=original_feature_values[i]
        else:
            cummulative_value=cummulative_value+original_feature_values[i]
        cummulative_value_list.append(cummulative_value)
            
    figure_filename=filename.replace(".csv","")
    write_array_to_csv(os.path.join(output_directory_filename, figure_filename+"_cummulative.csv"),cummulative_value_list)

    