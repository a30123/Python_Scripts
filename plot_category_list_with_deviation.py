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
from matplotlib import rc 

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
def extract_serial_number3(filename):
#    import re
    extract_regular_expression=re.search('(_\d+-deviation)',filename)
    serial_number_string=extract_regular_expression.group(0)
    serial_number_string=serial_number_string.replace('-deviation','')
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
sensor_variable=["TMAl_1.source"]
category_folder="C://Users//Mary//Music//Documents//Python Scripts//Try_20150510_category_plot_with_deviation//category_files"
setpoint_folder="C://Users//Mary//Music//Documents//Python Scripts//Try_20150510_category_plot_with_deviation//setpoint"
deviation_folder="C://Users//Mary//Music//Documents//Python Scripts//Try_20150510_category_plot_with_deviation//deviation"
output_folder="C://Users//Mary//Music//Documents//Python Scripts//Try_20150510_category_plot_with_deviation//Output"
PhysMax=500
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


files_in_folder3=os.listdir(deviation_folder)
serial_number_list2=np.array([extract_serial_number3(uu) for uu in files_in_folder3])

mean_reconstructed_error_list=[]
for i in range(len(files_in_folder)):
    temp_file_name=files_in_folder[i] 
    print(temp_file_name)  
    serial_number=extract_serial_number2(files_in_folder[i])
    yes_serial_number=(serial_number_list==serial_number) 
    yes_serial_number2=(serial_number_list2==serial_number)    
   
    increment=np.array(range(len(files_in_folder2)))
    position_of_serial_number=increment[yes_serial_number]
    position_of_serial_number2=increment[yes_serial_number2]
    
    
    temp_file_name2=files_in_folder2[position_of_serial_number]    
    temp_file_name3=files_in_folder3[position_of_serial_number2]    
    
    single_file_path=os.path.join(category_folder, temp_file_name)
    setpoint_file_path=os.path.join(setpoint_folder, temp_file_name2)
    deviation_file_path=os.path.join(deviation_folder, temp_file_name3)

 
    category_values=get_single_column_from_csv(single_file_path)
    setpoint_values=read_variables_as_stringlists_csv(setpoint_file_path,sensor_variable)
    deviation_values=read_variables_as_stringlists_csv(deviation_file_path,sensor_variable)
    category_values_float=np.array(category_values,dtype='float16')
    setpoint_values_float=np.array(setpoint_values,dtype='float16')
    deviation_values_float=abs(np.array(deviation_values,dtype='float16'))*PhysMax/100
    
    CC=np.array([[float(k)] for k in category_values])
    CC_difference=(CC[1:]-CC[:-1]) 
    choo=np.concatenate((np.array([[1]]),CC_difference,np.array([[1]])))
    boo=~(choo==0)
    increment2=np.array(range(len(CC)+1))
    doo=increment2[boo[:,0]]
    
    segment_points=doo#np.concatenate((np.array([0]),doo))
    segment_points[-1]=(len(setpoint_values)-1)
    
    
    rc('mathtext',default='regular')    
    
    
    figure_filename2=str(serial_number)+'.png'
    complete_path_to_save_figure=os.path.normpath(os.path.join(complete_dirpath_to_save_figure,figure_filename2))
    
    x_axis_range=np.arange(0,len(setpoint_values))
    sub_valuelist=setpoint_values_float
    sub_valuelist2=deviation_values_float
    
    
    fig=plt.figure(figsize=(14,6))
    ax=fig.add_subplot(111)
        
    lns1=ax.plot(x_axis_range,sub_valuelist,'-',label='TMAl_1.source setpoint')
    for ji in range((len(segment_points)-1)):
        lltemp=segment_points[ji]
        rrtemp=segment_points[ji+1]
        color_is=colors[int((int(float(category_values[lltemp]))))]
        plt.axvspan(lltemp,rrtemp, facecolor=color_is, alpha=0.8)
        
    ax2=ax.twinx()
    lns3=ax2.plot(x_axis_range,sub_valuelist2,'-r',label='TMAl_1.source reconstructed error')
    
    lns=lns1+lns3
    labs=[l.get_label() for l in lns]
    ax.legend(lns,labs,loc=0)
    
    ax.grid()
    ax.set_xlabel("time")
    ax.set_ylabel(r"setpoint")
    ax2.set_ylabel(r"reconstructed error")
    ax2.set_ylim(0,10)
    ax.set_ylim(0,500)    

    plt.show
    plt.savefig(complete_path_to_save_figure)
    plt.clf()

print('RUN TIME: %.2f secs' % (time.time()-tstart))


