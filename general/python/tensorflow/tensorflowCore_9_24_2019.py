from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf






a = tf.compat.v1.constant (3.0, dtype=tf.float32)
b = tf.compat.v1.constant (4.0) #dtype=tf.float32 by default
total = a + b

'''
print (a)
print (b)
print (total)

#Above Print Statements Produce:

Tensor("Const:0", shape=(), dtype=float32)
Tensor("Const_1:0", shape=(), dtype=float32)
Tensor("add:0", shape=(), dtype=float32)
'''





'''
#One neat capability of Tensor Board is displaying a computation graph

writer = tf.compat.v1.summary.FileWriter ('.')
writer.add_graph (tf.compat.v1.get_default_graph ())
writer.flush ()
'''





#tf.Session is the engine of a computational graph. Session objects are what enable running/computing operations
session = tf.compat.v1.Session ()
print (session.run ({'ab': (a,b), 'total': total}))



vector = tf.random.uniform (shape=(3,))
out1 = vector + 1
out2 = vector + 2
#On 2 separate calls to tf.Session.run (), 2 different vectors are generated of random uniform values
print ('First tf.Session.run (Vector):\n\n', session.run (vector))
print ('\n\nSecond tf.Session.run (Vector):\n\n', session.run (vector))
#In 1 single call to tf.Session.run (), only 1 vector is generated of random uniform values, and the 'out1' and 'out2' operations do NOT change the underlying vector initially produced when this single call to tf.Session.run () is made
print ('\n\nMulti output with same input Vector:', session.run ({'out1': out1, 'out2': out2, 'vector': vector}))





#tf.placeholder ()'s facilitate including VARIABLE values as input for a computational graph "tf.placeholder ()" is a PROMISE to provide a concrete value LATER
x = tf.compat.v1.placeholder (tf.float32)
y = tf.compat.v1.placeholder (tf.float32)
z = x + y

#To EVALUATE a compuational graph that includes tf.placeholder ()'s, utilize the "feed_dict" argument of tf.Session.run ()
print ('\n\nSingle Value for x-placeholder and y-placeholder: ', session.run (z, feed_dict={x: 3, y: 4.5}))
print ('\n\nMulti Value for x-placeholder and y-placeholder: ', session.run (z, feed_dict={x: [1,3], y: [.5,4]}))






data = [[0, 1], [2, 3], [4, 5], [6, 7]]

slices = tf.data.Dataset.from_tensor_slices (data)
next_item = tf.compat.v1.data.make_one_shot_iterator (slices).get_next ()#compat.v1.data.make_one_shot_iterator (slices).get_next ()#None#
#for slice in slices:
while True:
	try:
		print ("\n\nCurrent Next Item: ", session.run (next_item))
	except tf.errors.OutOfRangeError:
		break
#next_item = slice
#print ("\n\nCurrent Next Item: ", session.run (next_item))







x = tf.compat.v1.placeholder (dtype=tf.float32, shape=[None, 3])
linear_model = tf.compat.v1.layers.Dense (units=1)
y = linear_model (x)

initializer = tf.compat.v1.global_variables_initializer ()
session.run (initializer)

print (session.run (y, feed_dict={x:[[1,2,3],[4,5,6]]}))






#Build a Simple Linear Regression Model with TF
x = tf.compat.v1.constant ([[1], [2], [3], [4]])
y_true = tf.compat.v1.constant ([[0], [-1], [-2], [-3]])


linear_model = tf.compat.v1.layers.Dense (units=1, dtype=tf.float32)
y_pred = linear_model (x)


session = tf.compat.v1.Session ()
initializer = tf.compat.v1.global_variables_initializer ()
session.run (initializer)

print ("\n\nPredicted Values w/o Training: ", session.run (y_pred))

#In order to be able to optimize a model, must first define a LOSS function (for regression, standard = Mean Square Error)
loss = tf.compat.v1.losses.mean_squared_error (labels=y_true, predictions=y_pred)
print ("\n\nMean Square Error of Model: ", session.run (loss))


#Train the model in order to MINIMIZE the LOSS
optimizer = tf.compat.v1.train.GradientDescentOptimizer (0.01)
trainer = optimizer.minimize (loss)

for i in range (15):
	loss_value = session.run ((trainer, loss))
	
	print ("Update Loss ", i + 1, " = ", loss_value)