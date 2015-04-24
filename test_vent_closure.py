# -*- coding: utf-8 -*-
"""
Created on Fri Feb  6 09:25:44 2015

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
import os #-------------------------------------------------------Miscellaneous operating system interfaces
import numpy as np #----------------------------------------------array manipulation, scientific computing
import csv#-------------------------------------------------------read write csv files
import matplotlib.pyplot as plt  #--------------------------------John Hunter's  2D plotting library
import re #-------------------------------------------------------regular expressions
from matplotlib import rc 
############################################################################################################



#########################################################################################################
#######################################   FUNCTIONS           ###########################################
#########################################################################################################


#####################################
#reference:    http://stackoverflow.com/questions/273192/check-if-a-directory-exists-and-create-it-if-necessary     
def ensure_dir(f):
#    import os
    d=os.path.abspath(f)
    if not os.path.exists(d):
        os.makedirs(d)
   

def read_single_variable_as_stringlist_csv(csvpathfilename, variablename):
#   import csv
#   import numpy as np      
    
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
    extract_regular_expression=re.search('(_\d+-setpoint)',filename)
    serial_number_string=extract_regular_expression.group(0)
    serial_number_string=serial_number_string.replace('-setpoint','')
    serial_number_string=serial_number_string.replace('_','') 
    value_of_number=int(serial_number_string)
    return value_of_number
#######################################


#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################

#intialize "sensor variable of interest","folder to accesss", and "folder to save output to"
sensor_variables="Vent.vac"#-------------------------------------"sensor variable of interest"
folder_to_read_from="E://MovedFromD//CSV//TS1//Vac_2363runs//setpoint"#--------------------------------------------"folder to access"
path_to_save_csv="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150424_test_Vent_closure//"#----------------------------"folder to save output to"
filename1="VentVacLastSwitchType.csv"
filename2="VentVacLastSwitchTypeLabel.csv"
#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################


files_in_folder = os.listdir(folder_to_read_from) 
files_in_folder.sort(key=extract_serial_number)
vent_vac_type_list=[]
vent_vac_type_list_label=[]
for i in range(len(files_in_folder)):
    #--------------------------------------------------------------------------------file path name for single csv file
    
    temp_file_name=files_in_folder[i]    
    single_file_path=os.path.join(folder_to_read_from, temp_file_name)

    #--------------------------------------------------------------------------------prints serial number
    serial_number=extract_serial_number(files_in_folder[i])
    print('Reading CSV file:',serial_number)

    #--------------------------------------------------------------------------------reads values from csv file of specified sensor variable
    values_read_from_file=read_single_variable_as_stringlist_csv(single_file_path,sensor_variables)
     
    
    diff_values_from_file=values_read_from_file[1:]-values_read_from_file[:-1]    
    
    yes_no_negative_one=(diff_values_from_file==(-1))
    yes_no_one=(diff_values_from_file==1)
    if ((sum(yes_no_negative_one)>0)|(sum(yes_no_one)>0)):
        just_increments=np.array(range(len(diff_values_from_file)))
        if (sum(yes_no_negative_one)>0):
            position_of_negative_ones=just_increments[yes_no_negative_one]
            last_negative_one=max(position_of_negative_ones) 
        else:
            last_negative_one=0
            
        if (sum(yes_no_one)>0):
            position_of_ones=just_increments[yes_no_one]
            last_one=max(position_of_ones) 
        else:
            last_one=0
            
            
        if(last_one<last_negative_one):
            vent_vac_type_list.append("last close")
            vent_vac_type_list_label.append(-1)
        else:
            vent_vac_type_list.append("last open")
            vent_vac_type_list_label.append(1)
    else:
        vent_vac_type_list.append("no switch")
        vent_vac_type_list_label.append(0)
    
     
write_array_to_csv(path_to_save_csv+filename1,vent_vac_type_list)
write_array_to_csv(path_to_save_csv+filename2,vent_vac_type_list_label)