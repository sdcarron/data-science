#This follows the first url https://blog.sicara.com/naive-bayes-classifier-sklearn-python-example-tips-42d100429e44 https://machinelearningmastery.com/naive-bayes-classifier-scratch-python/ as a guide for developing a Naive Bayes classifier for the cracking problem
#The NB Classifier will be designed to predict whether a new cutter will be defective (have cracking) or successful (no cracking) based on its attribute values
#I think this is a Multinomial NB problem, but I'm not certain

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB



data = pd.read_csv ("C:\Users\SCarron\Desktop\compilation.csv")

#Verify that the data was read in successfully
print "Data Head: ", data.head ()


dataFilter = data [["Total Crack Scrap", "Total Starts", "Bad Carbide flag", "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press", "Operator ID"]] [(data ["Total Crack Scrap"].notnull ()) & (data ["Total Starts"] > 0 ) & (data ["Bad Carbide flag"] == "Good") & (data ["Carbide Density"].notnull ()) & (data ["Carbide MS"].notnull ()) & (data ["Carbide HC"].notnull ()) & (data ["PCD Density"].notnull ()) & (data ["Power Avg"].notnull ()) & (data ["TempTC Avg"].notnull ()) & (data ["TIMEbRuns Avg"].notnull ()) & (data ["Press"].notnull ()) & (data ["Operator ID"].notnull ())]

#Verify that the data has been filtered
print "\n\nDataFiler Head: ", dataFilter.head ()


dataFilter ["Fail PCT"] = dataFilter ["Total Crack Scrap"] / (1.0 * dataFilter ["Total Starts"])
#Verify that the Fail Percent was computed successfully
print "\n\nDataFilter with FAILURE PCT: ", dataFilter.head ()

dataFilter ["Fail Success Class"] = np.where (dataFilter ["Fail PCT"] > 0.025, 1, 0)




#print "\n\n\n\n\n\nNB predictor shape: ", dataFilter [["Carbide Density", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press"]].shape
#print "\n\n\n\n\n\nNB target shape: ", dataFilter [["Total Crack Scrap", "Success"]].shape


xTrain, xTest = train_test_split (dataFilter, test_size=0.5, random_state=5)


clfMultiNB = MultinomialNB ()
clfMultiNB.fit (xTrain [["Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press"]], xTrain [["Fail Success Class"]])
MultinomialNB (alpha=1.0, class_prior=None, fit_prior=True)


clfMultiNB.predict (xTest [["Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press"]])

print "Multinomial NB Classifier score for Crack Data: ", clfMultiNB.score (xTest [["Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press"]], xTest [["Fail Success Class"]], sample_weight=None)


clfMultiNB.fit (xTrain [["Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press"]], xTrain ["Total Crack Scrap"])
MultinomialNB (alpha=1.0, class_prior=None, fit_prior=True)

clfMultiNB.predict (xTest [["Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press"]])

print "Multinomial NB Classifier score with Total Crack Scrap as response: ", clfMultiNB.score (xTest [["Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press"]], xTest ["Total Crack Scrap"])





clfBernNB = BernoulliNB ()
clfBernNB.fit (xTrain [["Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press"]], xTrain [["Fail Success Class"]])
BernoulliNB (alpha=1.0, class_prior=None, fit_prior=True)

print "Bernoulli NB Classifier scorer for Crack Data: ", clfBernNB.score (xTest [["Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press"]], xTest [["Fail Success Class"]], sample_weight=None)













