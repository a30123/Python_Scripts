# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 22:12:42 2015

@author: HCKu
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
    serial_number_string=serial_number_string.replace('-setpoint','')
    serial_number_string=serial_number_string.replace('_','') 
    value_of_number=int(serial_number_string)
    return value_of_number

def adjusted_length(step_steplabel_file_path):
#    import numpy as np    
    xxx=get_variable_from_csv_alternative(single_file_path, 'Step')
    zero_step=np.zeros((1,1))
    zero_step=np.count_nonzero(xxx!=0)                
    return zero_step, xxx
    
#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################


sensor_variables=['NH3_1.push']#-------------------------------------"sensor variable of interest"
#setpoint_folder='D://setpoint'
#output_folder='D://Output'
setpoint_folder='D://MOCVD-TS2//setpoint'
output_folder='D://MOCVD-TS2//Output2'
#setpoint_folder='D://setpoint'
#output_folder='D://Output'
#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################

tstart = time.time()

files_in_folder = os.listdir(setpoint_folder)
files_in_folder.sort(key=extract_serial_number) 

complete_dirpath_to_save_segmentlist=os.path.normpath(os.path.join(output_folder,"CSV"))    
ensure_dir(complete_dirpath_to_save_segmentlist)

complete_dirpath_to_save_figure=os.path.normpath(os.path.join(output_folder,"FIG"))    
ensure_dir(complete_dirpath_to_save_figure)

doesnotwork=[]

u_count=0
for u in range(len(files_in_folder)):
    single_file_path=os.path.join(setpoint_folder, files_in_folder[u])

