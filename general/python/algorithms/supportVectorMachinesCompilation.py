#This follows this url http://scikit-learn.org/stable/modules/svm.html

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm


data = pd.read_csv ("C:\\Users\\SCarron\\Desktop\\compilation.csv")

#Verify that the data was read in successfully
print "Data Head: ", data.head ()


#Filter the data
dataFilter = data [["Total Crack Scrap","Total Starts","Bad Carbide flag","Carbide Density", "Carbide MS", "Carbide HC", "PCD Density","Power Avg","TempTC Avg","TIMEbRuns Avg","Press","Operator ID"]] [(data ["Bad Carbide flag"] == "Good") & (data ["Carbide Density"].notnull ()) & (data ["Carbide MS"].notnull ()) & (data ["Carbide HC"].notnull ()) & (data ["PCD Density"].notnull ()) & (data ["Power Avg"].notnull ()) & (data ["TempTC Avg"].notnull ()) & (data ["TIMEbRuns Avg"].notnull ()) & (data ["Press"].notnull ()) & (data ["Operator ID"].notnull ())]
#Verify that filtering was successful
print "DataFilter Head: ", dataFilter.head ()




#Compute the fraction of each batch that was labeled as failure
dataFilter ["Failure PCT"] = dataFilter ["Total Crack Scrap"] / (1.0 * dataFilter ["Total Starts"])
#Verify that the computation was successful
print "DataFilter AFTER Failure PCT: ", dataFilter.head ()




#Create a class label that identifies as batch as either successful or failure. Failure if the batch's scrap fraction exceeded 0.025
dataFilter ["Failure Success Class"] = np.where (dataFilter ["Failure PCT"] > 0.025, 1, 0)
#Verify that the class labels were created successfully
print "DataFilter AFTER Failure Success Class label: ", dataFilter.head ()



#Split the data into the train and test set
xTrain, xTest = train_test_split (dataFilter, test_size=0.5, random_state=5)


#Build the SVM model with the Training Data
clf = svm.SVC ()
clf.fit (xTrain [["Carbide Density", "Carbide MS", "Carbide HC", "PCD Density","Power Avg","TempTC Avg","TIMEbRuns Avg","Press"]], xTrain ["Failure Success Class"])

#SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False)



#Predict with the Test Data
svmPrediction = clf.predict (xTest [["Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press"]])
print "Type of svmPrediction: ", type (svmPrediction)

accuracyCount = np.where (xTest ["Failure Success Class"] == svmPrediction, 1, 0)
print "Accuracy of SVM Prediction: ", np.mean (accuracyCount)




#Build SVM using the Total Crack Scrap values as the Target Class Labels (achieved 76% accuracy)
clfOriginalFilter = svm.SVC ()
clfOriginalFilter.fit (xTrain [["Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press"]], xTrain ["Total Crack Scrap"])

svmOriginalFilterPrediction = clfOriginalFilter.predict (xTest [["Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press"]])

accuracyOriginalFilter = np.where (xTest ["Total Crack Scrap"] == svmOriginalFilterPrediction, 1, 0)
print "Accuracy of SVM Prediction with Total Crack Scrap as response: ", np.mean (accuracyOriginalFilter)


















	












#Build SVM models using single explanatory variables with the Target Failure Sucess Class Labels

#Using Carbide as the SINGLE explanatory feature, and the Failure Success Class label I generated as the target, the accuracy was 84.4%
clfCarbideDensity = svm.SVC ()
clfCarbideDensity.fit (xTrain ["Carbide Density"].values.reshape (-1,1), xTrain ["Failure Success Class"])

svmCarbideDensityPrediction = clfCarbideDensity.predict (xTest ["Carbide Density"].values.reshape (-1,1))

accuracyCarbideDensity = np.where (xTest ["Failure Success Class"] == svmCarbideDensityPrediction, 1, 0)
print "Accuracy of SVM Prediction with Carbide Density as explanatory: ", np.mean (accuracyCarbideDensity)

#Using Carbide as the SINGLE explanatory feature, and the Total Crack Scrap as the target, the accuracy was 76.11%
clfCarbideDensityCrackScrap = svm.SVC ()
clfCarbideDensityCrackScrap.fit (xTrain ["Carbide Density"].values.reshape (-1,1), xTrain ["Total Crack Scrap"])

svmCarbideDensityCrackScrapPrediction = clfCarbideDensityCrackScrap.predict (xTest ["Carbide Density"].values.reshape (-1,1))

accuracyCarbideDensityCrackScrap = np.where (xTest ["Total Crack Scrap"] == svmCarbideDensityCrackScrapPrediction, 1, 0)
print "Accuracy of SVM Prediction with Carbide Density as feature AND Crack Scrap as target: ", np.mean (accuracyCarbideDensityCrackScrap)




