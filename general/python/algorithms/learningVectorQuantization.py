#This follows this url https://machinelearningmastery.com/implement-learning-vector-quantization-scratch-python/
#Learning Vector Quantization is similar to KNN

from math import sqrt

#Compute the Euclidean Distance between two rows of the data
def euclidean_distance (row1, row2):

	distance = 0.0
	
	for i in range (len (row1) - 1):
	
		distance += (row1 [i] - row2 [i])**2
		
	return sqrt (distance)
	
	
	

#Identify the best match from all of the rows for the row of interest (the row of new data)
def best_match (row, codebooks):

	distances = list ()
	
	for codebook in codebooks:
		
		distance = euclidean_distance (row, codebook)
		
		distances.append ((codebook, distance))
		
	distances.sort (key=lambda tup: tup [1])
	#Another option for above line is "sorted (distances, key=lambda tupel, tupel [1])
	
	return distances [0] [0]
	
	
	
	
	
#Train the Codebook Vectors
def rand_codebook (train):

	nrecords = len (train)
	nfeatures = len (train [0])
	
	codebook = []
	
	for i in range (len (nfeatures)):
	
		codebook [i] = train [randrange (nrecords)] [i]
		
	return codebook

	
	
	
testData = [[2.7810836,2.550537003,0],
	[1.465489372,2.362125076,0],
	[3.396561688,4.400293529,0],
	[1.38807019,1.850220317,0],
	[3.06407232,3.005305973,0],
	[7.627531214,2.759262235,1],
	[5.332441248,2.088626775,1],
	[6.922596716,1.77106367,1],
	[8.675418651,-0.242068655,1],
	[7.673756466,3.508563011,1]]
	
	
row0 = testData [0]

for row in testData:

	print "Euclidean Distance between row [", row, "]\tand row[", row0, "is: ", euclidean_distance (row0, row)
	
	
	
bestMatch = best_match (row0, testData)

print "Best Match: ", bestMatch