#--------------------------------------------------------------------------------prints end of filename
    runnumberbylogfile=re.search('(\d+-setpoint)',files_in_folder[u])

    justnumbertemp=runnumberbylogfile.group(0)
    
    try:
        u_count=u_count+1
        print(u_count)
        print(justnumbertemp)
        
        AA=get_variable_from_csv(single_file_path, sensor_variables)
        
        zero_step, mmm=adjusted_length(single_file_path)
                
        plt.figure(figsize=(14,6))
        plt.plot(AA[zero_step:])
        
        A=AA[zero_step:]
        m=mmm[zero_step:]
      
        A_difference = np.zeros(((len(A)-1),1))
        m_difference = np.zeros(((len(m)-1),1))
        for i in range(0,(len(A)-1)):
            A_difference[i] = A[i+1] - A[i]    
            m_difference[i] = int(m[i+1]) - int(m[i])      
        
        no_A_difference=np.count_nonzero(m_difference<0)
        if no_A_difference>0:
            s=0
            D=np.zeros((len(A),3))
            for i in range(len(m)-1):
                if m_difference[i]<0:
                    D[s,0]=s+1
                    D[s,1]=i+1
                    D[s,2]=m[i+1]
                    s=s+1

            no_D=np.count_nonzero(D[:,1]!=0)
            D=D[:no_D,:]

            gg,ggg=np.unique(D[:,2],return_counts=True)
            ggg=np.cumsum(ggg)
            
            fff=np.zeros((len(ggg)+1,1))
            for i in range(len(fff)):
                if i==0:
                    fff[i]=0
                elif i>0:
                    fff[i]=ggg[i-1]
            
            s_gg=np.zeros((len(gg),1))
            yy=0
            for j in range(len(fff)-1):
                s_gg[yy]=min(D[fff[j]:fff[j+1]+1,1])-1
                yy=yy+1

            ss=0
            E=(-1)*np.ones((len(A),len(gg)))
            for j in range(len(gg)):
                for i in range(len(A)):
                    if int(m[i])==gg[j] or int(m[i])==gg[j]+(int(m[int(s_gg[j])])-gg[j]):
                        E[ss,j]=i
                        ss=ss+1
                ss=0

            fluc1=np.zeros((len(gg),2))
            for i in range(len(gg)):
                fluc1[i,0]=min(E[:np.count_nonzero(E[:,i]!=-1),i])
                fluc1[i,1]=max(E[:np.count_nonzero(E[:,i]!=-1),i])
        
            fluc=np.zeros((len(gg),2))
            y=0
            for k in range(len(fluc1)):
                if max(A_difference[fluc1[k,0]:fluc1[k,1]])*min(A_difference[fluc1[k,0]:fluc1[k,1]])<0:#fluctuation
                    fluc[y,0]=fluc1[k,0]
                    fluc[y,1]=fluc1[k,1]
                    y=y+1
        
            no_fluc=np.count_nonzero(fluc[:,0]!=0)
            fluc=fluc[:no_fluc,:]
            
            rrr=0
            B=(-1)*np.ones((len(A),3))
            B[rrr,0]=A[0]
            
            for i in range(len(fluc)):
                A[int(fluc[i,0]):int(fluc[i,1])+1]=(-1)*np.ones((int(fluc[i,1])-int(fluc[i,0])+1,1))            
            
            for i in range(0,(len(A)-1)):
                A_difference[i] = A[i+1] - A[i]
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

                for i in range(len(fluc)):
                    for j in range(len(G)):
                        if G[j,1]==fluc[i,0]:
                            G[j,0]=1

                ttt=0
                P=(-1)*np.ones((len(B),2))
                for i in range(len(G)):
                    if i!=len(G)-1:
                        if i==0 and G[i,1]==0 and G[i+1,1]-G[i,2]>2:
                            P[ttt,0]=G[i,2]+1
                            P[ttt,1]=G[i+1,1]-1                   
                            ttt=ttt+1
                        elif i==0 and G[i,1]!=0 and G[i,1]>2:
                            P[ttt,0]=0
                            P[ttt,1]=G[i,1]-1                         
                            ttt=ttt+1
                        elif i!=0 and G[i,1]!=0 and G[i+1,1]-G[i,2]>3:
                            P[ttt,0]=G[i,2]+1
                            P[ttt,1]=G[i+1,1]-1
                            ttt=ttt+1
                    elif i==len(G)-1 and G[i,2]!=len(A)-1:
                        P[ttt,0]=G[-1,2]+1
                        P[ttt,1]=len(A)-1
                
                no_P=np.count_nonzero(P[:,0]!=-1)
                P=P[:no_P,:]
            
        else:
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
                P=(-1)*np.ones((len(B),2))
                for i in range(len(G)):
                    if i!=len(G)-1:
                        if i==0 and G[i,1]==0 and G[i+1,1]-G[i,2]>2:
                            P[ttt,0]=G[i,2]+1
                            P[ttt,1]=G[i+1,1]-1                   
                            ttt=ttt+1
                        elif i==0 and G[i,1]!=0 and G[i,1]>2:
                            P[ttt,0]=0
                            P[ttt,1]=G[i,1]-1                         
                            ttt=ttt+1
                        elif i!=0 and G[i,1]!=0 and G[i+1,1]-G[i,2]>3:
                            P[ttt,0]=G[i,2]+1
                            P[ttt,1]=G[i+1,1]-1
                            ttt=ttt+1
                    elif i==len(G)-1 and G[i,2]!=len(A)-1:
                        P[ttt,0]=G[-1,2]+1
                        P[ttt,1]=len(A)-1
                
                no_P=np.count_nonzero(P[:,0]!=-1)
                P=P[:no_P,:] 
            
        # plot
        L=np.zeros((len(P),3))
        for j in range(len(P)):
            pp,ppp=np.unique(m[int(P[j,0]):int(P[j,1])+1],return_counts=True)
                
            pppp=np.zeros((len(pp)+1,1))
            pppp[0]=P[j,0]

            for i in range(1,len(pppp)):
                pppp[i]=np.count_nonzero(m[int(P[j,0]):int(P[j,1])+1]==pp[i-1])+pppp[i-1]-1

            for i in range(len(pppp)-1):
                slope=(A[int(pppp[i+1])]-A[int(pppp[i])])/(int(pppp[i+1])-int(pppp[i]))
                if slope>0.01 and slope<=0.1:
                    L[j,0]=5
                    L[j,1]=pppp[i]
                    L[j,2]=pppp[i+1]
                    plt.axvspan(pppp[i], pppp[i+1], facecolor='m', alpha=0.5)
                elif slope>0.1:
                    L[j,0]=3
                    L[j,1]=pppp[i]
                    L[j,2]=pppp[i+1]
                    plt.axvspan(pppp[i], pppp[i+1], facecolor='y', alpha=1)
                elif slope>-0.1 and slope<=-0.01:
                    L[j,0]=6
                    L[j,1]=pppp[i]
                    L[j,2]=pppp[i+1]                        
                    plt.axvspan(pppp[i], pppp[i+1], facecolor='k', alpha=0.2)
                elif slope<-0.1:
                    L[j,0]=2  
                    L[j,1]=pppp[i]
                    L[j,2]=pppp[i+1]
                    plt.axvspan(pppp[i], pppp[i+1], facecolor='r', alpha=1)
                else:
                    if pppp[i+1]!=pppp[i]:
                        L[j,0]=7  
                        L[j,1]=pppp[i]
                        L[j,2]=pppp[i+1]
                        
        no_L=np.count_nonzero(L[:,0]!=0)
        L=L[:no_L,:]
                    
   
        for g in range(len(G)):
            if G[g,0]==4:
                plt.axvspan(G[g,1], G[g,2], facecolor='c', alpha=0.5)
            elif G[g,0]==1:
                plt.axvspan(G[g,1], G[g,2], facecolor='g', alpha=1)
        
        segmentlist=np.zeros((len(G)+len(L),3))
        segmentlist=np.concatenate((G,L),axis=0)        
        
        segment_filename=files_in_folder[u].replace('setpoint','segmentlist')
        complete_path_to_save_segmentlist=os.path.normpath(os.path.join(complete_dirpath_to_save_segmentlist,segment_filename))
        write_array_to_csv(complete_path_to_save_segmentlist,segmentlist) 
 
        figure_filename=files_in_folder[u].replace('.csv','.png')
        complete_path_to_save_figure=os.path.normpath(os.path.join(complete_dirpath_to_save_figure,figure_filename))

        plt.xlim(0,len(A)-1)
#        plt.xlim(8055,8080)
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
        print('No valid StepLabel in this run!!!')
        doesnotwork.append(u)
    
    print('-----------------------------------------')

