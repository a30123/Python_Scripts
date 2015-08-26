# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 10:29:54 2015

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
import numpy as np
import os
from matplotlib import pyplot as plt
#########################################################################################################
#######################################   FUNCTIONS           ###########################################
#########################################################################################################
def get_single_column_from_csv(csvpathfilename):
    import csv
    import numpy as np      
    
    thelist=[]
    
    with open(csvpathfilename,'rU') as csvfile:
        contents=csv.reader(csvfile)
        for row in contents:
            thelist.append(float(row[0]))
        
    return np.array(thelist)    

#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
folder_to_read_from="C://Users//A30123.ITRI//Desktop//Tasks//FPC//data//sensor_csv"
figure_folder="C://Users//A30123.ITRI//Documents//Python Scripts//FPC//Try_20150826_plot_with_trip//output"
index_folder="C://Users//A30123.ITRI//Desktop//Tasks//FPC//Index//trip point//"
#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()
files_in_folder = os.listdir(folder_to_read_from)


single_file_path=os.path.join(folder_to_read_from,files_in_folder[0])
    
All_temp=pd.read_csv(single_file_path)

sensor_list=list(All_temp.columns.values)
sensor_list=sensor_list[1:len(sensor_list)]


All={0:0,1:0,2:0,3:0,4:0,5:0}
sensor_values={0:0,1:0,2:0,3:0,4:0,5:0}
trip_points={0:0,1:0,2:0,3:0,4:0,5:0}
no_of_runs=len(files_in_folder)



for i in range(len(files_in_folder)):
    single_file_path=os.path.join(folder_to_read_from,files_in_folder[i])
    single_file_path2=os.path.join(index_folder,files_in_folder[i])    
        
    All_temp=pd.read_csv(single_file_path)
    All_temp=All_temp.convert_objects(convert_numeric=True)
    All_temp[sensor_list]=All_temp[sensor_list].astype('float32')
    All[i]=All_temp
    
    
    temp_trip=get_single_column_from_csv(single_file_path2)
    trip_points[i]=np.array(temp_trip)



for j in range(4):#len(sensor_list)):
    for i in range(len(files_in_folder)):
        single_file_path=os.path.join(folder_to_read_from,files_in_folder[i])
        
        All_temp2=All[i]        
        sensor_values[i]=np.asarray(All_temp2[:][sensor_list[j]],dtype=np.float32)

    plot_x_limit=max((len(sensor_values[0]),len(sensor_values[1]),len(sensor_values[2]),len(sensor_values[3]),len(sensor_values[4]),len(sensor_values[5])))

    complete_path_to_save_figure=figure_folder+"//"+str(sensor_list[j])+".png"

    fig=plt.figure(figsize=(8.0, 5.0))
    
    ax1=fig.add_subplot(611)
    ax1.plot(list(range(len(sensor_values[0]))),sensor_values[0])
    ax1.fill_between(list(range(len(trip_points[0]))),min(sensor_values[0]),max(sensor_values[0]),where=trip_points[0]==1,facecolor='green',alpha=0.5)
    plt.grid(True)
    plt.tick_params(axis='x',which='both', bottom='off', top='off', labelbottom='off')
    plt.xlim((0,plot_x_limit))
    plt.yticks(np.arange(min(sensor_values[0]),2*max(sensor_values[0])-min(sensor_values[0]),max(sensor_values[0])-min(sensor_values[0])))
    
    ax2=fig.add_subplot(612)
    ax2.plot(list(range(len(sensor_values[1]))),sensor_values[1])
    plt.grid(True)
    plt.tick_params(axis='x',which='both', bottom='off', top='off', labelbottom='off')
    plt.xlim((0,plot_x_limit))
    plt.yticks(np.arange(min(sensor_values[1]),2*max(sensor_values[1])-min(sensor_values[1]),max(sensor_values[1])-min(sensor_values[1])))
   
    ax3=fig.add_subplot(613)
    ax3.plot(list(range(len(sensor_values[2]))),sensor_values[2])
    plt.grid(True)
    plt.tick_params(axis='x',which='both', bottom='off', top='off', labelbottom='off')
    plt.xlim((0,plot_x_limit))
    plt.yticks(np.arange(min(sensor_values[2]),2*max(sensor_values[2])-min(sensor_values[2]),max(sensor_values[2])-min(sensor_values[2])))
       
    
    ax4=fig.add_subplot(614)
    ax4.plot(list(range(len(sensor_values[3]))),sensor_values[3])
    plt.grid(True)
    plt.tick_params(axis='x',which='both', bottom='off', top='off', labelbottom='off')
    plt.xlim((0,plot_x_limit))
    plt.yticks(np.arange(min(sensor_values[3]),2*max(sensor_values[3])-min(sensor_values[3]),max(sensor_values[3])-min(sensor_values[3])))
       
    
    ax5=fig.add_subplot(615)
    ax5.plot(list(range(len(sensor_values[4]))),sensor_values[4])
    plt.grid(True)
    plt.tick_params(axis='x',which='both', bottom='off', top='off', labelbottom='off')
    plt.xlim((0,plot_x_limit))
    plt.yticks(np.arange(min(sensor_values[4]),2*max(sensor_values[4])-min(sensor_values[4]),max(sensor_values[4])-min(sensor_values[4])))
   
    
    ax6=fig.add_subplot(616)
    ax6.plot(list(range(len(sensor_values[5]))),sensor_values[5])
    plt.grid(True)
    plt.xlim((0,plot_x_limit))
    plt.yticks(np.arange(min(sensor_values[5]),2*max(sensor_values[5])-min(sensor_values[5]),max(sensor_values[5])-min(sensor_values[5])))
   
    
#    
    plt.show
    plt.savefig(complete_path_to_save_figure,dpi=200)
    plt.clf()
    
print('RUN TIME: %.2f secs' % (time.time()-tstart))

