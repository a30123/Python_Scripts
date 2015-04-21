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
   
def plot_and_save_list_values(valuelist,pathname,figure_filename):
#    import matplotlib.pyplot as plt  #--------------------------------John Hunter's  2D plotting library

    complete_dirpath_to_save_figures=os.path.normpath(os.path.join(os.getcwd(),pathname))    
    ensure_dir(complete_dirpath_to_save_figures)
    figure_filename2=figure_filename.replace('.csv','.png')
    complete_path_to_save_figure=os.path.normpath(os.path.join(complete_dirpath_to_save_figures,figure_filename2))
    
       
    plt.plot(valuelist)
    plt.savefig(complete_path_to_save_figure)
    plt.clf()
    

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
               thelist.append(row[(whichcolumn)])
        
    return np.array(thelist)    
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
path_to_save_figures="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150421_VentVac_switch//Output"#----------------------------"folder to save output to"


#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################


files_in_folder = os.listdir(folder_to_read_from) 
files_in_folder.sort(key=extract_serial_number)

for i in range(len(files_in_folder)):
    #--------------------------------------------------------------------------------file path name for single csv file
    single_file_path=os.path.join(folder_to_read_from, files_in_folder[i])

    #--------------------------------------------------------------------------------prints serial number
    serial_number=extract_serial_number(files_in_folder[i])
    print('Reading CSV file:',serial_number)

    #--------------------------------------------------------------------------------reads values from csv file of specified sensor variable
    values_read_from_file=read_single_variable_as_stringlist_csv(single_file_path,sensor_variables)
    
    #----------------------------------------------------------------------------------plots the values and saves as png file into designated folder    
    plot_and_save_list_values(values_read_from_file,path_to_save_figures,str(serial_number)+".csv")
    #plot_and_save_list_values(values_read_from_file,path_to_save_figures,files_in_folder[i])
    

