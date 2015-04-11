# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 10:53:31 2015

@author: A30330
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
import math
import matplotlib.pyplot as plt 
#########################################################################################################
#######################################   FUNCTIONS           ###########################################
#########################################################################################################

def get_variable_from_csv(csvpathfilename, listofvariablename):
    reader = csv.reader(open(csvpathfilename, 'r'), delimiter=',')
    tempArr = np.array(list(reader))
    tags = tempArr[0,:]
        
    variablearrays=np.zeros((np.shape(tempArr)[0] - 1, np.shape(np.array(listofvariablename))[0]))
    for j in range(0, np.shape(np.array(listofvariablename))[0]):
        for i in range(0,np.shape(tempArr)[1]):
            if tags[i] == np.array(listofvariablename)[j]:
                variablearrays[0:, j] = tempArr[1:, i].astype('float')
        
    return variablearrays    

def get_variable_from_csv_alternative(csvpathfilename, listofvariablename):       
    notfirst=1
    thelist=[]
    
    with open(csvpathfilename,'rU') as csvfile:
        contents=csv.reader(csvfile)
        for row in contents:
            if notfirst==1:
               whichcolumn=row.index(listofvariablename)
               notfirst+=1
            else:
               thelist.append(row[(whichcolumn)])
        
    return np.array(thelist)
    
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
    
def ensure_dir(f):
#    import os
    d=os.path.abspath(f)
    if not os.path.exists(d):
        os.makedirs(d)

def extract_serial_number(filename):
#    import re
    extract_regular_expression=re.search('(_\d+-setpoint)',filename)
    serial_number_string=extract_regular_expression.group(0)
    serial_number_string=serial_number_string.replace('-','')
    serial_number_string=serial_number_string.replace('_','') 
    value_of_number=int(serial_number_string)
    return value_of_number

def adjusted_length(step_steplabel_file_path):
#    import numpy as np    
    xxx=get_variable_from_csv_alternative(single_file_path, 'StepLabel')
    mmm=np.zeros((np.shape(xxx)[0],1))
    mmmm=np.zeros((np.shape(xxx)[0],1))
        
    for i in range(len(mmm)):
        mmm[i]=xxx[i].split(".")[0]
        try:
            mmmm[i]=xxx[i].split(".")[1]
        except:
            mmmm[i]=0
        
    zero_step=0
    for i in range(len(mmm)-1):
        if mmm[i]>mmm[i+1]:
            zero_step=(i+1)
            break
        elif mmm[i]==mmm[i+1] and mmmm[i]>mmmm[i+1]:
            zero_step=(i+1)
            break
                
    return ((len(xxx)-int(zero_step))), mmm
    
#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################

#sensor_variables=['TMAl_1.source']#-------------------------------------"sensor variable of interest"
#setpoint_folder='E://MovedFromD//CSV//TS1//MO1group_2363runs//setpoint'
sensor_variables=['Heater.temp']
setpoint_folder='E://MovedFromD//CSV//TS1//Heater_2363runs//setpoint'
output_folder='C://Users//A30123.ITRI//Documents//Python Scripts//New_for_event_mining//Try_20150411_HCKu_20150409_heater'

#setpoint_folder='D://HCKu//TMAlgroup//setpoint'
#output_folder='D://HCKu//TMAlgroup//Output'
#serial_number=1491
#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################

tstart = time.time()

files_in_folder = os.listdir(setpoint_folder) 

complete_dirpath_to_save_segmentlist=os.path.normpath(os.path.join(output_folder,"CSV"))    
ensure_dir(complete_dirpath_to_save_segmentlist)

complete_dirpath_to_save_figure=os.path.normpath(os.path.join(output_folder,"FIG"))    
ensure_dir(complete_dirpath_to_save_figure)

doesnotwork=[]

#serial_number_list=[]
#for w in range(len(files_in_folder)):
#    serial_number_list.append(extract_serial_number(files_in_folder[w]))
#
#u=serial_number_list.index(serial_number)  
#single_file_path=os.path.join(setpoint_folder, files_in_folder[u])

u_count=0
for u in range(len(files_in_folder)):
#for u in range(0,1):
    single_file_path=os.path.join(setpoint_folder, files_in_folder[u])

