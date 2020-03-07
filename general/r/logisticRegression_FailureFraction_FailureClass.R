data <- read.csv ("C:\\Users\\SCarron\\Desktop\\compilation.csv", header=TRUE)

#Verify that the data was read in succesfully
head (data)


#Filter out variables of interest
dataFilter <- subset (data, select=c ("Total.Crack.Scrap", "Total.Starts", "Bad.Carbide.flag", "Carbide.Density", "Carbide.MS", "Carbide.HC", "PCD.Density", "Power.Avg", "TempTC.Avg", "TIMEbRuns.Avg", "Press", "Operator.ID"))
head (dataFilter)

#Filter out an Null or NA values
dataFilter <- dataFilter [dataFilter$Bad.Carbide.flag == 'Good' & !is.na (dataFilter$Carbide.Density) & !is.na (dataFilter$Carbide.MS) & !is.na (dataFilter$Carbide.HC) & !is.na (dataFilter$PCD.Density) & !is.na (dataFilter$Power.Avg) & !is.na (dataFilter$TempTC.Avg) & !is.na (dataFilter$TIMEbRuns.Avg) & !is.na (dataFilter$Press) & !is.na (dataFilter$Operator.ID),]
head (dataFilter)



#Compute the Crack Failure Fraction
dataFilter$Failure.PCT <- dataFilter$Total.Crack.Scrap / dataFilter$Total.Starts
head (dataFilter)



#Create the Class Labels based on the Crack Failure Fractions (0 if Failure.PCT <= 0.025, 1 if Failure.PCT > 0.025)
dataFilter$Failure.Success.Class <- cbind (ifelse (dataFilter$Failure.PCT > 0.025, 1, 0))
head (dataFilter)
tail (dataFilter)

#Look for correlation between variables
#pairs (dataFilter)

#Look at the Denisty plots for the variables
# library (caret)
# X <- subset (dataFilter, select=c ("Carbide.Density", "PCD.Density", "Power.Avg", "TempTC.Avg", "TIMEbRuns.Avg"))
# Y <- subset (dataFilter, select=c ("Failure.Success.Class"))
# scales <- list (X=list (relation="free"), Y=list (relation="free"))
# featurePlot (x=X, y=Y, plot="density", scales=scales)


glmBernoulli <- glm ("Failure.Success.Class~Carbide.Density + Carbide.MS + Carbide.HC + Power.Avg  + TempTC.Avg  + TIMEbRuns.Avg + Press - 1", family=binomial (logit), data=dataFilter)# + PCD.Density 
summary (glmBernoulli)

pchisq (deviance (glmBernoulli), 4390, lower=F)


#I believe the hosmer-lemeshow test suggests that the frequency of Failure.Success.Class = 1 is NOT the same throughout the data
#(last entry on ) https://stats.stackexchange.com/questions/169438/evaluating-logistic-regression-and-interpretation-of-hosmer-lemeshow-goodness-of
#This may be related to what I discovered in the difference of Failure.Success.Class = 1 for below 1150 and above 1150 at the bottom of the script
library (ResourceSelection)
hoslem.test (glmBernoulli$y, fitted (glmBernoulli))

plot (dataFilter$Carbide.Density, dataFilter$Failure.PCT, xlab="Carbide Density", ylab="Failure PCT")
plot (dataFilter$Carbide.MS, dataFilter$Failure.PCT, xlab="Carbide MS", ylab="Failure PCT")
plot (dataFilter$Carbide.HC, dataFilter$Failure.PCT, xlab="Carbide HC", ylab="Failure PCT")
plot (dataFilter$Power.Avg, dataFilter$Failure.PCT, xlab="Power Avg", ylab="Failure PCT")
plot (dataFilter$TempTC.Avg, dataFilter$Failure.PCT, xlab="TempTC Avg", ylab="Failure PCT")
plot (dataFilter$TIMEbRuns.Avg, dataFilter$Failure.PCT, xlab="TIMEbRuns Avg", ylab="Failure PCT")
plot (dataFilter$Press, dataFilter$Failure.PCT, xlab="Press", ylab="Failure PCT")
plot (dataFilter$PCD.Density, dataFilter$Failure.PCT, xlab="PCD Density", ylab="Failure PCT")



sum (dataFilter$TempTC.Avg > 1200, rm.na=TRUE)
nrow (dataFilter)


dataAbove1200 <- dataFilter [dataFilter$TempTC.Avg > 1200,]
head (dataAbove1200)

sum (dataAbove1200$Failure.Success.Class == 1)
mean (dataAbove1200$Failure.Success.Class)

meanFailPctAbove1200 <- mean (dataAbove1200$Failure.PCT)
mean (dataAbove1200$Failure.PCT > meanFailPctAbove1200)

dataBelow1200 <- dataFilter [dataFilter$TempTC.Avg < 1200,]
head (dataBelow1200)
sum (dataBelow1200$Failure.Success.Class == 1)
nrow (dataBelow1200)
mean (dataBelow1200$Failure.Success.Class)
meanFailPctBelow1200 <- mean (dataBelow1200$Failure.PCT)
mean (dataBelow1200$Failure.PCT > meanFailPctBelow1200)


sum (dataFilter$TempTC.Avg < 1150)
dataBelow1150 <- dataFilter [dataFilter$TempTC.Avg < 1150,]
mean (dataBelow1150$Failure.Success.Class == 1)



dataAbove1150 <- dataFilter [dataFilter$TempTC.Avg >= 1150,]
mean (dataAbove1150$Failure.Success.Class == 1)








# linearModel <- lm ("Failure.PCT~ TempTC.Avg  - 1", data=dataFilter) #Carbide.Density + Power.Avg ++ TIMEbRuns.Avg
# summary (linearModel)
# 
# hist (dataFilter$Failure.PCT)
