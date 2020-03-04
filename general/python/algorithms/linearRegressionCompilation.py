#Perform Multiple Linear Regression for predicting the NUMBER of cutters that will be deemed Crack Scrap

#This follows the example for building Linear Regression models found at url https://towardsdatascience.com/simple-and-multiple-linear-regression-in-python-c928425168f9
#The above url states that statsmodels AND sklearn are the best libraries for building linear regression models

import numpy as np
import sklearn as sk 
import pandas as pd
import statsmodels.api as sm #This is the FIRST library used for building a linear regression model in the url above

import matplotlib.pyplot as plt


#In the above url, they place the predictor (independent) variables in one Pandas dataframe and the response (dependent) variable in a separate Pandas dataframe

data = pd.read_csv ("C:\Users\SCarron\Desktop\compilation.csv")

#I ended up selecting ONLY the observations for which "Total Crack Scrap" > 0 based because with the 0 values in there, even transforming the data with Box-Cox wasn't helping.
#Refer to this Publication for information about the difficulties of performing regression with response data that includes "clumping" or "high proportion" of values a 0:
#http://users.stat.ufl.edu/~aa/articles/min_agresti_2002.pdf
dataFilter = data [["Total Crack Scrap","Total Starts","Bad Carbide flag","Carbide Density","PCD Density","Power Avg","TempTC Avg","TIMEbRuns Avg","Press", "Year-Month Press"]] [(data ["Total Crack Scrap"] > 0) & (data ["Bad Carbide flag"] == "Good") & (data ["Carbide Density"].notnull ()) & (data ["PCD Density"].notnull ()) & (data ["Operator ID"].notnull ()) & (data ["Press"].notnull ()) & (data ["Power Avg"].notnull ()) & (data ["TempTC Avg"].notnull ()) & (data ["TIMEbRuns Avg"].notnull ())]

yearMonthOrdinalDict = {"2017-01": 1, "2017-02": 2, "2017-03": 3, "2017-04": 4, "2017-05": 5, "2017-06": 6, "2017-07": 7, "2017-08": 8, "2017-09": 9, "2017-10": 10, "2017-11": 11, "2017-12": 12, "2018-01": 13, "2018-02": 14, "2018-03": 15, "2018-04": 16, "2018-05": 17, "2018-06": 18}
dataFilter ["Year-Month Ordinal"] = dataFilter ["Year-Month Press"].map (yearMonthOrdinalDict)
dataFilter.columns = ["Scrap","Starts","Flag","CDensity","PDensity","PAvg","TempAvg","TimeAvg","Press","YMPress","YMOrdinal"]


#print "Data type of Year-Month Press", type (dataFilter ["Year-Month Press"])

# dataFilter ["Operator Ordinal"] = pd.Categorical (dataFilter ["Operator ID"])
# yearMonthSplit = dataFilter ["Year-Month Press"].str.split ("-")
# yearMonthSplitDate = 

#print "Year-Month Split Head:", yearMonthSplit.head ()

# print "Just made Year-Month Split Month: ", dataFilter ["Year-Month Split Month"]
# print "Just made Year-Month Split Year: ", dataFilter ["Year-Month Split Year"]

# dataFilter ["Pct Scrap"] = dataFilter ["Total Crack Scrap"] / dataFilter ["Total Starts"]

# print "Pct Scrap Head: ", dataFilter ["Pct Scrap"].head ()

# dataFilter ["Pct Scrap"].hist ()
# plt.title ("Histogram of PCT Scrap")
# plt.show ()


# #Verify that the data has been read in properly from the data file
# print "Total Data Head: ", data.head ()

print "Filter Data Head: ", dataFilter.head ()



#Set up the variables into a PREDICTOR df and a RESPONSE/TARGET df
predictorDF = dataFilter.loc [:, (dataFilter.columns.values != "Scrap") & (dataFilter.columns.values != "Flag") & (dataFilter.columns.values != "Operator ID") & (dataFilter.columns.values != "YMPress")] #  & (dataFilter.columns.values != "PCD Density") & (dataFilter.columns.values != "Press") & (dataFilter.columns.values != "TempTC Avg") #  & (dataFilter.columns.values != "Total Starts") & (dataFilter.columns.values != "Carbide Density")  # & (dataFilter.columns.values != "Total Starts") & (dataFilter.columns.values != "TIMEbRuns Avg")  #Could alternatively use the Pandas Dataframe "drop" method "df.drop ()"

#Verify that the selection was successful
#print "Predictor Variables DF Head: ", predictorDF.head ()
# print "Year Ordinal Head: ", predictorDF ["Year-Month Ordinal"].head ()
# print "\n\n\nOpertor Ordinal: ", predictorDF ["Operator Ordinal"].head ()


responseDF = dataFilter.loc [:, dataFilter.columns.values == "Scrap"]

#Verify that the selection was successful
print "Response Variable DF Head: ", responseDF.head ()



#"Diamond Powder Lot", "Carbide Powder Lot", "Year-Month Press"
# diamondLotUnique = data ["Diamond Powder Lot"].unique ()

# data.hist ("Diamond Powder Lot", weights=data ["Total Crack Scrap"])
# plt.title ("Total Crack Scarp against Diamond Powder Lot")
# plt.show ()


# carbideLotUnique = data ["Carbide Powder Lot"].unique ()

# data.hist ("Carbide Powder Lot", weights=data ["Total Crack Scrap"])
# plt.title ("Total Crack Scrap against Carbide Powder Lot")
# plt.show ()


# yearmonthUnique = data ["Year-Month Press"].unique ()

# data ["Year-Month Date"] = pd.to_datetime (data ["Year-Month Press"])