#Using Carbide MS as the SINGLE explanatory feature, and the Failure Success Class label I generated as the target, the accuracy was 84.4%
clfCarbideMS = svm.SVC ()
clfCarbideMS.fit (xTrain ["Carbide MS"].values.reshape (-1,1), xTrain ["Failure Success Class"])

svmCarbideMSPredict = clfCarbideMS.predict (xTest ["Carbide MS"].values.reshape (-1,1))

accuracyCarbideMS = np.where (xTest ["Failure Success Class"] == svmCarbideMSPredict, 1, 0)
print "Accuracy of SVM Prediction with Carbide MS as feature: ", np.mean (accuracyCarbideMS)

#Using Carbide MS as the SINGLE explanatory feature, and the Total Crack Scrap as the target, the accuracy was 76.11%
clfCarbideMSCrackScrap = svm.SVC ()
clfCarbideMSCrackScrap.fit (xTrain ["Carbide MS"].values.reshape (-1,1), xTrain ["Total Crack Scrap"])

svmCarbideMSCrackScrapPredict = clfCarbideMSCrackScrap.predict (xTest ["Carbide MS"].values.reshape (-1,1))

accuracyCarbideMSCrackScrap = np.where (xTest ["Total Crack Scrap"] == svmCarbideMSCrackScrapPredict, 1, 0)
print "Accuracy of SVM Prediction with Carbide MS as feature AND Crack Scrap as target: ", np.mean (accuracyCarbideMSCrackScrap)




#Using Carbide HC as the SINGLE explanatory feature, and the Failure Success Class label I generated as the target, the accuracy was 84.4%
clfCarbideHC = svm.SVC ()
clfCarbideHC.fit (xTrain ["Carbide HC"].values.reshape (-1,1), xTrain ["Failure Success Class"])

svmCarbideHCPredict = clfCarbideHC.predict (xTest ["Carbide HC"].values.reshape (-1,1))

accuracyCarbideHC = np.where (xTest ["Failure Success Class"] == svmCarbideHCPredict, 1, 0)
print "Accuracy of SVM Prediction with Carbide HC as feature: ", np.mean (accuracyCarbideHC)

#Using Carbide HC as the SINGLE explanatory feature, and the Total Crack Scrap as the target, the accuracy was 76.11%
clfCarbideHCCrackScrap = svm.SVC ()
clfCarbideHCCrackScrap.fit (xTrain ["Carbide HC"].values.reshape (-1,1), xTrain ["Total Crack Scrap"])

svmCarbideHCCrackScrapPredict = clfCarbideHCCrackScrap.predict (xTest ["Carbide HC"].values.reshape (-1,1))

accuracyCarbideHCCrackScrap = np.where (xTest ["Total Crack Scrap"] == svmCarbideHCCrackScrapPredict, 1, 0)
print "Accuracy of SVM Prediction with Carbide HC as feature AND Crack Scrap as target: ", np.mean (accuracyCarbideHCCrackScrap)




#Using PCD Density as the SINGLE explanatory feature, and the Failure Success Class label I generated as the target, the accuracy was 84.4%
clfPCDDensity = svm.SVC ()
clfPCDDensity.fit (xTrain ["PCD Density"].values.reshape (-1,1), xTrain ["Failure Success Class"])

svmPCDDensityPrediction = clfPCDDensity.predict (xTest ["PCD Density"].values.reshape (-1,1))

accuracyPCDDensity = np.where (xTest ["Failure Success Class"] == svmPCDDensityPrediction, 1, 0)

print "Accuracy of SVM Prediction with PCD Density as feature: ", np.mean (accuracyPCDDensity)

#Using PCD Density as the SINGLE explanatory feature, and the Total Crack Scrap as the target, the accuracy was 76.11%
clfPCDDensityCrackScrap = svm.SVC ()
clfPCDDensityCrackScrap.fit (xTrain ["PCD Density"].values.reshape (-1,1), xTrain ["Total Crack Scrap"])

svmPCDDensityCrackScrapPrediction = clfPCDDensityCrackScrap.predict (xTest ["PCD Density"].values.reshape (-1,1))

accuracyPCDDensityCrackScrap = np.where (xTest ["Total Crack Scrap"] == svmPCDDensityCrackScrapPrediction, 1, 0)

print "Accuracy of SVM Prediction with PCD Density as feature AND Crack Scrap as target: ", np.mean (accuracyPCDDensityCrackScrap)




#Using Power Avg as the SINGLE explanatory feature, and the Failure Success Class label I generated as the target, the accuracy was 84.03%
clfPowerAvg = svm.SVC ()
clfPowerAvg.fit (xTrain ["Power Avg"].values.reshape (-1,1), xTrain ["Failure Success Class"])

