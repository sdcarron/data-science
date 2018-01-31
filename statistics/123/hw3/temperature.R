# Make a list containing three elements named "y2011", "y2012", and "y2013"
# containing three data.frames of weather information for years 2011, 2012, and
# 2013 in Provo.  Use the Weather Underground website as shown in lecture.

webpage2011 <- "http://www.wunderground.com/history/airport/PVU/2011/1/1/CustomHistory.html?dayend=31&monthend=12&yearend=2011&req_city=NA&req_state=NA&req_statename=NA"
webpage2012 <- "http://www.wunderground.com/history/airport/PVU/2012/1/1/CustomHistory.html?dayend=31&monthend=12&yearend=2012&req_city=NA&req_state=NA&req_statename=NA"
webpage2013 <- "http://www.wunderground.com/history/airport/PVU/2013/1/1/CustomHistory.html?dayend=31&monthend=12&yearend=2013&req_city=NA&req_state=NA&req_statename=NA"

url2011 <- paste(webpage2011,"&format=1",sep="")
url2012 <- paste(webpage2012,"&format=1",sep="")
url2013 <- paste(webpage2013,"&format=1",sep="")


filename2011 <- "weather-PVU-2011.txt"
filename2012 <- "weather-PVU-2012.txt"
filename2013 <- "weather-PVU-2013.txt"

download.file(url2011,filename2011,method="curl")
download.file(url2012,filename2012,method="curl")
download.file(url2013,filename2013,method="curl")

  # For right now, the following 3 commands are only pulling in info for January
  # How do I pull info for all 12 months into each corresponding table?
weather2011 <- read.table (filename2011,skip=1,sep=",",header=TRUE,as.is=TRUE)
weather2012 <- read.table (filename2012,skip=1,sep=",",header=TRUE,as.is=TRUE)
weather2013 <- read.table (filename2013,skip=1,sep=",",header=TRUE,as.is=TRUE)

  # Can the following 3 commands be taken care of above, by reading the info in
  # as "data.frame" instead of "read.table"?
weatherDF2011 <- data.frame (weather2011)
weatherDF2012 <- data.frame (weather2012)
weatherDF2013 <- data.frame (weather2013)

weatherDataFramesList <- list ("y2011"=weatherDF2011, "y2012"=weatherDF2012, "y2013"=weatherDF2013)

# How many days in 2011 had a maximum temperature above 90 degrees?  Watch out, there may be missing values!
  #head (weatherDataFramesList)
  #head (weatherDataFramesList [[1]])
  #weatherDataFramesList [[1]]
  #weatherDataFramesList$weatherDF2011

head(weatherDataFramesList$y2011)
weatherDataFramesList$y2011$Max.TemperatureF
sum (weatherDataFramesList$y2011$Max.TemperatureF > 90, na.rm=TRUE)
  #31 days in 2011 had a maximum temperature above 90 degrees

# How many days in 2012 had a maximum temperature above 90 degrees?
weatherDataFramesList$y2012$Max.TemperatureF
sum (weatherDataFramesList$y2012$Max.TemperatureF > 90, na.rm=TRUE)
  #42 days in 2012 had a maximum temperature above 90 degrees

# How many days in 2013 had a maximum temperature above 90 degrees?
weatherDataFramesList$y2013$Max.TemperatureF
sum (weatherDataFramesList$y2013$Max.TemperatureF > 90, na.rm=TRUE)
  #48 days in 2013 had a maximum temperature above 90 degrees