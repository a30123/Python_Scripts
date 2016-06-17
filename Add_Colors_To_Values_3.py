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
# reads numerical list without header from csv file using csv.reader  
def get_single_column_from_csv(csvpathfilename):
#    import csv
#    import numpy as np      
    thelist=[]
    with open(csvpathfilename,'rU') as csvfile:
        contents = csv.reader(csvfile)
        for row in contents:
            thelist.append(row[0])
    return np.array(thelist)   
    
    
##this function writes a list or an numpy array into (a) column(s) in csv
def write_array_to_csv(filename_path, listname):
    ''' writes a list or an array to a csv file
    
    Parameters
    ----------
    
    filename_path : str, path and filename of the csv file to save list or array
    
    listname: a list or an np.ndarray 

    '''
#    import csv 
    with open(filename_path, 'w', newline='') as csvfile:
        wr = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
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


#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
category_csv_folder_name = "put_category_file_here"
value_csv_folder_name = "put_value_file_here"
category_names_csv_folder_name = "category_names"
output_filename = "output.csv"



#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
folder_to_read_from = folder_to_read_from = os.path.normpath(os.path.join(os.getcwd(),".."))
complete_dir_path_category_folder = os.path.normpath(os.path.join(folder_to_read_from,category_csv_folder_name))
complete_dir_path_value_folder = os.path.normpath(os.path.join(folder_to_read_from,value_csv_folder_name))
complete_dir_path_category_names_folder = os.path.normpath(os.path.join(folder_to_read_from, category_names_csv_folder_name))

category_csv_filename = os.listdir(complete_dir_path_category_folder)[0]
value_csv_filename = os.listdir(complete_dir_path_value_folder)[0]
category_names_csv_filename = os.listdir(complete_dir_path_category_names_folder)
complete_dirpath_to_read_categorylist = os.path.normpath(os.path.join(complete_dir_path_category_folder,category_csv_filename))
complete_dirpath_to_read_valuelist = os.path.normpath(os.path.join(complete_dir_path_value_folder,value_csv_filename))
complete_dirpath_to_write = os.path.normpath(os.path.join(folder_to_read_from,output_filename))


category_list = get_single_column_from_csv(complete_dirpath_to_read_categorylist)
value_list = get_single_column_from_csv(complete_dirpath_to_read_valuelist)

categories,inverse_indices = np.unique(category_list,return_inverse=True)

no_of_categories=len(categories)
length_of_list=len(category_list)

emptyarray=np.array(["" for x in range(no_of_categories)],dtype=object)
final_matrix=np.array([emptyarray for x in range(length_of_list)],dtype=object)

for i in range(length_of_list):
    final_matrix[i,inverse_indices[i]] = value_list[i]
 
if (category_names_csv_filename != []):
    complete_dirpath_to_read_categorynames = os.path.normpath(os.path.join(complete_dir_path_category_names_folder, category_names_csv_filename[0]))
    category_names = get_single_column_from_csv(complete_dirpath_to_read_categorynames)   
    integer_strings = list(map(str, (range(1,len(category_names)+1))))
    dict_of_category_names = dict(zip(integer_strings,category_names))
    reordered_category_names = [dict_of_category_names[key] for key in category_list]
    
    final_matrix = np.vstack((category_names,final_matrix))
else:
    renamed_category_names = ['category_'+key for key in categories]
    final_matrix = np.vstack((renamed_category_names,final_matrix))
    
final_matrix = np.column_stack((np.concatenate((np.array(["step increments"]),np.array(range(length_of_list)))),final_matrix))

write_array_to_csv(complete_dirpath_to_write,final_matrix)

