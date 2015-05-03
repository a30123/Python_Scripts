# -*- coding: utf-8 -*-
"""
Created on Sun May  3 10:31:34 2015

@author: Mary
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
import os
import time
import csv
import numpy as np
import re
import math
import matplotlib.pyplot as plt

#########################################################################################################
#######################################   FUNCTIONS           ###########################################
#########################################################################################################

def read_variables_as_stringlists_csv(csvpathfilename, variablenames):
#    import csv
#    import numpy as np      
    
    notfirst=1
    thelist=[]
    
    with open(csvpathfilename,'rU') as csvfile:
        contents=csv.reader(csvfile)
        for row in contents:
            if notfirst==1:
               whichcolumn=[row.index(i) for i in variablenames]
               notfirst+=1
            else:
               thelist.append([row[j] for j in whichcolumn])
        
    return np.array(thelist)  
    
def write_array_to_csv(filename_path,listname):
#    import csv   
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
    
def ensure_dir(f):
#    import os
    d=os.path.abspath(f)
    if not os.path.exists(d):
        os.makedirs(d)

def extract_serial_number(filename):
#    import re
    extract_regular_expression=re.search('(_\d+-setpoint)',filename)
    serial_number_string=extract_regular_expression.group(0)
    serial_number_string=serial_number_string.replace('-setpoint','')
    serial_number_string=serial_number_string.replace('_','') 
    value_of_number=int(serial_number_string)
    return value_of_number
    
def zero_step(Step_list):
#    import numpy as np
    mm2=(Step_list==0)
    return_this=sum(mm2)
#    
#    nonzero_step=np.zeros((1,1))
#    if min(mm)==0:
#        zero_step=np.count_nonzero(mm==0)
#        if zero_step==len(mm):
#            zero_step=0
#    else:
#        nonzero_step=np.count_nonzero(mm==min(mm))
#        for i in range(len(mm)):
#            if mm[i]==min(mm):
#                zero_step=(i+1)-nonzero_step
                
    return (int(return_this))
    
#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
sensor_variables=['TMAl_1.source']#-------------------------------------"sensor variable of interest"
step_variable=['Step']
#setpoint_folder='C://Users//Mary//Music//Documents//Python Scripts//Try_20150503_setpoint_partition//setpoint'
setpoint_folder='E://Raw Data//CSV files//TS1_TMAl_Step//setpoint'
output_folder='C://Users//Mary//Music//Documents//Python Scripts//Try_20150503_setpoint_partition//Output'

#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################

tstart = time.time()

files_in_folder = os.listdir(setpoint_folder)
files_in_folder.sort(key=extract_serial_number) 

complete_dirpath_to_save_segmentlist=os.path.normpath(os.path.join(output_folder,"CSV"))    
ensure_dir(complete_dirpath_to_save_segmentlist)

complete_dirpath_to_save_figure=os.path.normpath(os.path.join(output_folder,"PNG"))    
ensure_dir(complete_dirpath_to_save_figure)

doesnotwork=[]
zero_step_list=[]
for u in range(len(files_in_folder)):
    single_file_path=os.path.join(setpoint_folder, files_in_folder[u])
   
    try:
        serial_number=extract_serial_number(files_in_folder[u])
        print(serial_number)
        
        All_variables=read_variables_as_stringlists_csv(single_file_path,["TMAl_1.source","Step"])
        AA=np.array([[float(k)] for k in All_variables[:,0]])
        mmm=np.array([[int(kk)] for kk in All_variables[:,1]])   
        
        Zero_Step=zero_step(mmm)
        zero_step_list.append(Zero_Step)
        
    except ValueError:
        print('No valid StepLabel in this run!!!')
        doesnotwork.append(u)
    
    print('-----------------------------------------')
