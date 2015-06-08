# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 10:22:58 2015

@author: A30123
description:
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
import re
import csv
import numpy as np      
import pandas as pd 
#########################################################################################################
#######################################   FUNCTIONS           ###########################################
#########################################################################################################
def extract_serial_number2(filename):
#    import re
    extract_regular_expression=re.search('(_\d+-current)',filename)
    serial_number_string=extract_regular_expression.group(0)
    serial_number_string=serial_number_string.replace('-current','')
    serial_number_string=serial_number_string.replace('_','') 
    value_of_number=int(serial_number_string)
    return value_of_number
    
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
               thelist.append(row[(whichcolumn)].strip())
        
    return np.array(thelist)  
    
def write_array_to_csv(filename_path,listname):
    import csv
     
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
current_folder="E://TS1_all_variables//current"
InSitu_variable_file_path="C://Users//A30123.ITRI//Desktop//Tasks//Variable Selection//variable lists//In situ variables.csv"
other_non_sensor_variables=np.array(['DataTime','Step','StepLabel','FilterConsumption'])
output_filename="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150608_find_trivial_variables//nontrivial variables.csv"
#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()
files_in_folder = os.listdir(current_folder) 
files_in_folder.sort(key=extract_serial_number2)

single_file_path=os.path.join(current_folder,files_in_folder[1])
All=pd.read_csv(single_file_path)
variable_list=list(All.columns.values)
in_situ_variable_list=read_single_variable_as_stringlist_csv(InSitu_variable_file_path,"In situ")

insitu_removed_variable_list=[v for v in variable_list if (sum(in_situ_variable_list==v)==0)]
sensor_variable_list=[v for v in insitu_removed_variable_list if (sum(other_non_sensor_variables==v)==0)]

exclude_list=[]
same=1
for variable in sensor_variable_list:
    
    
    print(variable)
    single_file_path=os.path.join(current_folder,files_in_folder[0])
    variable_values=read_single_variable_as_float_csv(single_file_path,variable)
    value_now=variable_values[0]    
    i=0
    while((same==1) & (i<len(files_in_folder))):
        print(i)        
        single_file_path=os.path.join(current_folder,files_in_folder[i])
        variable_values=read_single_variable_as_float_csv(single_file_path,variable)
        j=0
        while( (same==1) & (j<len(variable_values))):
            if(value_now==variable_values[j]):
                j=(j+1)
            else:
                same=0
                exclude_list.append(variable)
            
        i=i+1

    same=1
write_array_to_csv(output_filename,exclude_list)
print('RUN TIME: %.2f secs' % (time.time()-tstart))