# plt.scatter (data ["Year-Month Date"], data ["Total Crack Scrap"])
# plt.title ("Total Crack Scrap against Year-Month Press")
# plt.show ()









#Build the FIRST Multiple Linear Regression model using the statsmodels library imported above
modelSM = sm.OLS (responseDF.astype (float), predictorDF.astype (float)).fit ()

prediction = modelSM.predict (predictorDF)
print "modelSM Summary: ", modelSM.summary () #Obviously this model has some major problems. I believe this is largely due to the fact that some of the Independent Variables do not have a linear relationship with the response



#Plot the Response variable against EACH Independent Variable to show the problems with some of the relationships (not being linear)
# plt.scatter (predictorDF ["Total Starts"], responseDF)
# plt.title ("Total Crack Scrap against Total Starts")
# plt.show ()

plt.scatter (predictorDF ["TimeAvg"], responseDF)
plt.title ("Total Crack Scrap against TIMEbRuns Avg")
plt.show ()

# plt.scatter (predictorDF ["TempTC Avg"], responseDF)
# plt.title ("Total Crack Scrap against TempTC Avg")
# plt.show ()

# plt.scatter (predictorDF ["Carbide Density"], responseDF)
# plt.title ("Total Crack Scrap against Carbide Density")
# plt.show ()

# plt.scatter (predictorDF ["PCD Density"], responseDF)
# plt.title ("Total Crack Scrap against PCD Density")
# plt.show ()

plt.scatter (predictorDF ["PAvg"], responseDF)
plt.title ("Total Crack Scrap against Power Avg")
plt.show ()


# plt.scatter (predictorDF [""], responseDF)
# plt.title ("Total Crack Scrap against ")
# plt.show ()

plt.scatter (prediction, responseDF)
plt.title ("Observed Values against Predicted")
plt.show ()


plt.scatter (prediction, modelSM.resid)
plt.title ("Residual against Predicted")
plt.show ()







# modelSM.resid.hist ()
# plt.title ("Histogram of Residuals")
# plt.show ()


logTransformResponse = (responseDF).apply (np.log)
logTransformResponse.hist ()
plt.title ("Histogram of Total Crack Scrap")
plt.show ()

from scipy import stats
transformedResponse = np.asarray (responseDF) #WITHOUT the "+1" the r^2 is .544 and WITH the "+1" the r^2 is .934.... WHY?! I removed the "+1" because all it was doing was adding 1 to the original response values

#print "Transformed Response Head: ", transformedResponse [0:6]

dft = stats.boxcox (transformedResponse) [0]

plt.hist (dft, bins=100)
plt.title ("Histogram of Box-Cox Transformed Total Crack Scrap")
plt.show ()



plt.scatter (predictorDF ["CDensity"], dft)
plt.title ("Box-Cox Tranformed Response against Carbide Density")
plt.show ()

plt.scatter (predictorDF ["PAvg"], dft)
plt.title ("Box-Cox Transformed Response against Power Avg")
plt.show ()

plt.scatter (predictorDF ["TimeAvg"], dft)
plt.title ("Box-Cox Transformed Response against TIMEbRuns Avg")
plt.show ()


# plt.scatter (predictorDF ["Total Starts"], dft)
# plt.title ("Box-Cox Transformed Total Crack Scrap against Total Starts")
# plt.show ()

# plt.scatter (predictorDF ["TIMEbRuns Avg"], dft)
# plt.title ("Box-Cox Transformed Total Crack Scrap against TIMEbRuns Avg")
# plt.show ()

# plt.scatter (predictorDF ["TempTC Avg"], dft)
# plt.title ("Box-Cox Transformed Total Crack Scrap against TempTC Avg")
# plt.show ()

# plt.scatter (predictorDF ["Carbide Density"], dft)
# plt.title ("Box-Cox Transformed Total Crack Scrap against Carbide Density")
# plt.show ()

# plt.scatter (predictorDF ["PCD Density"], dft)
# plt.title ("Box-Cox Transformed Total Crack Scrap against PCD Density")
# plt.show ()

# plt.scatter (predictorDF ["Power Avg"], dft)
# plt.title ("Box-Cox Transformed Total Crack Scrap against Power Avg")
# plt.show ()



modelTransformSM = sm.OLS (dft, predictorDF.astype (float)).fit ()

predictionTransform = modelTransformSM.predict (predictorDF)
print "Transformed Response Model summary: ", modelTransformSM.summary ()


transformPredicted = modelTransformSM.fittedvalues
transformResid = modelTransformSM.resid

plt.scatter (transformPredicted, transformResid)
plt.title ("TRANSFORM Predicted against TRANSFORM Resid")
plt.show ()






# densityCount = data ["Carbide Density"].value_counts ()
# print "Carbide Density value counts: ", densityCount



# densityByDate = dataFilter [["Carbide Density", "Year-Month Press", "Total Crack Scrap"]].groupby ("Year-Month Press")
# print "Density By Date: ", densityByDate ["Carbide Density"].value_counts ()


# crackScrapByDensityDate = dataFilter [["Total Crack Scrap", "Carbide Density", "Year-Month Press"]].groupby (["Year-Month Press", "Carbide Density"])
# print "Crack Scrap by Carbide Density by Date: ", crackScrapByDensityDate.sum ()



import statsmodels.formula.api as smf
dataFilter ["DFTScrap"] = dft
interactionModel = smf.ols (formula='DFTScrap~Starts + CDensity + PDensity + PAvg + TempAvg + TimeAvg + YMOrdinal - 1', data=dataFilter).fit () # + CDensity*YMOrdinal

print "Interaction Model Summary: ", interactionModel.summary ()




# plt.scatter (dataFilter ["YMOrdinal"], dataFilter ["LogScrap"])
# plt.title ("Scrap against Ordinal Date")
# plt.show ()