# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 16:49:31 2015

@author: Jia-Min Ren
"""


import os
import time
import numpy as np
from sklearn.neighbors import NearestNeighbors
import itertools
from itri_SC import itriSC
import importlib
importlib.reload(itriSC)


#################Jia-Min defined functions########################################
def genPatchFromCycleData2(data, patchSize=4, degradationTh=None):
    # number of cycle    
    numCycle = len(data)

    patch=[]
    patchRUL=[]
    patchCycleId=[]
    for i in range(0,numCycle):
        cycleData = data[i]
        # find the first run whose dp.filter is larger than degradationTh,
        # and then use the runs after the first run to create patches
        if degradationTh is None:
            idxFirstRun=[0] # the first run starts from 0
        else:
            idxFirstRun = np.where(cycleData >= degradationTh)[0]
            
        # if idxFirstRun is empty, then continue
        if len(idxFirstRun)==0:
            continue
        
        # only consider runs whose index is after idxFirstRun
        cycleData = cycleData[idxFirstRun[0]:]
        
        #split cycleData into overlapping patches
        numRun = len(cycleData) # number of runs in a cycle
        for j in range(0,numRun-patchSize):
            patch.append(cycleData[j:j+patchSize])
            patchRUL.append(cycleData[(j+patchSize)]/30) # number of remaining runs
            patchCycleId.append(i) # Cycle failure Id of current patch
        
    patch = np.asarray(patch)
    patchRUL = np.asarray(patchRUL)
    patchCycleId = np.asarray(patchCycleId)
    
    return patch, patchRUL, patchCycleId
 
    
#################Jia-Min defined function, Chi-Ting modified########################################
def computeRUL(knnDist, knnIdx, patchRUL, patchCycleId, testDataCycle=None, weightedMethod='I1'):
    
    numTestSample, k = knnIdx.shape # number of test samples

    p_RUL = [] # predicted rul of test samples
    p_conf = [] # predicted confidence of test samples
    
    # use mean of knn training samples as RUL
    # use 1/std of knn training samples as confidence
    for i in range(0, numTestSample):
        
        # equal-weighted RUL
        if weightedMethod == 'I1': 
            p_RUL.append(np.mean(patchRUL[knnIdx[i]]))
            
        # equal-weighted + exclude outlier(mean+std)
        if weightedMethod == 'I2': 
            std = np.std(patchRUL[knnIdx[i]])
            mean = np.mean(patchRUL[knnIdx[i]])
            temp = patchRUL[knnIdx[i]]
            temp = temp[np.abs(temp-mean)<(1*std)]
            p_RUL.append(np.mean(temp))
        
        # cycle-weighted 
        if weightedMethod == 'I3': 
            u, indices = np.unique(patchCycleId[knnIdx[i]],return_inverse=True)
            u, counts  = np.unique(patchCycleId[knnIdx[i]],return_counts=True)        
            weights2=[counts[int(kk)] for kk in indices ]
            p_RUL.append(np.average(patchRUL[knnIdx[i]],weights=weights2/sum(weights2)))
        
        if weightedMethod == 'I4': # distance-weighted 
            weights = 1.0 / knnDist
            weights /= weights.sum(axis=1)[:,None]
            p_RUL.append(np.dot(weights[i].T, patchRUL[knnIdx[i]]))
  
        p_conf.append(1.0/np.std(patchRUL[knnIdx[i]]))

    p_RUL = np.asarray(p_RUL)
    p_conf = np.asarray(p_conf)
    

    
    # correct RUL if necessary
    if testDataCycle is not None:
        uniCycleIdx = np.unique(testDataCycle)
        for i in range(0, len(uniCycleIdx)):
            rul = p_RUL[testDataCycle==uniCycleIdx[i]]
            conf = p_conf[testDataCycle==uniCycleIdx[i]]
            for j in range(1, len(rul)):
                if conf[j] <= conf[j-1]: # high confidence with previous result
                    rul[j] = rul[j-1]-1 # so current rul = previous rul -1
                    conf[j] = conf[j-1] # also replace confidence
                if rul[j] < 1: # predicted minimum rul is one run 
                    rul[j]=1
            p_RUL[testDataCycle==uniCycleIdx[i]]=rul
            p_conf[testDataCycle==uniCycleIdx[i]]=conf
    
    return p_RUL, p_conf
    
    
def write_array_to_csv(filename_path,listname):
    import csv
     
    runnumberfile=open(filename_path,'w',newline='')
    wr=csv.writer(runnumberfile,quoting=csv.QUOTE_MINIMAL,delimiter=',')
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
    
###################Initialization -----folder path#################################
current_directory=os.getcwd()
train_data_folder=os.path.join(current_directory,"train_test_data//train_data")
test_data_folder=os.path.join(current_directory,"train_test_data//test_data")

##################Initialization------ parameters ########################
parameter_variables_A={0:"patch size",'A1':4}
parameter_variables_B={0:"degradation threshold",'B1':10}
parameter_variables_C={0:"target value",'C1':"RUL",'C2':"life percentage",'C3':"dP_Filter percentage"}
parameter_variables_D={0:"atom number",'D1':4,'D2':6,'D3':8}
parameter_variables_E={0:"dictionary learning:alpha",'E1':0.5,'E2':1,'E3':2}
parameter_variables_F={0:"dictionary learning: initial D",'F1':"SPAMs",'F2':"sklearn"}
parameter_variables_G={0:"KNN: k", 'G1':3,'G2':5,'G3':7}
parameter_variables_H={0:"KNN: distance metric", 'H1':"euclidean", 'H2':"manhattan", 'H4':"cosine"}
parameter_variables_I={0:"weightedMethod",'I1':"I1",'I2':"I2", 'I3':"I3", 'I4':"I4"}
#parameter_variables_I={0:"weightedMethod",1:"equal weighted",2:"equal weighted exclude outlier", 3:"cycle weighted", 4:"distance weighted"}
parameter_list=[parameter_variables_A[0],parameter_variables_B[0],parameter_variables_C[0],parameter_variables_D[0],
                parameter_variables_E[0],parameter_variables_F[0],parameter_variables_G[0],parameter_variables_H[0],
                parameter_variables_I[0],'MSE','MAPE','accuracy']
##################### create combinations ##################
AA=list(parameter_variables_A.keys())[1:]
BB=list(parameter_variables_B.keys())[1:]
#CC=list(parameter_variables_C.keys())[1:]
CC=['C1']
DD=list(parameter_variables_D.keys())[1:]
EE=list(parameter_variables_E.keys())[1:]
#FF=list(parameter_variables_F.keys())[1:]
FF=['F2']
GG=list(parameter_variables_G.keys())[1:]
HH=list(parameter_variables_H.keys())[1:]
#HH=['H1','H2']
II=list(parameter_variables_I.keys())[1:]
combination_tuple=list(itertools.product(AA,BB,CC,DD,EE,FF,GG,HH,II))


#################data collection ########################
train_filenames=os.listdir(train_data_folder)
test_filenames=os.listdir(test_data_folder)
begin_time=time.time()
cycleData=[]
for filename in train_filenames:
    cycleData.append(np.loadtxt(os.path.join(train_data_folder,filename), delimiter=','))
    
TestcycleData=[]
for filename in test_filenames:
    TestcycleData.append(np.loadtxt(os.path.join(test_data_folder,filename), delimiter=','))



total = np.zeros((len(combination_tuple),12),dtype=object)
count=0
for tuptup in combination_tuple:
    #print(tuptup)
    #####################temporary variables/paramters ############
    patch_size_temp=parameter_variables_A[tuptup[0]]
    deg_threshold_temp=parameter_variables_B[tuptup[1]]
    atom_no_temp=parameter_variables_D[tuptup[3]]
    alpha_temp=parameter_variables_E[tuptup[4]]
    neighbor_number_temp=parameter_variables_G[tuptup[6]]
    distance_metric_temp=parameter_variables_H[tuptup[7]]
    weightedMethod_temp=parameter_variables_I[tuptup[8]]
    
    testDataCycle_temp=None
    
    ##################### Data preprocesing ---patch generation##################
    patch, patchRUL, patchCycleId = genPatchFromCycleData2(data = cycleData,patchSize=patch_size_temp,degradationTh=deg_threshold_temp)
    testpatch, testDataRUL, testDataCycle = genPatchFromCycleData2(data = TestcycleData,patchSize=patch_size_temp,degradationTh=deg_threshold_temp)
    
    ##################### Feature extraction ------dictionary learning############
    dictionary = itriSC.learnDict(data=patch, n_components=atom_no_temp, alpha=alpha_temp)
    sparseCoeff = itriSC.encoding(dictionary=dictionary, data=patch, transform_alpha=alpha_temp)
    TestsparseCoeff = itriSC.encoding(dictionary=dictionary, data=testpatch,transform_alpha=alpha_temp)                                                                
    
    ##################### Prediction model ----K-Nearest Neighbor ########
    nbrs = NearestNeighbors(algorithm='brute',metric=distance_metric_temp)
    nbrs.fit(X=sparseCoeff)
    knnDist, knnIdx = nbrs.kneighbors(X=TestsparseCoeff, n_neighbors=neighbor_number_temp,return_distance=True)
                  
    #p_RUL, p_conf = computeRUL(knnIdx, patchRUL, patchCycleId,testDataCycle=testDataCycle_temp)
    p_RUL, p_conf = computeRUL(knnDist, knnIdx, patchRUL, patchCycleId,testDataCycle=testDataCycle, weightedMethod=weightedMethod_temp)

    
    
    ###################### Performance evaluation ####################
    
    # mean square error
    rulError = (testDataRUL-p_RUL)
    rulSE = rulError**2
    rulMSE = np.mean(rulSE)
    print('MSE: %.4f\n' % rulMSE)
    
    # mean absolute percentage error
    rulAPE = np.abs(rulError / testDataRUL)
    rulMAPE = np.mean(rulAPE)
    print('MAPE: %.4f\n' % rulMAPE)
    
    # prediction accuracy: early prediction within 10% numRuns in a cycle
    numRunInTestCycle = np.array([34,65,48,42,67])
    hit=0.0
    uniCycleIdx = np.unique(testDataCycle)
    for i in range(0, len(uniCycleIdx)):
        rul = rulError[[testDataCycle==uniCycleIdx[i]]]
        for j in range(0,len(rul)):
            # early prediction & prediction error within 10% num of runs in a cycle
            if (rul[j] >= 0) & (rul[j] <= 0.1 * numRunInTestCycle[i]):
                hit = hit + 1
    
    accuracy = hit/len(rulError)
    print('Accuracy: %.4f' % accuracy)
    
    result = [tuptup[0],tuptup[1],tuptup[2],tuptup[3],
                              tuptup[4],tuptup[5],tuptup[6],
                              tuptup[7],tuptup[8],
                              '%.4f' % rulMSE, '%.4f' % rulMAPE, '%.4f' % accuracy]
        
    print(result)
    total[count,:]=result
    count +=1
total=np.vstack((parameter_list,total))

write_array_to_csv("output.csv",total)    


total_time=time.time()-begin_time
print('Total time: %.4f' % total_time)