svmPowerAvgPrediction = clfPowerAvg.predict (xTest ["Power Avg"].values.reshape (-1,1))

accuracyPowerAvg = np.where (xTest ["Failure Success Class"] == svmPowerAvgPrediction, 1, 0)

print "Accuracy of SVM Prediction with Power Avg as feature: ", np.mean (accuracyPowerAvg)

#Using Power Avg as the SINGLE explanatory feature, and the Total Crack Scrap as the target, the accuracy was 75.80%
clfPowerAvgCrackScrap = svm.SVC ()
clfPowerAvgCrackScrap.fit (xTrain ["Power Avg"].values.reshape (-1,1), xTrain ["Total Crack Scrap"])

svmPowerAvgCrackScrapPrediction = clfPowerAvgCrackScrap.predict (xTest ["Power Avg"].values.reshape (-1,1))

accuracyPowerAvgCrackScrap = np.where (xTest ["Total Crack Scrap"] == svmPowerAvgCrackScrapPrediction, 1, 0)

print "Accuracy of SVM Prediction with Power Avg as feature AND Crack Scrap as target: ", np.mean (accuracyPowerAvgCrackScrap)




#Using TempTC Avg as the SINGLE explanatory feature, and the Failure Success Class label I generated as the target, the accuracy was 84.4%
clfTempTCAvg = svm.SVC ()
clfTempTCAvg.fit (xTrain ["TempTC Avg"].values.reshape (-1,1), xTrain ["Failure Success Class"])

svmTempTCAvgPredict = clfTempTCAvg.predict (xTest ["TempTC Avg"].values.reshape (-1,1))

accuracyTempTCAvg = np.where (xTest ["Failure Success Class"] == svmTempTCAvgPredict, 1, 0)
print "Accuracy of SVM Prediction with TempTC Avg as feature: ", np.mean (accuracyTempTCAvg)

#Using TempTC Avg as the SINGLE explanatory feature, and the Total Crack Scrap as the target, the accuracy was 76.11%
clfTempTCAvgCrackScrap = svm.SVC ()
clfTempTCAvgCrackScrap.fit (xTrain ["TempTC Avg"].values.reshape (-1,1), xTrain ["Total Crack Scrap"])

svmTempTCAvgCrackScrapPredict = clfTempTCAvgCrackScrap.predict (xTest ["TempTC Avg"].values.reshape (-1,1))

accuracyTempTCAvgCrackScrap = np.where (xTest ["Total Crack Scrap"] == svmTempTCAvgCrackScrapPredict, 1, 0)
print "Accuracy of SVM Prediction with TempTC Avg as feature AND Crack Scrap as target: ", np.mean (accuracyTempTCAvgCrackScrap)




#Using TIMEbRuns Avg as the SINGLE explanatory feature, and the Failure Success Class label I generated as the target, the accuracy was 84.4%
clfTIMEbRuns = svm.SVC ()
clfTIMEbRuns.fit (xTrain ["TIMEbRuns Avg"].values.reshape (-1,1), xTrain ["Failure Success Class"])

svmTIMEbRunsPredict = clfTIMEbRuns.predict (xTest ["TIMEbRuns Avg"].values.reshape (-1,1))

accuracyTIMEbRuns = np.where (xTest ["Failure Success Class"] == svmTIMEbRunsPredict, 1, 0)
print "Accuracy of SVM Prediction with TIMEbRuns as feature: ", np.mean (accuracyTIMEbRuns)

#Using TIMEbRuns Avg as the SINGLE explanatory feature, and the Total Crack Scrap as the target, the accuracy was 76.11%
clfTIMEbRunsCrackScrap = svm.SVC ()
clfTIMEbRunsCrackScrap.fit (xTrain ["TIMEbRuns Avg"].values.reshape (-1,1), xTrain ["Total Crack Scrap"])

svmTIMEbRunsCrackScrapPredict = clfTIMEbRunsCrackScrap.predict (xTest ["TIMEbRuns Avg"].values.reshape (-1,1))

accuracyTIMEbRunsCrackScrap = np.where (xTest ["Total Crack Scrap"] == svmTIMEbRunsCrackScrapPredict, 1, 0)
print "Accuracy of SVM Prediction with TIMEbRuns as feature AND Crack Scrap as target: ", np.mean (accuracyTIMEbRunsCrackScrap)




#Using Press as the SINGLE explanatory feature, and the Failure Success Class label I generated as the target, the accuracy was 84.4%
clfPress = svm.SVC ()
clfPress.fit (xTrain ["Press"].values.reshape (-1,1), xTrain ["Failure Success Class"])

svmPressPredict = clfPress.predict (xTest ["Press"].values.reshape (-1,1))

