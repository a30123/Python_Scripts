#### created date:Aug 5 2015
#### last modified date:
#### author:A30123
#### description:


#########################################################################################################
###      #####  #####        #####       ###############    #   ###  ###       ###       ################
###  #########  ########  ########  ####################  #  #  ###  ###  ###  ###  ###  ################
###  #########  ########  ########  ####################  ####  ###  ###  ###  ###  ###  ################
###      #####  ########  ########       ###############  ####  ###  ###       ###       ################
#########################################################################################################


#########################################################################################################
#######################################   IMPORT LIBRARIES    ###########################################
#########################################################################################################

#########################################################################################################
########################################   FUNCTIONS           ##########################################
#########################################################################################################
library(ggplot2)
library("gridExtra")#used by grid.arrange
library(lubridate)
#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################
file_path_name="C:/Users/A30123.ITRI/Documents/Safebox/2015 PHM Challenge/data/PHMtrain/plant_1a.csv"
file_path_name2="C:/Users/A30123.ITRI/Documents/Safebox/2015 PHM Challenge/data/PHMtrain/plant_1c.csv"
output_folder_path="C:/Users/A30123.ITRI/Documents/R scripts/PHM Challenge 2015/Try_20150819_ggplot_stackplots_failure/output/plant1/"
#########################################################################################################
########################################   MAIN PROGRAM        ##########################################
#########################################################################################################


###fetch data
data<-read.csv(file_path_name,header=F)
data2<-read.csv(file_path_name2,header=F)


#data_split<-split(data2,floor((1:length(data2[,1])/1000)))
#all_intervals_fault1=vector()

data_fault1<-data2[data2[,3]==1,]
# all_intervals_fault1=
# for (kk in 1:length(data_fault1[,1])){
#   intervals_fault1<-new_interval(data_fault1[kk,1],data_fault1[kk,2])
#   all_intervals_fault1=c(all_intervals_fault1,intervals_fault1)                          
# }
a<-rep(0,length(data_fault1[,1]))
names(data)=c("component","time","sensor_1","sensor_2","sensor_3","sensor_4", "control_1","control_2", "control_3", "control_4")
data$time<-strptime(data$time,format="%Y-%m-%d %H:%M:%S")
data_length<-length(data[,1])
plot_number<-floor(data_length/1000)



for (i in 1:plot_number){
  begin_index<-(1+1000*(i-1))
  end_index<-(1000*i)
  plot_time_interval<-new_interval(data[begin_index,2],data[end_index,2])
  temp_data=as.data.frame(data[begin_index:end_index,])
  p1<-ggplot(temp_data)+geom_line(aes(x=time,y=sensor_1,group=component,col=factor(component)))+theme(legend.position="none")
  

  for (kk in 1:length(data_fault1[,1])){
    if(int_overlaps(plot_time_interval,new_interval(data_fault1[kk,1],data_fault1[kk,2]))){
      a[kk]<-1
      #p1<-p1+geom_rect(aes(xmin = as.POSIXct(data_fault1[kk,1]), xmax=as.POSIXct(data_fault1[kk,2]),ymin = -Inf, ymax = Inf),fill="green",alpha = 0.4)
    }
  }
  new_fault1<-as.data.frame(data_fault1[a==1,])
  new_fault1$V1=as.POSIXct(new_fault1$V1)
  new_fault1$V2=as.POSIXct(new_fault1$V2)
  p1<-(p1+geom_rect(data=new_fault1,aes(xmin =V1, xmax=V2,ymin = -Inf, ymax = Inf),fill="pink",alpha = 0.4))
  p1
  
  p2<-ggplot(data=data[begin_index:end_index,],aes(x=time,y=sensor_2,group=component,col=factor(component)))+geom_line()+theme(legend.position="none")
  p3<-ggplot(data=data[begin_index:end_index,],aes(x=time,y=sensor_3,group=component,col=factor(component)))+geom_line()+theme(legend.position="none")
  p4<-ggplot(data=data[begin_index:end_index,],aes(x=time,y=sensor_4,group=component,col=factor(component)))+geom_line()+theme(legend.position="bottom")

  dirname1<-output_folder_path
  dirname2<-"plant1"
  dirname3<-"_"
  dirname4<-toString(begin_index)
  dirname5<-"to"
  dirname6<-toString(end_index)
  dirname7<-".jpg"
  dirname=paste(dirname1,dirname2,dirname3,dirname4,dirname5,dirname6,dirname7,sep="")

  grid.arrange(p1,p2,p3,p4,ncol=1, nrow=4, heights=c(1,1,1,1.3), widths=c(4))
  dev.copy(png,file=dirname, width=12, height=10,units="in",res=50)
  graphics.off()

}