#--------------------------------------------------------------------------------prints end of filename
    runnumberbylogfile=re.search('(\d+-setpoint)',files_in_folder[u])

    justnumbertemp=runnumberbylogfile.group(0)
    
    try:
        u_count=u_count+1
        print(u_count)
        print(justnumbertemp)
        
        AA=get_variable_from_csv(single_file_path, sensor_variables)
        
        modified_length, mmm=adjusted_length(single_file_path)  
   
        A=AA[-modified_length:]
        m=mmm[-modified_length:]
      
        A_difference = np.zeros(((modified_length-1),1))
        for i in range(0,(modified_length-1)):
            A_difference[i] = A[i+1] - A[i]           
             
        uu,uuu=np.unique(m,return_counts=True)
        uuu[-1]=uuu[-1]
        k=len(uuu)
        nnn=uuu
        
        rrr=0
        B=(-1)*np.ones((len(A),3))
        B[rrr,0]=A[0]
        for i in range(len(A_difference)):
            if math.fabs(A_difference[i])!=0:
                B[rrr,1]=i
                B[rrr+1,0]=A[i+1]
                rrr=rrr+1
        B[rrr,1]=len(A)-1  
        
        no_B=np.count_nonzero(B[:,1]!=-1)
        if rrr==0:
            G=np.zeros((1,3))
            G[0,0]=4
            G[0,1]=0
            G[0,2]=len(A)-1
            
            P=np.zeros((1,3))
        else:
            B=B[:no_B,:]
            B[0,2]=B[0,1]
        
            for i in range(len(B)-1):
                B[i+1,2]=B[i+1,1]-B[i,1]
        
            tt=0
            G=(-1)*np.ones((len(B),3))
            for i in range(len(B)):
                if B[i,2]>5:
                    if i==0:
                        G[tt,0]=4
                        G[tt,1]=0
                        G[tt,2]=B[i,2]
                        tt=tt+1
                    else:
                        G[tt,0]=4
                        G[tt,1]=B[i-1,1]+1
                        G[tt,2]=B[i,1]
                        tt=tt+1   

            no_G=np.count_nonzero(G[:,1]!=-1)
            G=G[:no_G,:]

            ttt=0
            P=(-1)*np.ones((len(B),3))
            for i in range(len(G)):
                if i!=len(G)-1:
                    if i==0 and G[i,1]==0 and G[i+1,1]-G[i,2]>2:
                        P[ttt,1]=G[i,2]+1
                        P[ttt,2]=G[i+1,1]-1
                        if np.mean(A_difference[P[ttt,1]:P[ttt,2]])>0.01 and np.mean(A_difference[P[ttt,1]:P[ttt,2]])<=0.1:
                            P[ttt,0]=5
                        elif np.mean(A_difference[P[ttt,1]:P[ttt,2]])>0.1:
                            P[ttt,0]=3
                        elif np.mean(A_difference[P[ttt,1]:P[ttt,2]])>-0.1 and np.mean(A_difference[P[ttt,1]:P[ttt,2]])<=-0.01:
                            P[ttt,0]=6
                        elif np.mean(A_difference[P[ttt,1]:P[ttt,2]])<-0.1:
                            P[ttt,0]=2
                        
                        ttt=ttt+1
                    elif i==0 and G[i,1]!=0 and G[i,1]>2:
                        P[ttt,1]=0
                        P[ttt,2]=G[i,1]-1
                        if np.mean(A_difference[P[ttt,1]:P[ttt,2]])>0.01 and np.mean(A_difference[P[ttt,1]:P[ttt,2]])<=0.1:
                            P[ttt,0]=5
                        elif np.mean(A_difference[P[ttt,1]:P[ttt,2]])>0.1:
                            P[ttt,0]=3
                        elif np.mean(A_difference[P[ttt,1]:P[ttt,2]])>-0.1 and np.mean(A_difference[P[ttt,1]:P[ttt,2]])<=-0.01:
                            P[ttt,0]=6
                        elif np.mean(A_difference[P[ttt,1]:P[ttt,2]])<-0.1:
                            P[ttt,0]=2
                            
                        ttt=ttt+1
                    elif i!=0 and G[i,1]!=0 and G[i+1,1]-G[i,2]>2:
                        P[ttt,1]=G[i,2]+1
                        P[ttt,2]=G[i+1,1]-1
                        if np.mean(A_difference[P[ttt,1]:P[ttt,2]])>0.01 and np.mean(A_difference[P[ttt,1]:P[ttt,2]])<=0.1:
                            P[ttt,0]=5
                        elif np.mean(A_difference[P[ttt,1]:P[ttt,2]])>0.1:
                            P[ttt,0]=3
                        elif np.mean(A_difference[P[ttt,1]:P[ttt,2]])>-0.1 and np.mean(A_difference[P[ttt,1]:P[ttt,2]])<=-0.01:
                            P[ttt,0]=6
                        elif np.mean(A_difference[P[ttt,1]:P[ttt,2]])<-0.1:
                            P[ttt,0]=2
                        ttt=ttt+1
                if i==len(G)-1 and G[i,2]!=len(A)-1:
                    P[ttt,1]=G[-1,2]+1
                    P[ttt,2]=len(A)-1
                    if np.mean(A_difference[P[ttt,1]:P[ttt,2]])>0.01 and np.mean(A_difference[P[ttt,1]:P[ttt,2]])<=0.1:
                        P[ttt,0]=5
                    elif np.mean(A_difference[P[ttt,1]:P[ttt,2]])>0.1:
                        P[ttt,0]=3
                    elif np.mean(A_difference[P[ttt,1]:P[ttt,2]])>-0.1 and np.mean(A_difference[P[ttt,1]:P[ttt,2]])<=-0.01:
                        P[ttt,0]=6
                    elif np.mean(A_difference[P[ttt,1]:P[ttt,2]])<-0.1:
                        P[ttt,0]=2
                
            no_P=np.count_nonzero(P[:,1]!=-1)
            P=P[:no_P,:]

        yyy=0
        PP=np.zeros((len(P),3))
        for i in range(len(P)):
            if P[i,0]==-1:
