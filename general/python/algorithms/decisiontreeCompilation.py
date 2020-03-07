#This code follows the guide found at http://scikit-learn.org/stable/modules/tree.html
#"iris.data" and "iris.target" in the decision tree example at above url are both numpy ndarrays

from sklearn import tree
import pandas as pd
import numpy as np




data = pd.read_csv ("C:\Users\SCarron\Desktop\compilation.csv")

#print "Data Head: ", data.head ()

dataFilter = data [["Total Crack Scrap", "Total Starts", "Bad Carbide flag", "Carbide Density", "PCD Density", "Operator ID", "Press", "Power Avg", "TempTC Avg", "TIMEbRuns Avg"]] [(data ["Total Crack Scrap"].notnull ()) & (data ["Total Starts"].notnull ()) & (data ["Bad Carbide flag"].notnull ()) & (data ["Carbide Density"].notnull ()) & (data ["PCD Density"].notnull ()) & (data ["Year-Month Press"].notnull ()) & (data ["Operator ID"].notnull ()) & (data ["Press"].notnull ()) & (data ["Power Avg"].notnull ()) & (data ["TempTC Avg"].notnull ()) & (data ["TIMEbRuns Avg"].notnull ())]

#Verify that data was read in successfully
print "DataFilter Head: ", dataFilter.head ()




#Split the data into a TARGET Numpy ndarray and an EXPLANATORY Numpy ndarray
dataFilter ["PCT Scrap"] = (dataFilter ["Total Crack Scrap"] / dataFilter ["Total Starts"] * 1.0)


dataFilter ["Bernoulli Class"] = np.where (dataFilter ["PCT Scrap"] > 0.01, 1, 0)

print "DataFilter Head AFTER adding in the PCT Scrap and associated Bernoulli Class labels: ", dataFilter.tail ()

dataFilterBernoulli_1 = dataFilter [["Bernoulli Class"]] [dataFilter ["Bernoulli Class"] == 1].sum ()
print "Count of Observations in each Bernoulli Class: ", dataFilterBernoulli_1



#Break up each of these so that the dataset is SPLIT into a training and a test set
targetNP = dataFilter [["Bernoulli Class"]].values

xNP = dataFilter [["Total Starts", "Carbide Density", "PCD Density", "Operator ID", "Press", "Power Avg", "TempTC Avg", "TIMEbRuns Avg"]].values

#Verify that the arrays are Numpy ndarrays 
print "Type of targetNP array: ", type (targetNP)
print "Type of xNP array: ", type (xNP)




#Build the decision tree using the "targetNP" and "xNP" Numpy ndarrays
clf = tree.DecisionTreeClassifier ()

clf = clf.fit (xNP, targetNP)

import graphviz

dot_data = tree.export_graphviz (clf, out_file=None)
graph = graphviz.Source (dot_data)
graph.render ("dataFilter")


#These are all of the files I was following for trying to install Graphviz properly. Something still isn't working right. For some reason, it can't seem to recognize that I've included the "bin" and "bin/dot.exe" in the PATH
#https://stackoverflow.com/questions/22722730/installing-pygraphviz-on-windows-python-2-7-graphviz-2-36
#https://stackoverflow.com/questions/40809758/howto-install-pygraphviz-on-windows-10-64bit
#https://stackoverflow.com/questions/35064304/runtimeerror-make-sure-the-graphviz-executables-are-on-your-systems-path-aft
#https://stackoverflow.com/questions/22722730/installing-pygraphviz-on-windows-python-2-7-graphviz-2-36
#https://stackoverflow.com/questions/22722730/installing-pygraphviz-on-windows-python-2-7-graphviz-2-36
#
#https://fileinfo.com/extension/whl
# (Look at Pygraphiz) https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygraphviz
#https://graphviz.gitlab.io/_pages/Download/Download_windows.html
#https://pypi.org/project/graphviz/
