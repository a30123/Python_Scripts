# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 09:11:42 2015

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


#########################################################################################################
#######################################   FUNCTIONS           ###########################################
#########################################################################################################
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
#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
#sensor_variable="dP_Filter"
directory_filename2="E://TS1_all_variables//current"
directory_filename="E://MovedFromD//CSV//TS1//MFC_2492runs//current"
variable_file_path="C://Users//A30123.ITRI//Desktop//Tasks//Variable Selection//removedvariablelist6.csv"
output_directory_filename="E://Serial_number_2492runs.csv"

#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()

files_in_folder = os.listdir(directory_filename) 
files_in_folder.sort(key=extract_serial_number)


ji=[]
for i in range(len(files_in_folder)):
    serial_number1=extract_serial_number(files_in_folder[i])
    ji.append(serial_number1)
    
write_array_to_csv(output_directory_filename,ji)    