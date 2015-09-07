# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 11:19:24 2015

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
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#########################################################################################################
#######################################   FUNCTIONS           ###########################################
#########################################################################################################


#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
people=('Tom','Dick','Harry','Slim','Jim')
figure_folder="C://Users//A30123.ITRI//Documents//Python Scripts//FPC//Try_20150907_evaluate_discrimination//output"
folder_path="C://Users//A30123.ITRI//Documents//Python Scripts//FPC//Try_20150907_evaluate_discrimination//mean//"
#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()
single_file_path=folder_path+"slide window-7350MAbr(20110329).csv"
All_temp=pd.read_csv(single_file_path,header=None)
sensor_list=list(All_temp.columns.values)
sensor_list=sensor_list[1:len(sensor_list)]
 
All_temp=All_temp.convert_objects(convert_numeric=True)
All_temp=All_temp[:][sensor_list].astype('float32')
feature_matrix=np.asarray(All_temp)

distance_value=10

y_pos=np.arange(len(people))
performance=distance_value*np.ones(len(people))

plt.barh(y_pos,performance,align='center',color='DarkOliveGreen',alpha=0.4)
plt.yticks(y_pos,people)
plt.xlabel('Bhattacharyya distance')
plt.title('How fast do you want to go today')


complete_path_to_save_figure=figure_folder+"//"+"try.png"


plt.show
plt.savefig(complete_path_to_save_figure,dpi=200)
plt.clf()




print('RUN TIME: %.2f secs' % (time.time()-tstart))

