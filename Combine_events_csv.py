# -*- coding: utf-8 -*-
"""
Created on Sun Mar 08 12:59:42 2015

@author: A30123
modified date: Mar 13 2015
description: Program for combining multiple events from seperate csv files. Combines arbitrary number of events.
"""

########################################################################################################
###      #####  #####        #####       ###############    #   ###  ###       ###       ###############
###  #########  ########  ########  ####################  #  #  ###  ###  ###  ###  ###  ###############
###  #########  ########  ########  ####################  ####  ###  ###  ###  ###  ###  ###############
###      #####  ########  ########       ###############  ####  ###  ###       ###       ###############
########################################################################################################

########################################################################################################
#######################################  IMPORT LIBRARIES     ##########################################
########################################################################################################
import time
import os
import numpy as np
import csv

########################################################################################################
#######################################   FUNCTIONS           ##########################################
########################################################################################################
def get_single_column_from_csv(csvpathfilename):
#    import csv
#    import numpy as np      
    
    thelist=[]
    
    with open(csvpathfilename,'rU') as csvfile:
        contents=csv.reader(csvfile)
        for row in contents:
            thelist.append(row[0])
        
    return np.array(thelist)    
    
##this function writes a list or an numpy array into (a) column(s) in csv
def write_array_to_csv(filename_path,listname):
#    import csv
     
    runnumberfile=open(filename_path,'w',newline='')
    wr=csv.writer(runnumberfile,quoting=csv.QUOTE_ALL)
    if type(listname)==list:
        for item in listname:
            wr.writerow([item])
    elif type(listname)==np.ndarray:
        for item in listname:
            wr.writerow(item)
    else:
        print("the structure you are writing is neither a list nor an np.ndarray")
		
    runnumberfile.close()
    


########################################################################################################
#######################################   INITIALIZING        ##########################################
########################################################################################################
folder_to_read_from="C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150308_combine_events//where_I_put_the_files"
runindex_filename="run_index.csv"
output_filename="output.csv"

########################################################################################################
#######################################   MAIN PROGRAM      # ##########################################
########################################################################################################
tstart = time.time()

complete_dirpath_to_read_runindexlist=os.path.normpath(os.path.join(folder_to_read_from,runindex_filename))
complete_dirpath_to_write=os.path.normpath(os.path.join(folder_to_read_from,output_filename))
complete_dirpath_to_event_folder=os.path.normpath(os.path.join(folder_to_read_from,"just events"))

files_in_folder = os.listdir(complete_dirpath_to_event_folder)

runindex_list=get_single_column_from_csv(complete_dirpath_to_read_runindexlist)

number_of_events=len(files_in_folder)
length_of_list=len(runindex_list)

emptyarray=np.array(["" for x in range(number_of_events)],dtype=object)
final_matrix=np.array([emptyarray for x in range(length_of_list+1)],dtype=object)


for i in range(number_of_events):
    complete_dirpath_to_read_eventlist=os.path.normpath(os.path.join(complete_dirpath_to_event_folder,files_in_folder[i]))
    temp_event_list=get_single_column_from_csv(complete_dirpath_to_read_eventlist)
    
    zero_one,inverse_indices=np.unique(temp_event_list,return_inverse=True)
    labels=np.array(["",(number_of_events-i)],dtype=object)  
    final_matrix[-length_of_list:,i]=labels[inverse_indices]
    final_matrix[0,i]=files_in_folder[i].replace(".csv","")
    
    
final_matrix=np.column_stack((np.concatenate((np.array(["step increments"]),np.array(range(length_of_list)))),final_matrix))
final_matrix=np.column_stack((np.concatenate((np.array(["run index"]),runindex_list)),final_matrix))



write_array_to_csv(complete_dirpath_to_write,final_matrix)

print('RUN TIME: %.2f secs' % (time.time()-tstart))
