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
import pandas as pd
#########################################################################################################
#######################################   FUNCTIONS           ###########################################
#########################################################################################################
#
#def read_variables_as_stringlists_csv(csvpathfilename, variablenames):
##    import csv
##    import numpy as np      
#    
#    notfirst=1
#    thelist=[]
#    
#    with open(csvpathfilename,'rU') as csvfile:
#        contents=csv.reader(csvfile)
#        for row in contents:
#            if notfirst==1:
#               whichcolumn=[row.index(i) for i in variablenames]
#               notfirst+=1
#            else:
#               thelist.append([row[j] for j in whichcolumn])
#        
#    return np.array(thelist)  
    
def write_array_to_csv(filename_path,listname):
#    import csv   
    runnumberfile=open(filename_path,'w',newline='')
    wr=csv.writer(runnumberfile,quoting=csv.QUOTE_MINIMAL)
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
#Step_list is a column array
#    import numpy as np

    zeros_in_step_list=(Step_list==0)
    return_this=sum(zeros_in_step_list)
    #handling cases where step does not start with zero
    if(return_this==0):
        step_list_difference=(Step_list[1:]-Step_list[:-1])
        negatives_in_differences=(step_list_difference<0)
        increments=np.array(range(1,len(Step_list)+1)) 
        #handling csaes where step does not start with zero and loops in step exists
        if(sum(negatives_in_differences)>1):
            negatives_in_differences=(step_list_difference<-3)
        
        if(sum(negatives_in_differences)>0):
            return_this=min(increments[negatives_in_differences[:,0]])
               
    return (int(return_this))
    
def extract_intervals(True_False_List):
    output_array=[]
    increment=np.array(range(len(True_False_List)))
       
    positions_of_change=increment[~True_False_List[:,0]]
    
    all_positions_considered=np.concatenate((np.array([-1],dtype=np.int),positions_of_change,np.array([len(True_False_List)],dtype=np.int)))         
    
    constant_durations=all_positions_considered[1:]-all_positions_considered[:-1]
    position2=np.concatenate((np.array([0]),np.cumsum(constant_durations)))           
            
    
    long_enough_duration=(constant_durations>1)
    loop_no=sum(long_enough_duration)
    
    if(loop_no>0):
        increment3=np.array(range(len(constant_durations)))
        list3=increment3[long_enough_duration]                
        
        for jiji in list3:
            ll=position2[jiji]
            rr=position2[jiji+1]
            output_array.append([ll,rr])            
    
    return(output_array)
#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
sensor_variable='Heater.temp'#-------------------------------------"sensor variable of interest"
step_variable='Step'
setpoint_folder='E://Data//CSV//TS1//BLAHtemp_2492runs//setpoint'
#setpoint_folder='E://Test_Heater_temp_partitioning//setpoint'
output_folder='E://Data//Processed//TS1//Segmentations//Heater_temp_20150815'
#output_folder='E://Test_Heater_temp_partitioning//partition_output'
#output_filename='C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150508_TMAl_source_setpoint_partition_rewritten_improved4//intermediate.csv'
#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################

tstart = time.time()

files_in_folder = os.listdir(setpoint_folder)
files_in_folder.sort(key=extract_serial_number) 

complete_dirpath_to_save_segmentlist=os.path.normpath(os.path.join(output_folder,"CSV"))    
ensure_dir(complete_dirpath_to_save_segmentlist)


doesnotwork=[]

for u in range(len(files_in_folder)):
    single_file_path=os.path.join(setpoint_folder, files_in_folder[u])
    serial_number=extract_serial_number(files_in_folder[u])
    print(serial_number)
    
