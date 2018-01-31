# Load the mtcars dataset that comes preinstalled in R.
mtcarsDataFrame <- mtcars
mtcarsDataFrame

# Find the mean of the miles per gallon variable.
mean (mtcarsDataFrame$mpg)
  # the mean of the miles per gallon variable is 20.09062


# Compute the linear correlation between the "mpg" and "cyl" variables.
with (mtcarsDataFrame, cor (mpg, cyl))
  # the linear correlation between "mpg" and "cyl" is -.852162

# Compute the linear correlation between the "mpg" and "gear" variables.
with (mtcarsDataFrame, cor (mpg, gear))
  # the linear correlation between "mpg" and "gear" is .4802848


# Find the mean of the "mpg" variable for each value of the "gear" variable.
mean (mtcarsDataFrame$mpg [mtcarsDataFrame$gear == 3])
  # mean mpg for 3 gear vehicles is 16.10667
mean (mtcarsDataFrame$mpg [mtcarsDataFrame$gear == 4])
  # mean mpg for 4 gear vehicles is 24.5333
mean (mtcarsDataFrame$mpg [mtcarsDataFrame$gear == 5])
  # mean mpg for 5 gear vehicels is 21.38

# Find the median of the "mpg" variable for each value of the "gear" variable.
median (mtcarsDataFrame$mpg [mtcarsDataFrame$gear == 3])
  # median mpg for 3 gear vehicles is 15.5
median (mtcarsDataFrame$mpg [mtcarsDataFrame$gear == 4])
  # median mpg for 4 gear vehicles is 22.8
median (mtcarsDataFrame$mpg [mtcarsDataFrame$gear == 5])
  # median mpg for 5 gear vehicles is 19.7

# Find the make and model of the car with the highest miles per gallon.  What are its "cyl" and "gear" values?
which.max (mtcarsDataFrame$mpg)
  # the car with the highest miles per gallon (33.9) is Toyota Corolla
  # it is the 20th entry in the table

mtcarsDataFrame$cyl [which.max (mtcarsDataFrame$mpg)]
  # the Toyota Corolla, which has the highest mpg, has 4 cylinders

mtcarsDataFrame$gear [which.max (mtcarsDataFrame$mpg)]
  # the Toyota Corolla, which has the highest mpg, has 4 gears