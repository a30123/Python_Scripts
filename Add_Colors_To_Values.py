# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 10:16:24 2015

@author: A30123

description: Program for seperating values from csv file into features in different columns of csv file under the category list given
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
import numpy as np
import csv


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
    
    
##this function writes a list or an numpy array into (a) column(s) in csv
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


#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
folder_to_read_from=folder_to_read_from=os.path.join(os.getcwd(),"..","value_and_category_files_here")
category_csv_filename="run0830_6 inch Si.SL.AlN_SLs Buffer_Si_016-11_6 inch Si.SL.AlN_SLs Buffer_Si_016-11_846-segment.csv"
value_csv_filename="run0830_6 inch Si.SL.AlN_SLs Buffer_Si_016-11_6 inch Si.SL.AlN_SLs Buffer_Si_016-11_846-setpoint.csv"
output_filename="output.csv"



#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
complete_dirpath_to_read_categorylist=os.path.normpath(os.path.join(folder_to_read_from,category_csv_filename))
complete_dirpath_to_read_valuelist=os.path.normpath(os.path.join(folder_to_read_from,value_csv_filename))
complete_dirpath_to_write=os.path.normpath(os.path.join(folder_to_read_from,"..",output_filename))


category_list=get_single_column_from_csv(complete_dirpath_to_read_categorylist)
value_list=get_single_column_from_csv(complete_dirpath_to_read_valuelist)

categories,inverse_indices=np.unique(category_list,return_inverse=True)

no_of_categories=len(categories)
length_of_list=len(category_list)

emptyarray=np.array(["" for x in range(no_of_categories)],dtype=object)
final_matrix=np.array([emptyarray for x in range(length_of_list)],dtype=object)

for i in range(length_of_list):
    final_matrix[i,inverse_indices[i]]=value_list[i]
    
final_matrix=np.column_stack((np.array(range(length_of_list)),final_matrix))

write_array_to_csv(complete_dirpath_to_write,final_matrix)