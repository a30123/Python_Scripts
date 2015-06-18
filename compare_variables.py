# -*- coding: utf-8 -*-
"""
Created on Wed Jun  15 09:11:42 2015

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
    
def get_single_column_from_csv(csvpathfilename):
#    import csv
#    import numpy as np      
    
    thelist=[]
    
    with open(csvpathfilename,'rU') as csvfile:
        contents=csv.reader(csvfile)
        for row in contents:
            thelist.append(row[0])
        
    return np.array(thelist)  
    
    
#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
#sensor_variable="dP_Filter"
directory_filename="C://Users//A30123.ITRI//Desktop//Tasks//Variable Selection//variable lists//nontrivial variables.csv"
directory_filename2="C://Users//A30123.ITRI//Desktop//Tasks//Variable Selection//variable lists//digital_analog_combined.csv"
variable_file_path="C://Users//A30123.ITRI//Desktop//Tasks//Variable Selection//removedvariablelist6.csv"
output_directory_filename="E://all_variable_features//"

#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()

list1=get_single_column_from_csv(directory_filename)
list2=get_single_column_from_csv(directory_filename2)

for i in range(len(list1)):
    
    if(sum(list2==list1[i])==0):
        print(list1[i])
    

for i in range(len(list2)):
    
    if(sum(list1==list2[i])==0):
        print(list2[i])
        