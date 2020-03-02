from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf





#Define INPUT Function
#This function builds an input pipeline that yields (features, labels) pairs where features is a dictionary features
def train_input_fn (features, labels, batch_size):
	
	#Convert inputs to a Dataset
	dataset = tf.compat.v1.data.Dataset.from_tensor_slices ((dict (features), labels))
	
	#Shuffle, Repeat, and Batch
	dataset = dataset.shuffle (1000).repeat ().batch (batch_size)
	
	#Return the shuffled dataset
	return dataset





#Define Feature Columns - specify how the model should use each feature
features = []

for key in x_train.keys ():
	features.append (tf.feature_column.numeric_column (key=key))





#Define a Model Function
def main_model_fn (features, labels, mode, parameters):
	net = tf.compat.v1.feature_columns.input_layer (features, parameters ['feature_columns']) #Define the Input Layer for the Model Function
	
	#In order to build a DEEP Neural Net, AT LEAST ONE hidden layer must be defined
	#Define the Hidden Layer(s) for the Model. tf.layers API has functions available for producing layers of all types
	#In a DENSE Layer, each Node in the layer is connected to EVERY Node in the PRECEDING layer
	for units in parameters ['hidden_units']:
		net = tf.compat.v1.layers.dense (net, units, activation=tf.compat.v1.nn.relu)
	
	#Define the Output Layer, again using tf.layers API
	#The parameters ['n_classes'] specifices the number of output values (number of potential prediction classes), and NO activation function is used
	logits = tf.compat.v1.layers.dense (net, parameters ['n_classes'], activation=None)
	
	
	
	#Implement the branching code for handling tf.estimator.ModeKeys.TRAIN, tf.estimator.ModeKeys.EVAL, and tf.estimator.ModeKeys.PREDICT
	
	#Predict
	prediction_classes = tf.argmax (logits, 1)
	if mode == tf.estimator.ModeKeys.PREDICT:
		predictions =	{
							'class_ids': prediction_classes [:,tf.newaxis],
							'probabilities': tf.nn.softmax (logits),
							'logits': logits
						}
		
		return tf.estimator.EstimatorSpec (mode, predictions=predictions)
	
	
	
	#Loss (MUST be returned for Evaluate and Train)
	loss = tf.losses.sparse_softmax_cross_entropy (labels=labels, logits=logits)
	
	
	
	#Evaluate - the Evaluate Mode MUST return the Model LOSS
	accuracy = tf.metrics.accuracy (labels=labels, predictions=prediction_classes, name='acc_op')
	
	metrics = {'accuracy': accuracy}
	if mode == tf.estimator.ModeKeys.EVAL:
		return tf.estimator.EstimatorSpec (mode, loss=loss, eval_metric_ops=metrics) #NOTE, eval_metric_ops is OPTIONAL
	
	
	
	#Train - the Train Mode MUST return the Model LOSS AND a Training Operation
	#Training Operation - construction requires an OPTIMIZER (many options to choose from in the tf.train package)
	optimizer = tf.train.AdagradOptimizer (learning_rate=0.1)
	
	trainop = optimizer.minimize (loss, global_step=tf.train.get_global_step ())
	
	if mode == tf.estimator.ModeKeys.TRAIN:
		return tf.estimator.EstimatorSpec (mode, loss=loss, train_op=trainop)






#Need to IMPORT argparse
parser = argparse.ArgumentParser ()
parser.add_argument('--batch_size', default=100, type=int, help='batch size')
parser.add_argument('--train_steps', default=1000, type=int, help='number of training steps')


def main (argv):
	
	#Obtain command line arguments/parameters/specifications... BUT WHY does it start from index 1? What is the argv [0] for Python? (I think argv [0] might be used for checking "name == '__main__'"
	args = parser.parse (argsv [1:])
	
	#Obtain the data
	(train_x, train_y), (test_x, test_y) = iris_data.load_data ()
	
	#Define Feature Columns for specifying how the data should be used/consumed by the Estimator
	#In the case of the Iris dataset, ALL features are Numeric, but depending on the data in some other dataset, some features may be numberic, others may be categorical, or all may be categorical
	feature_columns = []
	for key in train_x.keys ():
		feature_columns.append (tf.feature_column.numeric_column (key=key))
	
	#Instantiate the Custom Estimator
	#This Estimator uses the Model Function defined above
	#The PARAMS dictionary argument in this Custom Estimator is equivalent to the key-word arguments of the Premade Estimator DNNClassifier
	#This Estimator uses the Feature Columns defined above to know HOW each column of data should be used
	#This Estimator has 2 Hidden Layers (making it a DEEP Neural Net), with each layer having 10 Nodes
	#This Estimator is forced to choose between 3 classes (for identifying each data entry)
	classifier = tf.estimator.Estimator (model_fn=main_model_fun, params={'feature_columns': feature_columns, 'hidden_units': [10,10], 'n_classes': 3})
	
	
	
	#Train the Custom Estimator
	#NOTE the "iris_data.train_input_fn ()" call from iris.py in the reference TF GitHub documents could have been replaced with calling the "train_input_fn ()" defined above, because the code is exactly the same
	classifier.train (input_fn=lambda:iris_data.train_input_fn (train_x, train_y, args.batch_size), steps=args.train_steps)
	
	
	
	#Evaluate the result from the Custom Estimator
	#NOTE could replace "iris_data.eval_input_fn ()" call from iris.py in the reference TF GitHub documents with a custom "eval_input_fn ()" IF it were to be defined above (like the "train_input_fn ()" defined above)
	eval_result = classifier.evaluate (input_fn=lambda:iris_data.eval_input_fn (train_x, train_y, args.batch_size))
	
	
	
	
	
	