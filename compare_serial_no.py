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
#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
#sensor_variable="dP_Filter"
directory_filename2="E://TS1_all_variables//current"
directory_filename="E://MovedFromD//CSV//TS1//MFC_2492runs//current"
variable_file_path="C://Users//A30123.ITRI//Desktop//Tasks//Variable Selection//removedvariablelist6.csv"
output_directory_filename="E://all_variable_features//"

#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()

files_in_folder = os.listdir(directory_filename) 
files_in_folder.sort(key=extract_serial_number)

files_in_folder2 = os.listdir(directory_filename2) 
files_in_folder2.sort(key=extract_serial_number)
ji="kk"
for i in range(len(files_in_folder)):
    serial_number1=extract_serial_number(files_in_folder[i])
    serial_number2=extract_serial_number(files_in_folder2[i])
    print(serial_number1)
    print(serial_number2)
    print(not(serial_number1==serial_number2))
    if((not(serial_number1==serial_number2))&(ji=="kk")):
        ji=files_in_folder[i]
    
    