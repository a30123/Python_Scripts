# -*- coding: utf-8 -*-
"""
created on Thu Apr 23 14:41:01 2015

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




#########################################################################################################
#######################################   FUNCTIONS           ###########################################
#########################################################################################################
############################################################################################################

#####################################
#reference:    http://stackoverflow.com/questions/273192/check-if-a-directory-exists-and-create-it-if-necessary     
def ensure_dir(f):
#    import os
    d=os.path.abspath(f)
    if not os.path.exists(d):
        os.makedirs(d)
     
def plot_and_save_list_values(valuelist,pathname,figure_filename):
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
               thelist.append(float(row[(whichcolumn)]))
        
    return np.array(thelist) 


#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
sensor_variables="TMAl_1.source"#-------------------------------------"sensor variable of interest"
folder_to_read_from="Input_files//Test"
path_to_save_figures="Output//value_plots"


#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################


folder_path=os.path.normpath(os.path.join(os.getcwd(),folder_to_read_from))
files_in_folder = os.listdir(folder_path) 


for i in range(len(files_in_folder)):
    single_file_path=os.path.join(folder_to_read_from, files_in_folder[i])
    
    print('Reading CSV file:',files_in_folder[i])

    values_read_from_file=read_single_variable_as_stringlist_csv(single_file_path,sensor_variables)
    
    plot_and_save_list_values(values_read_from_file,path_to_save_figures,files_in_folder[i])
    

