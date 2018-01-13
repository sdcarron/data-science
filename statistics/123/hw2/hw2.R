x <- c(6,3,8,5,5,7,5,7,6,2,5,5,6,6,2,4,5,3,5,4,5,2,5,4,6,9,6,4,
       7,1,6,5,3,6,5,4,2,3,5,2,6,12,8,2,5,1,2,4,9,3,3,6,2,9,4,3,
       8,8,3,4,6,8,7,10,3,7,4,3,3,3,1,11,5,4,10,8,4,7,5,4,6,2,6,
       6,5,7,2,2,1,6,2,4,5,3,8,5,4,6,9,5,4,4,6,6,6,6,5,5,5,7,6,
       4,4,5,4,3,2,3,6,5,7,5,6,2,7,6,3,2,7,5,4,4,7,4,6,4,3,4,9,6,
       5,8,2,3,7,1,10,8,5,7,4,4,7,5,4,4,4,3,2,7,5,7,3,3,3,4,3,3,
       7,7,4,11,4,5,4,4,5,7,4,9,6,8,7,6,6,3,7,6,5,5,3,6,2,4,2,5,
       6,7,10,5,8,4,7,8,3,4,1,6,6,3,5,5,2,2,1,3,5,3,5,3,2,5,3,5,
       8,3,2,6,3,12,3,4,3,7,8,8,5,4,4,5,5,7,5,8,4,5,3,3,7,6,7,2,
       4,5,5,5,5,1,4,4,4,6,1,2,5,2,5,8,3,8,5,4,6,5,2,5,3,7,6,6,
       4,6,6,3,7,6,5,4,2,12,3,8,5,4,9,4,4,5,5,4,8,4,6,5,6,3,12,6,
       2,7,8,4,3,5,5,5,2,3,5,7,6,6,4,4,5,7,4,3,7,4,3,2,3,4,2,7,4,
       4,5,6,1,4,4,3,6,6,5,8,6,1,3,2,7,2,6,5,6,5,7,4,2,4,6,6,6,6,
       5,4,9,4,7,2,2,8,3,10,7,6,7,9,6,6,4,2,2,7,8,5,7,6,0,3,5,1,
       4,1,8,2,6,3,7,5,3,3,1,8,6,4,7,4,8,4,4,6,8,4,5,7,9,7,4,0,2,
       2,6,4,3,6,7,7,9,8,8,9,7,4,8,6,8,10,5,6,1,4,3,9,7,4,6,7,6,
       5,5,3,1,5,4,7,3,4,2,7,4,5,3,9,8,7,3,9,9,4,7,8,4,4,4,5,6,7,
       5,11,6,3,4,0,4,5,3,5,6,5,4,5,5,1,4,3,5,3)
y <- x
set.seed(944452)
y[sample(length(x),10)] <- NA



# What is the length of the x vector?
length (x)
# X has 500 elements



# Find the sum of the numbers in the x vector.
sum (x)
# The sum of x's elements is 2495



# Find the mean of the numbers in the x vector using two methods:
# 1. the 'mean' function in R and
# 2. the 'sum' function and definition of the mean.
mean (x)
# mean of elements in x is 4.99

sum (x) / length (x)
# mean of elements in x is 4.99



# Find the standard deviation in the x vector using two methods:
# 1. the 'sd' function in R and
# 2. the 'sum' and 'mean' functions and definition of the standard deviation.

sd (x) 
# x's standard deviation is 2.192605

x_Diff_From_Mean <- x - mean (x)
x_Diff_From_Mean

sdCalculated <- sqrt (sum (x_Diff_From_Mean ^ 2) / (length (x) - 1))
sdCalculated
# x's standard deviation is 2.192605



# Find the standard deviation of the first 50 numbers in the x vector.
sd (x[1:50])
# the standard deviation of x's first 50 elements is 2.210273




# Find the sum of numbers in the x vector whose position is even (e.g., x[2] + x[4] + ...)
x_Even_Indexes <- c((1:500) %% 2 == 0)
x_Even_Indexes
sum (x[x_Even_Indexes == TRUE])
# the sum of x's elements located at even index positions is 1258



# Find the sum of the even numbers in the x vector.
x_Even_Value_Indexes <- c (x %% 2 == 0)
sum (x[x_Even_Value_Indexes == TRUE])
# the sum of x's even-valued elements is 1274



# Find the mean of the values of the x vector that are not more than 10.
x_Less_Than_10_Value_Indexes <- c (x < 10)
x_Less_Than_10_Value_Indexes

mean (x[x_Less_Than_10_Value_Indexes == TRUE])
# mean of x's elements with values less than 10 is 4.833676




# What is mean of the y vector (excluding missing values)?
# Show two solutions, one that excludes missing values using an argument of the 'mean' function
# and another that uses the 'is.na' function.
y_Excluding_NA <- c(!is.na(y))
y_Excluding_NA
mean (y[y_Excluding_NA == TRUE])
# mean of y elements that are NOT "NA" is 4.987755

mean (y, na.rm=TRUE)
# mean of y elements that are NOT "NA" is 4.987755



# Define a variable w as the standard deviation of the x vector, divided by the square root of 30.
w <- sd(x) / sqrt(30)
w # w = 0.400313


# Take a simple random sample of 30 items from the x vector.  What is the sample mean?
sample_30_From_x <- sample (x, 30)
sample_30_From_x


# Is the sample mean within w (computed above) of the mean of the x vector?
mean (sample_30_From_x)
mean (x) - mean (sample_30_From_x)
# the difference between x's mean and the mean of the sample from x is .323333
# yes the sample mean is within w of x's mean