accuracyPress = np.where (xTest ["Failure Success Class"] == svmPressPredict, 1, 0)
print "Accuracy of SVM Prediction with Press as feature: ", np.mean (accuracyPress)

#Using Press as the SINGLE explanatory feature, and the Total Crack Scrap as the target, the accuracy was 76.11%
clfPressCrackScrap = svm.SVC ()
clfPressCrackScrap.fit (xTrain ["Press"].values.reshape (-1,1), xTrain ["Total Crack Scrap"])

svmPressCrackScrapPredict = clfPressCrackScrap.predict (xTest ["Press"].values.reshape (-1,1))

accuracyPressCrackScrap = np.where (xTest ["Total Crack Scrap"] == svmPressCrackScrapPredict, 1, 0)
print "Accuracy of SVM Prediction with Press as feature AND Crack Scrap as target: ", np.mean (accuracyPressCrackScrap)



























#Build SVM models for the dataset BROKEN UP BY SFG Description and compute prediction accuracy for the Total Crack Scrap  and Failure Success Class labels
descriptionSVMAccuracyDict = {}

clfDescription = svm.SVC ()

for description in data ["SFG Description"].unique ():

	descriptionSVMAccuracyDict [description] = []

	dataFilter = data [["Part Size", "SFG Part Family", "Total Crack Scrap","Total Starts","Bad Carbide flag","Carbide Density", "Carbide MS", "Carbide HC", "PCD Density","Power Avg","TempTC Avg","TIMEbRuns Avg","Press","Operator ID"]] [(data ["SFG Description"] == description) & (data ["Bad Carbide flag"] == "Good") & (data ["Carbide Density"].notnull ()) & (data ["Carbide MS"].notnull ()) & (data ["Carbide HC"].notnull ()) & (data ["PCD Density"].notnull ()) & (data ["Power Avg"].notnull ()) & (data ["TempTC Avg"].notnull ()) & (data ["TIMEbRuns Avg"].notnull ()) & (data ["Press"].notnull ()) & (data ["Operator ID"].notnull ())]
	
	#Compute the fraction of each batch that was labeled as failure
	dataFilter ["Failure PCT"] = dataFilter ["Total Crack Scrap"] / (1.0 * dataFilter ["Total Starts"])
	#Verify that the computation was successful
	#print "DataFilter AFTER Failure PCT: ", dataFilter.head ()




	#Create a class label that identifies as batch as either successful or failure. Failure if the batch's scrap fraction exceeded 0.025
	dataFilter ["Failure Success Class"] = np.where (dataFilter ["Failure PCT"] > 0.025, 1, 0)
	
	xTrain, xTest = train_test_split (dataFilter, test_size=0.5, random_state=5)
	
	
	if xTrain ["Failure Success Class"].nunique () > 1:
	
		clfDescription.fit (xTrain [["Part Size", "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press"]], xTrain ["Failure Success Class"])
		
		svmDescriptionPredict = clfDescription.predict (xTest [["Part Size", "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press"]])
		
		accuracyDescription = np.where (xTest ["Failure Success Class"] == svmDescriptionPredict, 1, 0)
		
		descriptionSVMAccuracyDict [description].append (np.mean (accuracyDescription))
	
	else:
		#accuracyDescription = np.where (xTest ["Failure Success Class"].reset_index(drop=True) == xTrain ["Failure Success Class"].reset_index(drop=True), 1, 0)
	
		descriptionSVMAccuracyDict [description].append ("failur class # xTrain Unique: " + str (xTrain ["Failure Success Class"].nunique ()) + "AND # xTest Unique: " + str (xTest ["Failure Success Class"].nunique ()))#+ xTrain ["Failure Success Class"].unique ());

	
	
	
	if xTrain ["Total Crack Scrap"].nunique () > 1:
	
		clfDescription.fit (xTrain [["Part Size", "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press"]], xTrain ["Total Crack Scrap"])
		
		svmDescriptionPredict = clfDescription.predict (xTest [["Part Size", "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press"]])
		
		accuracyDescription = np.where (xTest ["Total Crack Scrap"] == svmDescriptionPredict, 1, 0)
		
		descriptionSVMAccuracyDict [description].append (np.mean (accuracyDescription))
		
	else:

		descriptionSVMAccuracyDict [description].append ("crack scrap # xTrain Unique: " + str (xTrain ["Total Crack Scrap"].nunique ()) + "AND # xTest Unique: " + str (xTest ["Total Crack Scrap"].nunique ()))
	
	
	
	
	
	
print "\n\n\n\n\n\n\n\n\n\nSVM Accuracies for SFG Descrptions\n\n"

for description in descriptionSVMAccuracyDict:

	print "Description:", description, "\t\t", descriptionSVMAccuracyDict [description], "\n\n"