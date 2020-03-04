#This follows this url http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier



data = pd.read_csv ("C:\\Users\\SCarron\\Desktop\\compilation.csv")
#Verify that the data read in successfully
print "Data Head: ", data.head ()



#Filter data to keep variables of interest AND remove Null values
dataFilter = data [["Total Crack Scrap","Total Starts","Carbide Density", "Carbide MS", "Carbide HC", "PCD Density","Power Avg", "TempTC Avg","TIMEbRuns Avg","Press","Operator ID"]] [(data ["Bad Carbide flag"] == "Good") & (data ["Carbide Density"].notnull ()) & (data ["Carbide MS"].notnull ()) & (data ["Carbide HC"].notnull ()) & (data ["PCD Density"].notnull ()) & (data ["Power Avg"].notnull ()) & (data ["TempTC Avg"].notnull ()) & (data ["TIMEbRuns Avg"].notnull ()) & (data ["Press"].notnull ()) & (data ["Operator ID"].notnull ())]
#Verify that the data was filtered correctly
print "DataFilter Head: ", dataFilter.head ()




#Compute fraction of each batch that was labeled as failure
dataFilter ["Failure PCT"] = dataFilter ["Total Crack Scrap"] / (1.0 * dataFilter ["Total Starts"])
#Verify that the computation was successfully
print "DataFilter AFTER Failure PCT: ", dataFilter.head ()



#Create a class label identifying each batch as successful or failure. Failure if the batch's scrap fraction exceeded 0.025
dataFilter ["Failure Success Class"] = np.where (dataFilter ["Failure PCT"] > 0.025, 1, 0)
#Verify that the computation was successful
print "DataFilter AFTER Failure Success Class: ", dataFilter.head ()



#Split the data set into Train and Test sets
xTrain, xTest = train_test_split (dataFilter, test_size=0.05, random_state=5)



#Build the classifier
clf = KNeighborsClassifier ()
clf.fit (xTrain [["Carbide Density", "Carbide MS", "Carbide HC", "PCD Density","Power Avg","TempTC Avg","TIMEbRuns Avg","Press"]], xTrain ["Failure Success Class"])

knnPrediction = clf.predict (xTest [["Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press"]])


knnAccuracy = np.where (xTest ["Failure Success Class"] == knnPrediction, 1, 0)
print "Accuracy of KNN prediction: ", np.mean (knnAccuracy)











clfOriginalFilter = KNeighborsClassifier ()
clfOriginalFilter.fit (xTrain [["Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press"]], xTrain ["Total Crack Scrap"])

knnOriginalFilterPrediction = clfOriginalFilter.predict (xTest [["Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press"]])


knnOriginalFilterAccuracy = np.where (xTest ["Total Crack Scrap"] == knnOriginalFilterPrediction, 1, 0)
print "Accuracy of KNN prediction when using ORIGINAL target (Total Crack Scrap): ", np.mean (knnOriginalFilterAccuracy)