#    All_variables=read_variables_as_stringlists_csv(single_file_path,[sensor_variable,step_variable])
#    AA=np.array([[float(k)] for k in All_variables[:,0]])
#    mm=np.array([[int(kk)] for kk in All_variables[:,1]])   

    All=pd.read_csv(single_file_path)
    AA=(np.asarray([All[:][sensor_variable]]))
    mm=(np.asarray([All[:][step_variable]]))
    
    AA=AA.transpose()
    mm=mm.transpose()    
    
    data_length=len(AA)
    category_list=np.zeros((data_length,1))
    
               
    try:
        Zero_Step=zero_step(mm)
        
        adjusted_length=data_length-Zero_Step
        substantial_amount=data_length/700
        increment_1=np.array(range(adjusted_length))
        increment_2=np.array(range(data_length))
        
        if Zero_Step!=data_length:
            
            # category -1
            if Zero_Step!=0:
                category_list[:Zero_Step]=(-1)*np.ones((Zero_Step,1))
                AAA=AA[Zero_Step:]
                mmm=mm[Zero_Step:]
            else:
                AAA=AA[:]
                mmm=mm[:]
            
            # difference 
            AAA_difference=(AAA[1:]-AAA[:-1])    
            mmm_difference=(mmm[1:]-mmm[:-1])
            
            # category 4 (flat region)            
            no_change_steps=(AAA_difference==0)
            flat_intervals=extract_intervals(no_change_steps)
            for jj in flat_intervals:
                if ((jj[1]-jj[0])>substantial_amount):
                    category_list[jj[0]+Zero_Step:jj[1]+Zero_Step]=4*np.ones((jj[1]-jj[0],1),dtype=np.int)
            
            
            #write_array_to_csv(output_filename,category_list) 
            # category 1 (fluctuating region)  
            yes_negative_three=((mmm_difference<-1)&(mmm_difference>-50))
            if (sum(yes_negative_three)[0]>0):
                indices_negative_three=increment_1[yes_negative_three[:,0]]
                ttt=mmm[indices_negative_three]
                ttt2=mmm[indices_negative_three+1]
                sss,ss=np.unique(ttt,return_inverse=True)
                ss_difference=((ss[1:]-ss[:-1])==1)
                increment5=np.array(range(1,len(mmm)+1))
                indices_2=np.concatenate((np.array([0]),increment5[ss_difference]))
                for jjj in range(len(sss)):
                    yes_loop_end=(mm[:,0]==sss[jjj])
                    yes_loop_start=(mm[:,0]==ttt2[indices_2[jjj]][0])
                    rr=max(increment_2[yes_loop_end])
                    ll=min(increment_2[yes_loop_start])
                    sum_of_abs_diff=sum(abs(AAA_difference[ll+Zero_Step:rr+Zero_Step,0]))
                    std_of_value=np.std((AAA[ll+Zero_Step:rr+Zero_Step,0]))        
                    range_of_value=max((AAA[ll+Zero_Step:rr+Zero_Step,0]))-min((AAA[ll+Zero_Step:rr+Zero_Step,0]))

#                    if((len(np.unique(category_list[ll:rr]))!=1)& (std_of_value>0.2*range_of_value)):
#                        category_list[ll:rr]=np.ones((rr-ll,1),dtype=np.int)
#
#                  
                    if((std_of_value>0.2*range_of_value)&(sum_of_abs_diff>1)):
                        category_list[ll:rr]=np.ones((rr-ll,1),dtype=np.int)
                          
            # other categories
            category_difference=(category_list[1:]-category_list[:-1])
            no_change_steps2=((category_list[:-1]==0)*(category_difference==0))
            no_change_steps3=((no_change_steps2*(np.concatenate((np.zeros((Zero_Step,1)),mmm_difference))==0)))
            remaining_intervals=extract_intervals(no_change_steps3)

            
            for jkjk in remaining_intervals:
                if(jkjk[1]==data_length):
                    rr=jkjk[1]-1
                else:
                    rr=jkjk[1]
                    
                ll=jkjk[0]
                    
                if ((AA[rr]-AA[ll])>0):
                    if (((AA[rr]-AA[ll])/(rr-ll))>0.1):
                        label_int=int(3)
                    else:
                        label_int=int(5)
                else:
                    if (((AA[rr]-AA[ll])/(rr-ll))<-0.1):
                        label_int=int(2)
                    else:
                        label_int=int(6)
                category_list[ll:rr]=label_int*np.ones((rr-ll,1),dtype=np.int)
        
        else:            #if all step are zero value
            category_list=(-1)*np.ones((data_length,1))

        segment_filename=str(serial_number)+'.csv'
        complete_path_to_save_segmentlist=os.path.normpath(os.path.join(complete_dirpath_to_save_segmentlist,segment_filename))
        write_array_to_csv(complete_path_to_save_segmentlist,category_list) 
      
    except ValueError:
        print('No valid StepLabel in this run!!!')
        doesnotwork.append(u)
    
    print('-------------')
    

print('segement partition failed for the following runs:', doesnotwork)      
