# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 13:24:16 2015

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
import time

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
#####################################


#####################################    
#HCKu's code for retrieving variable values
def get_variables_from_csv(csvpathfilename, listofvariablename):
#    import csv
#    import numpy as np      
    
    reader = csv.reader(open(csvpathfilename, 'r'), delimiter=',')
    tempArr = np.array(list(reader))
    tags = tempArr[0,:]
        
    variablearrays=np.zeros((np.shape(tempArr)[0] - 1, np.shape(np.array(listofvariablename))[0]))
    for j in range(0, np.shape(np.array(listofvariablename))[0]):
        for i in range(0,np.shape(tempArr)[1]):
            if tags[i] == np.array(listofvariablename)[j]:
                variablearrays[0:, j] = tempArr[1:, i].astype('float')
        
    return variablearrays    
######################################


######################################
def extract_serial_number(filename):
#    import re
    extract_regular_expression=re.search('(_\d+-setpoint)',filename)
    serial_number_string=extract_regular_expression.group(0)
    serial_number_string=serial_number_string.replace('-setpoint','')
    serial_number_string=serial_number_string.replace('_','') 
    value_of_number=int(serial_number_string)
    return value_of_number
#######################################
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

#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
sensor_variables=["TMGa_1.run"]#-------------------------------------"sensor variable of interest"
folder_to_read_from="E://MovedFromD//CSV//TS1//MO1group_line_run_2363runs//setpoint//"#--------------------------------------------"folder to access"
path_to_save_figures="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150327_RunSwitches//PNG"#----------------------------"folder to save output to"
path_to_save_csv_files="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150327_RunSwitches//CSV"#----------------------------"folder to save output to"

#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()



files_in_folder = os.listdir(folder_to_read_from) 
files_in_folder.sort(key=extract_serial_number)


length_between_switches_list=[]
yes_no_freq_switch_region_list=[]
for i in range(len(files_in_folder)):
    #--------------------------------------------------------------------------------file path name for single csv file
    single_file_path=os.path.join(folder_to_read_from, files_in_folder[i])

    #--------------------------------------------------------------------------------prints serial number
    print('Reading CSV file:',extract_serial_number(files_in_folder[i]))

    #--------------------------------------------------------------------------------reads values from csv file of specified sensor variable
    run_list=get_variables_from_csv(single_file_path,sensor_variables)
   
    diff_run_list=run_list[1:]-run_list[:-1]  
    
    no_of_switch_points=len(np.nonzero(diff_run_list)[0])
    
    yes_no_freq_switch_region=np.zeros(len(run_list))
    
    if (no_of_switch_points>5):
                
        
        switch_points=np.zeros(no_of_switch_points+2)
        switch_points[1:-1]=np.nonzero(diff_run_list)[0]
        switch_points[-1]=(len(run_list)-1)
        switch_points[0]=0

        length_between_switch_points=switch_points[1:]-switch_points[:-1]
        length_between_switches_list.append(length_between_switch_points)
        
       
        
        types_of_lengths, counts=np.unique(length_between_switch_points,return_counts=True)
        
        
        if max(counts)>5:           
            yes_no_freq_switch=(counts==max(counts)) 
            just_increments=np.array(range(len(counts)))
            position_of_freq_switch=just_increments[yes_no_freq_switch]

            counts2=counts
            
            #temp_run_list=get_variables_from_csv(single_file_path,sensor_variables)
            lower_bound=[]
            upper_bound=[]
            x=0
            while (x==0):#(max(counts2)>5)and (no_of_switch_points>5)):
                one_length=types_of_lengths[position_of_freq_switch[0]]

                just_increments2=np.array(range(len(length_between_switch_points)))
                its_that_length=(length_between_switch_points<one_length+20)*(length_between_switch_points>one_length-20)
                positions_of_that_length=just_increments2[its_that_length]
            
                no_of_positions=len(positions_of_that_length)
                position_now=0
                flag=True
 
                while (position_now<no_of_positions and flag):
                    position_to_start_with=positions_of_that_length[position_now]
                    moving_position=position_to_start_with
                    position_to_add=1
                    other_length=length_between_switch_points[positions_of_that_length[position_now]+1]
                    compare_length=length_between_switch_points[positions_of_that_length[position_now]+1]
                    while (sum(positions_of_that_length==(moving_position+2))>0 and other_length+20>compare_length and other_length-20<compare_length):
                        moving_position=moving_position+2
                        position_to_add=position_to_add+1
                        compare_length=length_between_switch_points[positions_of_that_length[position_now+position_to_add-1]+1]
                        
                    if(position_to_add>5):
                        flag=False
                    else:
                        position_now=position_now+position_to_add
                        temp_lower_bound=switch_points[position_to_start_with]    
                        temp_upper_bound=switch_points[moving_position+1]
                        #temp_run_list[temp_lower_bound:temp_upper_bound]=np.zeros((temp_upper_bound-temp_lower_bound,1))
                
                if flag==False:
                    lower_bound=switch_points[position_to_start_with]    
                    upper_bound=switch_points[moving_position+1]
                    #temp_run_list[lower_bound:upper_bound]=np.zeros((upper_bound-lower_bound,1))
                    yes_no_freq_switch_region[lower_bound:upper_bound]=np.ones(upper_bound-lower_bound)
                else:
                    lower_bound=0
                    upper_bound=0.01
                   
                    
                x=1
                              
            
        else:
            
            lower_bound=0
            upper_bound=0.01
    else:
        length_between_switches_list.append("less than 5 switches")
        lower_bound=0
        upper_bound=0.01
    
    ##Save CSV
    figure_filename3=str(extract_serial_number(files_in_folder[i]))+'.csv'
    complete_path_to_save_csv=os.path.normpath(os.path.join(path_to_save_csv_files,figure_filename3))
    write_array_to_csv(complete_path_to_save_csv,yes_no_freq_switch_region)

    
    ###MAke figure    
    plt.figure(figsize=(10,6))
    plt.plot(run_list)
    plt.axvspan(lower_bound, upper_bound, facecolor='darkgoldenrod', alpha=0.8)
    
   # figure_filename2=files_in_folder[i].replace('.csv','.png')
    figure_filename2=str(extract_serial_number(files_in_folder[i]))+'.png'
    complete_path_to_save_figure=os.path.normpath(os.path.join(path_to_save_figures,figure_filename2))
    plt.xlim(0,len(run_list))
    plt.grid()
    plt.xlabel("Time(s)",fontsize=16)
    plt.ylabel("Setpoint",fontsize=16) 
    for tick in plt.gca().xaxis.get_major_ticks():
        tick.label1.set_fontsize(12) 
    for tick in plt.gca().yaxis.get_major_ticks():
        tick.label1.set_fontsize(12) 
        
    plt.savefig(complete_path_to_save_figure)
    plt.clf()    

write_array_to_csv("C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150327_RunSwitches//TMGa_1_lengths_between_switches.csv",length_between_switches_list)


print('RUN TIME: %.2f secs' % (time.time()-tstart))