#                PP[yyy,1]=P[i,1]
                for j in range(int(P[i,1])+1,int(P[i,2]-2)):
                    if math.fabs(math.fabs(A_difference[j])-math.fabs(A_difference[j+1]))>0.1:
                        print(j)
                        yyy=yyy+1
        
        # partition completed
        
        section=np.cumsum(nnn)
        section=np.concatenate((np.array([0]),section),axis=0)
        
        categorylist=np.zeros(modified_length)   

        # plot
        plt.figure(figsize=(14,6))
        plt.plot(A)
        
        for g in range(len(G)):
            plt.axvspan(G[g,1], G[g,2], facecolor='c', alpha=0.5)
        
        for p in range(len(P)):
            if P[p,0]==2:
                plt.axvspan(P[p,1], P[p,2], facecolor='r', alpha=1)
            elif P[p,0]==3:
                plt.axvspan(P[p,1], P[p,2], facecolor='y', alpha=1)
            elif P[p,0]==5:
                plt.axvspan(P[p,1], P[p,2], facecolor='m', alpha=0.5)
            elif P[p,0]==6:
                plt.axvspan(P[p,1], P[p,2], facecolor='k', alpha=0.2)
        
        for j in range(0, k):
            if k>1 and section[j+1]-section[j]>3 and max(A_difference[section[j]+1:section[j+1]-1])*min(A_difference[section[j]+1:section[j+1]-1]) < 0:#fluctuation
                categorylist[section[j]:(section[j+1])]=1*np.ones((section[j+1]-section[j]))
                plt.axvspan(section[j], section[j+1], facecolor='g', alpha=1)
                
#                for i in range(len(G)):
#                    if section[j]<G[i,2] and section[j]>G[i,1]:
#                        G[i,2]=section[j]-1
#                    elif section[j+1]<G[i,2] and section[j+1]>G[i,1]:
#                        G[i,1]=section[j+1]
#                
#                for i in range(len(G)):
#                    if G[i,2]
                        
#                elif max(A_difference[section[j]+1:section[j+1]-1]) < -0.1:# decrease fast:red
#                    categorylist[section[j]:(section[j+1])]=2*np.ones((section[j+1]-section[j]))
#                    plt.axvspan(section[j], section[j+1], facecolor='r', alpha=1)
#                elif min(A_difference[section[j]+1:section[j+1]-1]) > 0.1:# increase fast:yellow
#                    categorylist[section[j]:(section[j+1])]=3*np.ones((section[j+1]-section[j]))
#                    plt.axvspan(section[j], section[j+1], facecolor='y', alpha=1)
#                elif max(A_difference[section[j]+1:section[j+1]-1]) < 0.01 and min(A_difference[section[j]+1:section[j+1]-1]) >= -0.01: # stable:cyan
#                    categorylist[section[j]:(section[j+1])]=4*np.ones((section[j+1]-section[j]))
#                    plt.axvspan(section[j], section[j+1], facecolor='c', alpha=0.5)
#                elif max(A_difference[section[j]+1:section[j+1]-1]) <= 0.1 and max(A_difference[section[j]+1:section[j+1]-1]) >= 0.01 and min(A_difference[section[j]+1:section[j+1]-1]) >= 0: # increase slowly:magenta
#                    categorylist[section[j]:(section[j+1])]=5*np.ones((section[j+1]-section[j]))
#                    plt.axvspan(section[j], section[j+1], facecolor='m', alpha=0.5)
#                elif min(A_difference[section[j]+1:section[j+1]-1]) >= -0.1 and max(A_difference[section[j]+1:section[j+1]-1]) <= -0.01 and min(A_difference[section[j]+1:section[j+1]-1]) <= 0: # decrease slowly:gray
#                    categorylist[section[j]:(section[j+1])]=6*np.ones((section[j+1]-section[j]))
#                    plt.axvspan(section[j], section[j+1], facecolor='k', alpha=0.2)                
#                else: 
#                    categorylist[section[j]:(section[j+1])]=6*np.ones((section[j+1]-section[j]))
#                    plt.axvspan(section[j], section[j+1], facecolor='w', alpha=1)
            
            
            
            
            
            
#        for i in range(1, np.shape(categorylist)[0]):
#            if categorylist[i]==0:
#                categorylist[i]=categorylist[i-1]
                
