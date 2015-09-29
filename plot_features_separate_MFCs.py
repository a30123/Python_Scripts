# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 15:27:10 2015

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
import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
#########################################################################################################
#######################################   FUNCTIONS           ###########################################
#########################################################################################################
def ensure_dir(f):
#    import os
    d=os.path.abspath(f)
    if not os.path.exists(d):
        os.makedirs(d)

#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
output_folder_name="output_figs"
#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()

current_directory=os.getcwd()

files_in_current_directory=os.listdir(path=current_directory)

reg_search_list=[re.search('(^\w+\.)csv',k) for k in files_in_current_directory]
csv_file=[l.group(0) for l in reg_search_list if l!=None]

output_folder_path=os.path.join(current_directory,output_folder_name)
for i in range(len(csv_file)):
    file_name=csv_file[i]
    output_subfolder_path=os.path.join(output_folder_path,file_name.replace('.csv','_figs'))
    ensure_dir(output_subfolder_path)
    feature_data_frame=pd.read_csv(file_name)   
    MFC_names=feature_data_frame[feature_data_frame.columns[0]]
    run_names=feature_data_frame.columns[1:]
    
    for j in range(len(MFC_names)):
        MFC_name=MFC_names[j]
        figure_filename=os.path.join(output_subfolder_path,MFC_name+'.png')
        feature_values=feature_data_frame.loc[j,run_names]
        ts=pd.Series(feature_values,index=run_names)
        plt.figure(figsize=(14,6))
        ts.plot(marker=".",markersize=14)        
        plt.ylim(3*min(feature_values)/2-max(feature_values)/2,3*max(feature_values)/2-min(feature_values)/2)
        plt.title(MFC_name+" "+file_name,fontsize=20)
        plt.xlabel("run no.",fontsize=16)
        plt.ylabel("feature values",fontsize=16)
        for k in range(len(run_names)):
            plt.text(k,feature_values[k],str(feature_values[k]))
        plt.savefig(figure_filename)
        plt.clf()
print('RUN TIME: %.2f secs' % (time.time()-tstart))

