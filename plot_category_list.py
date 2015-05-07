# -*- coding: utf-8 -*-
"""
Created on Tue May  5 09:25:21 2015

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
import matplotlib.pyplot as plt
#import matplotlib.colors
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
def extract_serial_number2(filename):
#    import re
    extract_regular_expression=re.search('(^\d+.csv)',filename)
    serial_number_string=extract_regular_expression.group(0)
    serial_number_string=serial_number_string.replace('.csv','')
 
    value_of_number=int(serial_number_string)
    return value_of_number
def extract_serial_number(filename):
#    import re
    extract_regular_expression=re.search('(_\d+-setpoint)',filename)
    serial_number_string=extract_regular_expression.group(0)
    serial_number_string=serial_number_string.replace('-setpoint','')
    serial_number_string=serial_number_string.replace('_','') 
    value_of_number=int(serial_number_string)
    return value_of_number    
   
def ensure_dir(f):
#    import os
    d=os.path.abspath(f)
    if not os.path.exists(d):
        os.makedirs(d)   

#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
#category_folder="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150505_plot_category_list//setpoint"
#category_folder='C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150507_TMAl_source_setpoint_partition_rewritten_improved2//Output//CSV'
category_folder='C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150507_TMAl_source_setpoint_partition_rewritten_improved2//Trial//CSV'
#category_folder="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150506_TMAl_source_setpoint_partition_rewritten_improved//Output//CSV"
setpoint_folder="E://MovedFromD//CSV//TS1//MO1group_2363runs//setpoint"
sensor_variable=["TMAl_1.source"]
#output_folder="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150505_plot_category_list//Output4"
output_folder="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150505_plot_category_list//Trial"

#colors=['b','','g','r','y','c','m','k']
colors={-1:'b',0:'g',1:'g',2:'r',3:'y',4:'c',5:'m',6:'k'}
#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()
complete_dirpath_to_save_figure=os.path.normpath(os.path.join(output_folder,"PNG"))    
ensure_dir(complete_dirpath_to_save_figure)

files_in_folder = os.listdir(category_folder) 
files_in_folder.sort(key=extract_serial_number2)

files_in_folder2=os.listdir(setpoint_folder)
serial_number_list=np.array([extract_serial_number(uu) for uu in files_in_folder2])

mean_reconstructed_error_list=[]
for i in range(len(files_in_folder)):
    temp_file_name=files_in_folder[i] 
    print(temp_file_name)  
    serial_number=extract_serial_number2(files_in_folder[i])
    yes_serial_number=(serial_number_list==serial_number)    
    increment=np.array(range(len(files_in_folder2)))
    position_of_serial_number=increment[yes_serial_number]
    
    temp_file_name2=files_in_folder2[position_of_serial_number]    
    
    single_file_path=os.path.join(category_folder, temp_file_name)
    setpoint_file_path=os.path.join(setpoint_folder, temp_file_name2)
 
    category_values=get_single_column_from_csv(single_file_path)
    setpoint_values=read_variables_as_stringlists_csv(setpoint_file_path,sensor_variable)
    category_values_float=np.array(category_values,dtype='float16')
    
    
    CC=np.array([[float(k)] for k in category_values])
    CC_difference=(CC[1:]-CC[:-1]) 
    choo=np.concatenate((np.array([[1]]),CC_difference,np.array([[1]])))
    boo=~(choo==0)
    increment2=np.array(range(len(CC)+1))
    doo=increment2[boo[:,0]]
    
    segment_points=doo#np.concatenate((np.array([0]),doo))

    
    plt.figure(figsize=(14,6))
    plt.plot(setpoint_values)    
    

    
    for ji in range((len(segment_points)-1)):
        ll=segment_points[ji]
        rr=segment_points[ji+1]
        color_is=colors[int((int(float(category_values[ll]))))]
        plt.axvspan(ll-0.5,rr-0.5, facecolor=color_is, alpha=0.8)
        
    figure_filename=str(serial_number)+'.png'
    complete_path_to_save_figure=os.path.normpath(os.path.join(complete_dirpath_to_save_figure,figure_filename))
    
   
    
    plt.xlim(0,len(setpoint_values)-1)
    plt.grid()
    plt.xlabel("Time(s)",fontsize=16)
    plt.ylabel("Setpoint",fontsize=16) 
    for tick in plt.gca().xaxis.get_major_ticks():
        tick.label1.set_fontsize(12) 
    for tick in plt.gca().yaxis.get_major_ticks():
        tick.label1.set_fontsize(12) 
    plt.savefig(complete_path_to_save_figure)
    plt.clf()    
        
        

    


print('RUN TIME: %.2f secs' % (time.time()-tstart))


