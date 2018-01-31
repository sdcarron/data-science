# Using the file https://dahl.byu.edu/123/2016a/hw3/report.csv, read the daily interest in lds.org for 2014-06-09 through 2014-09-06 into an data.frame.
ldsData <- read.csv ("report.csv", skip=5, nrows=90, header=FALSE)
  # I found how to read in this data set properly by referring to Dr. Dahl's
  # page: https://dahl.byu.edu/123/2016a/2016-01-14/temperatures.R
dim(ldsData)

ldsDataFrame <- data.frame (ldsData[1],ldsData[2])
ldsDataFrame
# Name the variables in the data.frame "date" and "interest".
colnames (ldsDataFrame) <- c ("date", "interest")
ldsDataFrame

# Replace the "date" character vector in the data.frame into a vector of Date objects of the same name.
ldsDataFrame$date <- as.Date(ldsDataFrame$date)

# Use the "weekdays" function to define a new variable in the data.frame called "weekday" from the "date" variable.
ldsDataFrame[3] <- weekdays (ldsDataFrame$date)
colnames (ldsDataFrame) [3] <- "weekday"
ldsDataFrame

# Find the mean of the interest variable across all Mondays.  
mean (ldsDataFrame$interest [ldsDataFrame$weekday == "Monday"])
# the mean of the interest variable across all Mondays is 26.76923

# Find the mean of the interest variable for the weekends.
mean (ldsDataFrame$interest [ldsDataFrame$weekday == "Saturday" | ldsDataFrame$weekday == "Sunday"])
# the mean of the interest variable across all weekends is 54.28

# Find the mean of the interest variable for all weekdays.
mean (ldsDataFrame$interest [ldsDataFrame$weekday != "Saturday" & ldsDataFrame$weekday != "Sunday"])
# the mean of the interest variable across all weekdays is 21.13846

# Comment on whether you believe there is a statistically significant
# difference between the mean interest on weekdays and weekends?  You don't
# have to do a formal test.  We're asking for just your intuition after seeing
# the data. Since your response won't be executable code, prefix your comments
# with R's comment character, e.g. '#'
  
  # My intuition tells me that there is a statistically significant difference
  # between the mean interest on weekdays and weekends. 

# What are the median, minimum, and maximum interest?
which.median (ldsDataFrame$interest)
  # the median of the interest variable is 22

min (ldsDataFrame$interest)
  # the min of the interest variable is 14
which.min (ldsDataFrame$interest)
  # the min of the interest variable is the 59th entry
ldsDataFrame$date [which.min (ldsDataFrame$interest)]
  # the min occurs on 2014-08-06

max (ldsDataFrame$interest)
  # the max of the interest variable is 100
which.max (ldsDataFrame$interest)
  # the max of the interest variable is the 77th entry
ldsDataFrame$date [which.max (ldsDataFrame$interest)]
  # the max occurs on 2014-08-24

# What is the correlation between interests one day apart?
ldsDataFrameFirstDayInterest <- ldsDataFrame$interest [1:89]
ldsDataFrameSecondDayInterest <- ldsDataFrame$interest [2:90]

cor (ldsDataFrameFirstDayInterest, ldsDataFrameSecondDayInterest)

  #the correlation between interests one day apart is .04974271