# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 16:32:36 2015

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
def read_single_variable_as_stringlist_csv(csvpathfilename, variablename):
#    import csv
#    import numpy as np      
    
    notfirst=1
    thelist=[]
    
    with open(csvpathfilename,'rU') as csvfile:
        contents=csv.reader(csvfile)
        for row in contents:
            if notfirst==1:
               whichcolumn=row.index(variablename)
               notfirst+=1
            else:
               thelist.append((row[(whichcolumn)]))
        
    return np.array(thelist)    

def read_single_variable_as_float_csv(csvpathfilename, variablename):
#    import csv
#    import numpy as np      
    
    notfirst=1
    thelist=[]
    
    with open(csvpathfilename,'rU') as csvfile:
        contents=csv.reader(csvfile)
        for row in contents:
            if notfirst==1:
               whichcolumn=row.index(variablename)
               notfirst+=1
            else:
               thelist.append(float(row[(whichcolumn)]))
        
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
#directory_filename="E://TS1_all_variables//current"
directory_filename="E://MovedFromD//CSV//TS1//HydrideAndReactorPress_2492runs//current"
variable_file_path="C://Users//A30123.ITRI//Desktop//Tasks//Variable Selection//variable lists//removedvariablelist28.csv"
output_directory_filename="E://all_variable_features//"

#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()

files_in_folder = os.listdir(directory_filename) 
files_in_folder.sort(key=extract_serial_number)


variable_list=read_single_variable_as_stringlist_csv(variable_file_path,"x")
    
for sensor_variable in variable_list:
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    list5=[]
    list6=[]
    print(sensor_variable)
    for i in range(len(files_in_folder)):
        temp_file_name=files_in_folder[i]
        print(i)
        complete_file_path=os.path.join(directory_filename, temp_file_name)
        
        current_values=read_single_variable_as_float_csv(complete_file_path,sensor_variable)
        
        list1.append(np.mean(current_values))
        list2.append(np.var(current_values))
        list3.append(max(current_values))
        list4.append(min(current_values))
        list5.append(statistics.median(current_values))
        #list6.append((max(current_values)-min(current_values)))
    write_array_to_csv(os.path.join(output_directory_filename, "Feature_"+sensor_variable+"_mean.csv"),list1)
    write_array_to_csv(os.path.join(output_directory_filename, "Feature_"+sensor_variable+"_variance.csv"),list2)
    write_array_to_csv(os.path.join(output_directory_filename, "Feature_"+sensor_variable+"_max.csv"),list3)
    write_array_to_csv(os.path.join(output_directory_filename, "Feature_"+sensor_variable+"_min.csv"),list4)
    write_array_to_csv(os.path.join(output_directory_filename, "Feature_"+sensor_variable+"_median.csv"),list5)
    #write_array_to_csv(os.path.join(output_directory_filename, "Feature_"+sensor_variable+"_range.csv"),list6)

    