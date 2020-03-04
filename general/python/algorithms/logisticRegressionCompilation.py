#Perform Logistic Regression (Actually Generalized Lienar Model with Binomial Outcome because respone is GROUPS of bernoulli trials) for predicting PROBABILITY of Crack Scrap

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rc ("font", size=14)
import seaborn as sns
sns.set (style="white")
sns.set (style="whitegrid", color_codes=True)
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split




data = pd.read_csv ("C:\Users\SCarron\Desktop\\reducedCompilation.csv", header=0)

#print data.head ()


#print data ['Carbide Density'].unique ()


#"1062 Crack - Edge, Interfacial", "1152 Crack - Vertical", 
dataFilter = data [["Total Crack Scrap", "Total Starts", "Bad Carbide flag", "Carbide Density", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press", "Operator ID"]] [(data ['Bad Carbide flag'] == 'Good') & (data ['Carbide Density'].notnull ()) & (data ['PCD Density'].notnull ()) & (data ["Operator ID"].notnull ()) & (data ["Press"].notnull ()) & (data ['Power Avg'].notnull ()) & (data ['TempTC Avg'].notnull ()) & (data ['TIMEbRuns Avg'].notnull ())]

#print "Count of product batches with SOME cracked AND GOOD Carbide: ", dataFilter.shape [0]





# pd.crosstab (dataFilter ["Carbide Density"], dataFilter ["Total Crack Scrap"]).plot (kind='bar')
# plt.title ("Crack Scrap against Carbide Density")
# plt.ylabel ("Crack Scrap")
# plt.xlabel ("Carbide Density")
# plt.show ()





# pd.crosstab (dataFilter ["PCD Density"], dataFilter ["Total Crack Scrap"]).plot (kind="bar")
# plt.title ("Crack Scrap against PCD Density")
# plt.ylabel ("Crack Scrap")
# plt.xlabel ("PCD Density")
# plt.show ()


#print max (dataFilter ["Total Crack Scrap"])

#print dataFilter.groupby ("Total Crack Scrap").count ()





# pd.crosstab (dataFilter ["Amps Avg"], dataFilter ["Total Crack Scrap"]).plot (kind="bar")
# plt.title ("Crack Scrap against Amps Avg")
# plt.ylabel ("Crack Scrap")
# plt.xlabel ("Amps Avg")
# plt.show ()





# pd.crosstab (dataFilter ["TIMEbRuns Avg"], dataFilter ["Total Crack Scrap"]).plot (kind="bar")
# plt.title ("Crack Scrap against Time Between Runs Avg")
# plt.ylabel ("Crack Scrap")
# plt.xlabel ("Time Between Runs Avg")
# plt.show ()


#print dataFilter ["TIMEbRuns Avg"].unique ()
print dataFilter ["Carbide Density"].unique ()



#The Scatter Plot of "Total Crack Scrap" against "Carbide Density" definitely appears to suggest a relationship (maybe exponential?), but doesn't have equal variance
#Don't care about Unequal variance (heteroscedasticity) for Logistic Regression
plt.scatter (dataFilter ["Carbide Density"], dataFilter ["Total Crack Scrap"])
plt.title ("Scatter Crack Scrap against Carbide Density")
#plt.show ()




#The Scatter Plot of "Total Crack Scrap" against "PCD Density" doesn't appear to show as much of a relationship as the one with "Carbide Density" BUT it does appear to be "bi-modal" or something like that
plt.scatter (dataFilter ["PCD Density"], dataFilter ["Total Crack Scrap"])
plt.title ("Scatter Crack Scrap against PCD Density")
#plt.show ()


#The Scatter Plot of "Total Crack Scrap" against "Power Avg" looks to have some kind of a relationship (Large cluster in the middle, but tapers at either end)
plt.scatter (dataFilter ["Power Avg"], dataFilter ["Total Crack Scrap"])
plt.title ("Scatter Crack Scrap against Power Avg")
#plt.show ()


#The Scatter Plot of "Total Crack Scrap" against "TIMEbRuns Avg" looks to have maybe a exponential decreasing relationship?
plt.scatter (dataFilter ["TIMEbRuns Avg"], dataFilter ["Total Crack Scrap"])
plt.title ("Scatter Crack Scrap against TIMEbRuns Avg")
#plt.show ()


#The Scatter Plot of "Total Crack Scrap" against "TempTC Avg" looks to have maybe  a exponential increasing relationship?
plt.scatter (dataFilter ["TempTC Avg"], dataFilter ["Total Crack Scrap"])
plt.title ("Scatter Crack Scrap against TempTC Avg")
#plt.show ()




plt.scatter (dataFilter ["Press"], dataFilter ["Total Crack Scrap"])
plt.title ("Scatter Crack Scrap against Press")
#plt.show ()


plt.scatter (dataFilter ["Operator ID"], dataFilter ["Total Crack Scrap"])
plt.title ("Scatter Crack Scrap against Operator ID")
#plt.show ()





#Carbide Density may be normally distributed, but just have a very small variance
dataFilter ["Carbide Density"].hist ()
plt.title ("Histogram of Carbide Density Dist")
#plt.show ()

print "\n\nCarbide Density variance: ", dataFilter ["Carbide Density"].var ()


# dataFilter ["Carbide Density"].hist ()
# plt.xlim (xmin=14.05, xmax=14.36)
# plt.title ("Histogram of Carbide Density Dist w/ Reduced X range")
# plt.show ()

#PCD Density does not appear to be noramlly distributed, but it does have 2 modes. Could be bi modal normal with a very small variance?
dataFilter ["PCD Density"].hist ()
plt.title ("Histogram of PCD Density Dist")
#plt.show ()

print "\n\nPCD Density variance: ", dataFilter ["PCD Density"].var ()

#Power is fairly normally distributed
dataFilter ["Power Avg"].hist ()
plt.title ("Histogram of Power Avg Dist")
#plt.show ()

print "\n\nPower Avg variance: ", dataFilter ["Power Avg"].var ()

#TIMEbRuns Avg is not normally distributed. Looks like an exponenital or gamma with the skewness
dataFilter ["TIMEbRuns Avg"].hist ()
plt.title ("Histogram of TIMEbRuns Avg Dist")
#plt.show ()


#I considered performing a Log Transform on both TIMEbRuns and TempTC, but because they contain observatiobns that have value of 0, when transformed that results in Negative Infinity, and Histograms can't be made with that
# logTIMEbRuns = dataFilter ["TIMEbRuns Avg"].apply (np.log)
# # logTIMEbRuns.hist ()
# # plt.title ("Histogram of LOG TIMEbRuns Avg")
# # plt.show ()
# print "\n\nLOG TIMEbRuns: ", logTIMEbRuns


#TempTC Avg is not normally distributed. Looks like an exponential or gamma with the skewness
dataFilter ["TempTC Avg"].hist ()
plt.title ("Histogram of TempTC Avg Dist")
#plt.show ()







dataFilter ["Press"].hist ()
plt.title ("Histogram of Press Dist")
#plt.show ()



dataFilter ["Operator ID"].hist ()
plt.title ("Histogram of Operator ID Dist")
#plt.show ()













#Convert the RESPONSE "Total Crack Scrap" into BINARY form for Logistic Regression
#This doesn't work... not sure why the division in the lambda function with an if clause ISN'T working dataFilter dataFilter ["Scrap Binary"] = ["Total Crack Scrap"].apply (lambda x: (x/x) if x > 0)
# dataFilter ["Scrap Binary"] = np.where (dataFilter ["Total Crack Scrap"] > 0, 1, 0)


# print "\n\n Data Filter after casting Scrap to Binary: ", dataFilter ["Scrap Binary"].head ()
# print "\n\n Unique Values for Scrap Binary: ", dataFilter ["Scrap Binary"].unique ()








#Because the response variable is presented in Succes/Failure COUNTS (grouped data) rather than SINGLE OBSERVATION Binary Outcome, the approach is to use a Generalized Linear Model with Binomial Response Data
#http://www.statsmodels.org/stable/examples/notebooks/generated/glm.html

#I will need to convert the data from a Pandas Dataframe into a Numpy ndarray in order to use the GLM with Binomial Outcome in statsmodels
import numpy as np
import statsmodels.api as sm
from scipy import stats
import matplotlib.pyplot as plt

#Construct a new column (Difference between Total Crack Scrap and Total Starts) in order to have the Binomial Outcome DEPENDENT OUTCOME we need (Failure = Total Crack Scrap, Success = Total Starts - Total Crack Scrap)
dataFilter ["Failure"] = dataFilter ["Total Crack Scrap"]
dataFilter ["Success"] = dataFilter ["Total Starts"] - dataFilter ["Total Crack Scrap"]

#I thought the above two lines of code weren't working properly because the first row from the data file was NOT appearing as the first row in the dataframe dataFilter. This is becauase the first row from the DATA FILE
#DOES NOT have a value for Carbide, so it is not ever included in the dataFilter dataframe
# print "\n\nHead Total Crack Scrap: ", dataFilter ["Total Crack Scrap"].head ()
# print "\n\nHead Total Starts: ", dataFilter ["Total Starts"].head ()
# print "\n\nHead Binomial FAILURE outcome: ", dataFilter ["Failure"].head ()
# print "\n\nHead Binomial SUCCESS outcome: ", dataFilter ["Success"].head ()


# print "\n\nTotal Crack Scrap idx 0: ", dataFilter["Total Crack Scrap"].iloc [0]
# print "\n\nFAILURE idx 0: ", dataFilter ["Failure"].iloc [0]
# print "\n\nSUCCESS idx 0: ", dataFilter ["Success"].iloc [0]


# print "\n\nidx where Failure = 3", dataFilter.index [dataFilter ["Total Crack Scrap"] == 3]

# print "\n\nData Set Line 358: ", dataFilter.ix [358]





#Create a dummy variable for Operator ID NOTE: This isn't working for some reason... get "ValueError: Wrong number of items passed 99, placement implies 1
#dataFilter ["Dummy Operator ID"] = pd.get_dummies (dataFilter ["Operator ID"])

dfBinomDependent = dataFilter [["Failure", "Success"]]
print "\n\nHead dfBinomDependent: ", dfBinomDependent.head ()


dfBinomIndependent = dataFilter [["Carbide Density", "PCD Density", "Power Avg", "TempTC Avg", "Press", "Operator ID"]] # "TIMEbRuns Avg", 
print "\n\nHead dfBinomIndependent: ", dfBinomIndependent.head ()




#Convert the Dependent and Independent Pandas dataframes into Numpy Arrays so that the GLM Binomial Guide (url posted on line 217) can be used
arrayBinomDependent = dfBinomDependent.values#as_matrix ()#values ()
arrayBinomIndependent = dfBinomIndependent.values#as_matrix ()#values ()

# print type (dfBinomDependent)
# print type (dfBinomIndependent)

#Numpy ndarrays do not have a method called "head", but the arrays created ABOVE ARE Numpy ndarrays, so now the GLM model can be built
# print "\n\nHead arrayBinomDependent: ", arrayBinomDependent.head ()
# print "\n\nHead arrayBinomIndependent: ", arrayBinomIndependent.head ()



glmBinom = sm.GLM (arrayBinomDependent, arrayBinomIndependent, family=sm.families.Binomial ())
fit = glmBinom.fit ()
print "\n\nGLM Fit Summary: \n\n", fit.summary ()

prediction = fit.fittedvalues

#This url discusses obtaining the information about Goodness of Fit for a GLM https://stats.stackexchange.com/questions/46345/how-to-calculate-goodness-of-fit-in-glm-r
# plt.scatter (prediction, fit.resid) #a glmresults object doesn't contain a "resid" attribute (resid = residuals)
# plt.title ("Predicted Values against Residuals")
# plt.show ()

#What do the resutls for the GLM mean though?





#Interesting plots obtained from the results
#nobs = fit.nobs ()
y = arrayBinomDependent [:,0] / arrayBinomDependent.sum (1) #This SHOULD take each value in the FIRST column and then divide it by the SUM of the value in the first and second columns, but it's not working for some reason

#print type (arrayBinomDependent)

# y = []
# for row in dfBinomDependent:
	# y.append (row [0] / sum (row [0], row [1]))
	
yhat = fit.mu

from statsmodels.graphics.api import abline_plot

fig, ax = plt.subplots ()
ax.scatter (yhat, y)
line_fit = sm.OLS (y, sm.add_constant (yhat, prepend=True)).fit ()
abline_plot (model_results=line_fit, ax=ax)

ax.set_title ("Model Fit Plot")
ax.set_ylabel ("Observed Values")
ax.set_xlabel ("Fitted Values")

plt.show ()



print np.where (arrayBinomDependent [:,1] == 0)#arrayBinomDependent [:,1]) #Trying to find what point corresponds to the Observed Y value of 1.0 on the plot of "y vs yhat"
print arrayBinomDependent [366,:] #In row 366, apparently ALL of the products were Crack Scrap

print yhat [366] #For some reason the predicted value for point 366 is WAY off... predicted value is .02 and observed value is 1.0


# print fit.mu
# print type (fit.mu)
# print fit.mu.shape


#I was working on computing R^2 for the GLM, but learned that R^2 doesn't make sense as a measure for goodness of fit for GLM UNLESS the errors are Gaussian AND the link function is the identity function
# print "Data type of predicted values container: ", type (prediction)
# residuals = prediction - arrayBinomDependent

# plt.hist (residuals, bins=10)
# plt.title ("Histogram of Logistic Regression Residuals")
# plt.show ()