#        for j in range(len(categorylist)-1):
#            if categorylist[j+1]!=categorylist[j]:
#                if categorylist[j]==1:
#                    plt.axvspan(categorylist[j-1], categorylist[j]+1, facecolor='g', alpha=0.8)
#                if categorylist[j]==2:
#                    plt.axvspan(categorylist[j-1], categorylist[j]+1, facecolor='r', alpha=1)
#                if categorylist[j]==3:
#                    plt.axvspan(categorylist[j-1], categorylist[j]+1, facecolor='y', alpha=1)
#                if categorylist[j]==4:
#                    plt.axvspan(categorylist[j-1], categorylist[j]+1, facecolor='c', alpha=0.5)
#                if categorylist[j]==5:
#                    plt.axvspan(categorylist[j-1], categorylist[j]+1, facecolor='m', alpha=0.5)
#                if categorylist[j]==6:
#                    plt.axvspan(categorylist[j-1], categorylist[j]+1, facecolor='k', alpha=0.2)
        
#        if len(section)==2:
#            intv=np.zeros((2,2))
#            intv[1,0]=np.count_nonzero(categorylist==categorylist[-2])
#            intv[1,1]=categorylist[-2]
#            intv_n=2
#        else:
#            r=0
#            rr=0
#            intv=np.zeros((max(m),2))
#            for s in range(len(categorylist)-1):
#                if categorylist[s]!=categorylist[s+1]:
#                    intv[r,0]=np.count_nonzero(categorylist[rr:s+1]==categorylist[s])
#                    rr=s
#                    intv[r,1]=categorylist[s]
#                    r=r+1
#            intv_n=r
#            intv[:,0]=np.cumsum(intv[:,0])
#            intv=np.concatenate((np.zeros((1,2)),intv),axis=0)
#        
#        for v in range(len(intv)-1):
#            if intv[v+1,1]==1:
#                plt.axvspan(intv[v,0], intv[v+1,0]-1, facecolor='g', alpha=0.8)
#            if intv[v+1,1]==2:
#                plt.axvspan(intv[v,0], intv[v+1,0]-1, facecolor='r', alpha=1)
#            if intv[v+1,1]==3:
#                plt.axvspan(intv[v,0], intv[v+1,0]-1, facecolor='y', alpha=1)
#            if intv[v+1,1]==4:
#                plt.axvspan(intv[v,0], intv[v+1,0]-1, facecolor='c', alpha=0.5)
#            if intv[v+1,1]==5:
#                plt.axvspan(intv[v,0], intv[v+1,0]-1, facecolor='m', alpha=0.5)
#            if intv[v+1,1]==6:
#                plt.axvspan(intv[v,0], intv[v+1,0]-1, facecolor='k', alpha=0.2)
    
#        categorylist=np.concatenate((np.zeros(zero_step),categorylist),axis=0)
        
        complete_path_to_save_segmentlist=os.path.normpath(os.path.join(complete_dirpath_to_save_segmentlist,justnumbertemp))
        figure_filename2=justnumbertemp.replace('.csv','.png')
        complete_path_to_save_figure=os.path.normpath(os.path.join(complete_dirpath_to_save_figure,figure_filename2))
        
        write_array_to_csv(complete_path_to_save_segmentlist,categorylist)

        plt.xlim(0,len(A)-1)
#        plt.xlim(13120,13131)
        plt.grid()
        plt.xlabel("Time(s)",fontsize=16)
        plt.ylabel("Setpoint",fontsize=16) 
        for tick in plt.gca().xaxis.get_major_ticks():
            tick.label1.set_fontsize(12) 
        for tick in plt.gca().yaxis.get_major_ticks():
            tick.label1.set_fontsize(12) 
        plt.savefig(complete_path_to_save_figure)
        plt.clf()
    
    
    except ValueError:
#        print('Reading CSV file:',justnumbertemp)
#        print('run',u)
        print('No valid StepLabel in this run!!!')
        doesnotwork.append(u)
#    print('Reading CSV file:',justnumbertemp) 
    
    print('-----------------------------------------')
complete_path_to_save_doesnotwork=os.path.normpath(os.path.join(output_folder,"doesnotwork.csv"))
write_array_to_csv(complete_path_to_save_doesnotwork,doesnotwork)
