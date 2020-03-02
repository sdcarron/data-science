import tensorflow as tf


#Creating TF Datasets
#Datasets in TF can be constructed with various structures
#Dataset.output_types and Dataset.output_shapes provide information regarding the inferred type and shape of each Dataset element tensor
dataset1 = tf.data.Dataset.from_tensor_slices (tf.random_uniform ([4,10]))
print (dataset1.output_types)
print (dataset1.output_shapes)

dataset2 = tf.data.Dataset.from_tensor_slices ((tf.random_uniform ([4]), tf.random_uniform ([4,100], maxval=100, dtype=tf.int32)))
print (dataset2.output_types)
print (dataset2.output_shapes)

dataset3 = tf.data.Dataset.zip ((dataset1, dataset2))
print (dataset3.output_types)
print (dataset3.output_shapes)

#It can be convenient naming different components of an element (perhaps each component represents a different feature of a training example)
#In addition to tuples, you can also used "collections.namedtuples" or a dictionary that maps strings to Tensors in order to represent a single Dataset element
dataset4 = tf.data.Dataset.from_tensor_slices ({"a": tf.random_uniform ([4]), "b": tf.random_uniform ([4,100], maxval=100, dtype=tf.int32)})
print (dataset4.output_types) # ==> "{'a': tf.float32, 'b': tf.int32}" 
print (dataset4.output_shapes) # ==> "{'a': (), 'b': (100,)}"

#Dataset TRANSFORMATIONS accomodate the various possible structures, when using Dataset.map (), Dataset.flat_map (), or Dataset.filter (), which apply a function to EACH ELEMENT, the ELEMENT STRUCTURE is what determines the argument structures
dataset1.map (lambda x: ...)
dataset2.flat_map (lambda x, y: ...)
dataset3.filter (lambda x, (y, z): ...)
