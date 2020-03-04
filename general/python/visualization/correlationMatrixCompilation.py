import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm


data = pd.read_csv ("C:\\Users\SCarron\\Desktop\\compilation.csv", low_memory=False)


print "Number of unique Operator IDs: ", data ["Operator ID"].nunique ()
operatorEncodeDict = {}

operatorEncode = 1

for operatorID in data ["Operator ID"].unique ():

	if operatorID not in operatorEncodeDict.keys () and np.isnan (operatorID) == False and len (str (operatorID)) > 3: #
		
		operatorEncodeDict [operatorID] = operatorEncode
		
		operatorEncode += 1
		
		#np.where (data ["Operator ID"] == operatorID, operatorEncode, 
		
		
print "Operator Encode Dict Head: ", operatorEncodeDict.keys () [0:5]

print "Operator Encode Dict Head: "

for ID in operatorEncodeDict.keys () [0:5]:

	print "\n", operatorEncodeDict [ID]

		
		
data ["Operator Encode"] = data ["Operator ID"]
		
for operatorID in operatorEncodeDict.keys ():

	#print "Operator ID is of type: ", type (operatorID)

	#data ["Operator Encode"] = np.where (data ["Operator ID"] == operatorID, operatorEncodeDict [operatorID], continue)
	for ID in data ["Operator ID"]:
	
		#print "Operator ID (", ID, ") VS the Encode Dictionary Key (", operatorID, ")\n\n"
	
		if ID == operatorID:
		
			data.loc [data ["Operator ID"] == ID, ["Operator Encode"]] = operatorEncodeDict [operatorID]
	
	
	
	
print "Operator Encode Head: ", data ["Operator Encode"].head ()

print "Number of UNIQUE Operator Encode IDs: ", data ["Operator Encode"].nunique ()


print "Operator Encode Values: ", data ["Operator Encode"].unique ()
		
		
		
correlationDict = {}




#Work through each UNIQUE Part Description 
for partType in data ["SFG Assembly"].unique (): #data ["SFG Description"].unique ():

	#Work through each UNIQUE Date Unit for the CURRENT Unique Part Description
	for date in data ["Year-Month Press"].unique ():

		
		
		
		
		#Collect the Data for Total Crack Scrap for the CURRENT Unique Date AND Unique Part Description
		dataFilter = data [["Part Size", "Total Crack Scrap", "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "Resistance Avg", "TempTC Avg", "Offset Delta (E-S) Avg", "Press"]] [(data ["Part Size"].notnull()) & (data ["SFG Assembly"] == partType) & (data ["SFG Part Family"].notnull ()) & (data ["Total Crack Scrap"].notnull ()) & (data ["Bad Carbide flag"] == "Good") & (data ["Carbide Density"].notnull ()) & (data ["Carbide MS"].notnull ()) & (data ["Carbide HC"].notnull ()) & (data ["PCD Density"].notnull ()) & (data ["Year-Month Press"] == date) & (data ["Power Avg"].notnull ()) & (data ['Resistance Avg'].notnull ()) & (data ["TempTC Avg"].notnull ()) & (data ['Offset Delta (E-S) Avg'].notnull ()) & (data ["Press"].notnull ())]
		
		#Collect the Data for Interfacial Crack Scrap for the CURRENT Unique Date AND Unique Part Description
		dataFilterInterfacial = data [["Part Size", "1064 CRACK - EDGE, INTERFACIAL", "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "Resistance Avg", "TempTC Avg", "Offset Delta (E-S) Avg", "Press"]] [(data ["Part Size"].notnull()) & (data ["SFG Description"] == partType) & (data ["SFG Part Family"].notnull ()) & (data ["Total Crack Scrap"].notnull ()) & (data ["Bad Carbide flag"] == "Good") & (data ["Carbide Density"].notnull ()) & (data ["Carbide MS"].notnull ()) & (data ["Carbide HC"].notnull ()) & (data ["PCD Density"].notnull ()) & (data ["Year-Month Press"] == date) & (data ["Power Avg"].notnull ()) & (data ['Resistance Avg'].notnull ()) & (data ["TempTC Avg"].notnull ()) & (data ['Offset Delta (E-S) Avg'].notnull ()) & (data ["Press"].notnull ())]
		
		#Collect the Data for Vertical Crack Scrap for the CURRENT Unique Date AND Unique Part Description
		dataFilterVertical = data [["Part Size", "1152 CRACK - VERTICAL",  "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "Resistance Avg", "TempTC Avg", "Offset Delta (E-S) Avg", "Press"]] [(data ["Part Size"].notnull()) & (data ["SFG Description"] == partType) & (data ["SFG Part Family"].notnull ()) & (data ["Total Crack Scrap"].notnull ()) & (data ["Bad Carbide flag"] == "Good") & (data ["Carbide Density"].notnull ()) & (data ["Carbide MS"].notnull ()) & (data ["Carbide HC"].notnull ()) & (data ["PCD Density"].notnull ()) & (data ["Year-Month Press"] == date) & (data ["Power Avg"].notnull ()) & (data ['Resistance Avg'].notnull ()) & (data ["TempTC Avg"].notnull ()) & (data ['Offset Delta (E-S) Avg'].notnull ()) & (data ["Press"].notnull ())]
		
		
		
		
		
		#Compute Correlation for the Total Crack Scrap Data collected above (Pandas DataFrame objects have the .corr() function for this)
		corr = dataFilter.corr ()
		
		#Compute Correlation for the Interfacial Crack Scrap Data collected above
		corrInterfacial = dataFilterInterfacial.corr ()
		
		#Compute Correlation for the Vertical Crack Scrap Data collected above
		corrVertical = dataFilterVertical.corr ()
		
		
		
		
		
		
		#print "Data type of dataFilter.corr (): ", type (corr)
		
		#print "DataFrame dimensions of dataFilter.corr (): ", corr.shape
		
		# if correlationDict [partType].notnull ():
		
			# if correlationDict [partType] [date].notnull ():
			
				# correlationDict [partType] [date].append (corr)
				
			# else:
			
				# correlationDict [partType] [date] = []
				
		# else:
		
			# correlationDict [partType] = {}
		
		
		# sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns, annot=True)
		# plt.show ()
		
		
		# sns.heatmap(dataFilter.corr (), annot=True, fmt=".2f")
		# plt.show ()
		
		
		
		
		
		
		#"%.2f" % round(corrVertical
		
		#Filter Data to ONLY work with Data associated with D82 Part Descriptions for now
		#if str (partType).find ("Y31036") != -1: #("D82") != -1:
		
			# if not (partType in timeSeriesTotalDict.keys ()):#timeSeriesTotalDict [partType] is None:
			
				# timeSeriesTotalDict [partType] = []
				
			# else:
			
				# #for column in dataFilter.columns:
				
				# #	if column != "Total Crack Scrap":
					
				# timeSeriesTotalDict [partType].append (dataFilter.drop (columns="Total Crack Scrap").corrwith (dataFilter ["Total Crack Scrap"]))#"%.2f" % round(dataFilter ["Total Crack Scrap"].corr (column).astype (float)))
				
			# if not (partType in timeSeriesInterfacialDict.keys ()): #timeSeriesInterfacialDict [partType] is None:
			
				# timeSeriesInterfacialDict [partType] = []
				
			# else:
			
				# #for column in dataFilterInterfacial.columns:
				
				# #	if column != "1064 CRACK - EDGE, INTERFACIAL":
					
				# timeSeriesInterfacialDict [partType].append (dataFilterInterfacial.drop (columns="1064 CRACK - EDGE, INTERFACIAL").corrwith (dataFilterInterfacial ["1064 CRACK - EDGE, INTERFACIAL"]))#"%.2f" % round(dataFilterInterfacial ["1064 CRACK - EDGE, INTERFACIAL"].corr (column).astype (float)))
				
			# if not partType in timeSeriesVerticalDict.keys (): #timeSeriesVerticalDict [partType] is None:
			
				# timeSeriesVerticalDict [partType] = []

			# else:
			
				# #for column in dataFilterVertical.columns:
				
				# #	if column != "1152 CRACK - VERTICAL":
					
				# timeSeriesVerticalDict [partType].append (dataFilterVertical.drop (columns="1152 CRACK - VERTICAL").corrwith (dataFilterVertical ["1152 CRACK - VERTICAL"]))#"%.2f" % round(dataFilterVertical ["1152 CRACK - VERTICAL"].corr (column).astype (float)))
		
		
			
dataFilterTotal = data [["Part Size", "Total Crack Scrap", "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "Resistance Avg", "TempTC Avg", "Offset Delta (E-S) Avg", "Press"]] [(data ["Part Size"].notnull()) & (data ["SFG Assembly"].str.contains ("Y31036") != False) & (data ["SFG Part Family"].notnull ()) & (data ["Total Crack Scrap"].notnull ()) & (data ["Bad Carbide flag"] == "Good") & (data ["Carbide Density"].notnull ()) & (data ["Carbide MS"].notnull ()) & (data ["Carbide HC"].notnull ()) & (data ["PCD Density"].notnull ()) & (data ["Year-Month Press"] == date) & (data ["Power Avg"].notnull ()) & (data ['Resistance Avg'].notnull ()) & (data ["TempTC Avg"].notnull ()) & (data ['Offset Delta (E-S) Avg'].notnull ()) & (data ["Press"].notnull ())]

dataFilterInterfacial = data [["Part Size", "1064 CRACK - EDGE, INTERFACIAL", "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "Resistance Avg", "TempTC Avg", "Offset Delta (E-S) Avg", "Press"]] [(data ["Part Size"].notnull()) & (data ["SFG Assembly"].str.contains ("Y31036") != False) & (data ["SFG Part Family"].notnull ()) & (data ["Total Crack Scrap"].notnull ()) & (data ["Bad Carbide flag"] == "Good") & (data ["Carbide Density"].notnull ()) & (data ["Carbide MS"].notnull ()) & (data ["Carbide HC"].notnull ()) & (data ["PCD Density"].notnull ()) & (data ["Year-Month Press"] == date) & (data ["Power Avg"].notnull ()) & (data ['Resistance Avg'].notnull ()) & (data ["TempTC Avg"].notnull ()) & (data ['Offset Delta (E-S) Avg'].notnull ()) & (data ["Press"].notnull ())]

dataFilterVertical = dataFilterVertical = data [["Part Size", "1152 CRACK - VERTICAL",  "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "Resistance Avg", "TempTC Avg", "Offset Delta (E-S) Avg", "Press"]] [(data ["Part Size"].notnull()) & (data ["SFG Assembly"].str.contains ("Y31036") != False) & (data ["SFG Part Family"].notnull ()) & (data ["Total Crack Scrap"].notnull ()) & (data ["Bad Carbide flag"] == "Good") & (data ["Carbide Density"].notnull ()) & (data ["Carbide MS"].notnull ()) & (data ["Carbide HC"].notnull ()) & (data ["PCD Density"].notnull ()) & (data ["Year-Month Press"] == date) & (data ["Power Avg"].notnull ()) & (data ['Resistance Avg'].notnull ()) & (data ["TempTC Avg"].notnull ()) & (data ['Offset Delta (E-S) Avg'].notnull ()) & (data ["Press"].notnull ())]		


corr = dataFilterTotal.corr ()
corrInterfacial = dataFilterInterfacial.corr ()
corrVertical = dataFilterVertical.corr ()
			
#Create Correlation Matrix plots for the Correlation Values computed above for Total, Interfacial, and Vertical Crack Scrap
#These three sets of plt calls are set up to construct correlation matrices for each of the D82 parts. If Correlation Matrices are desired for EVERY Part Description, these three plt calls need to be SHIFT+TAB once
fig = plt.figure(figsize=(19.2,10.8), dpi=100)
ax1 = fig.add_subplot(111)
cmap = cm.get_cmap('jet', 30)
cax = ax1.imshow(corr, interpolation="nearest", cmap=cmap)
ax1.grid(True)
plt.title(str (partType) + "_" + str (date) + "_TotalScrap")
labels=["Part Size", "Total Crack Scrap", "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "Resistance", "TempTC Avg", "Offset Delta", "Press"]

#Force ALL of the varible names to be displayed
ax1.set_xticks(np.arange(len(labels)))
ax1.set_yticks(np.arange(len(labels)))

# Make x-axis variable names display
ax1.xaxis.label.set_rotation(90)
# Make y-axis variable names display horizontally
ax1.yaxis.label.set_rotation (0)

#Force the tick marks to be identified by the variable names
ax1.set_xticklabels(labels,fontsize=6)
ax1.set_yticklabels(labels,fontsize=6)

# Add colorbar, make sure to specify tick locations to match desired ticklabels
fig.colorbar(cax, ticks=[.75,.8,.85,.90,.95,1])



for i in range(len(labels)):
	for j in range(len(labels)):
		text = ax1.text(j, i, "%.2f" % round(corr.iat [i, j],4),
					   ha="center", va="center", color="w")



#plt.show()
plt.savefig (str (partType) + "_" + str (date) + "TotalCrackScrap" + ".png")


plt.close ("all")











figInterfacial = plt.figure(figsize=(19.2,10.8), dpi=100)
ax1 = figInterfacial.add_subplot(111)
cmap = cm.get_cmap('jet', 30)
cax = ax1.imshow(corrInterfacial, interpolation="nearest", cmap=cmap)
ax1.grid(True)
plt.title(str (partType) + "_" + str (date) + "_Interfacial")
labels=["Part Size", "Crack IF", "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "Resistance", "TempTC Avg", "Offset Delta", "Press"]

#Force ALL of the varible names to be displayed
ax1.set_xticks(np.arange(len(labels)))
ax1.set_yticks(np.arange(len(labels)))

# Make x-axis variable names display vertically
ax1.xaxis.label.set_rotation(90)
# Make y-axis variable names display horizontally
ax1.yaxis.label.set_rotation (0)

#Force the tick marks to be identified by the variable names
ax1.set_xticklabels(labels,fontsize=6)
ax1.set_yticklabels(labels,fontsize=6)

# Add colorbar, make sure to specify tick locations to match desired ticklabels
fig.colorbar(cax, ticks=[.75,.8,.85,.90,.95,1])



for i in range(len(labels)):
	for j in range(len(labels)):
		text = ax1.text(j, i, "%.2f" % round(corrInterfacial.iat [i, j],4),
					   ha="center", va="center", color="w")



#plt.show()
plt.savefig (str (partType) + "_" + str (date) + "_Interfacial" + ".png")

















figVertical = plt.figure(figsize=(19.2,10.8), dpi=100)
ax1 = figVertical.add_subplot(111)
cmap = cm.get_cmap('jet', 30)
cax = ax1.imshow(corrVertical, interpolation="nearest", cmap=cmap)
ax1.grid(True)
plt.title(str (partType) + "_" + str (date) + "_Vertical")
labels=["Part Size", "Crack Vert", "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "Resistance", "TempTC Avg", "Offset Delta", "Press"]

#Force ALL of the varible names to be displayed
ax1.set_xticks(np.arange(len(labels)))
ax1.set_yticks(np.arange(len(labels)))

# Make x-axis variable names display vertically
ax1.xaxis.label.set_rotation(90)
# Make y-axis variable names display horizontally
ax1.yaxis.label.set_rotation (0)

#Force the tick marks to be identified by the variable names
ax1.set_xticklabels(labels,fontsize=6)
ax1.set_yticklabels(labels,fontsize=6)

# Add colorbar, make sure to specify tick locations to match desired ticklabels
fig.colorbar(cax, ticks=[.75,.8,.85,.90,.95,1])



for i in range(len(labels)):
	for j in range(len(labels)):
		text = ax1.text(j, i, "%.2f" % round(corrVertical.iat [i, j],4),
					   ha="center", va="center", color="w")



#plt.show()
plt.savefig (str (partType) + "_" + str (date) + "_Vertical" + ".png")
		
		
		




		
		
		
		
		
		# plt.matshow (corr, annot=True)
		# plt.xticks (range (len (corr.columns)), corr.columns)
		# plt.yticks (range (len (corr.columns)), corr.columns)
		# plt.title (date)
		# plt.show ()
		
		
		
		
		
		
		# corr = dataFilter.corr ().abs ()
		
		# s = corr.unstack ()
		
		# so = s.sort_values (kind='quicksort')
		
		# print so
		
		
		#print dataFilter [["Part Size", "SFG Part Family", "Total Crack Scrap", "Total Starts", "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press", "Operator ID"]].corrwith (dataFilter ["Total Crack Scrap"], axis=1)
		
		
		
		
		
		
		# print "\n\n\n\nCorrelation values for: ", date, "AND SFG Part Family (", partType, ")"
		
		# for column in dataFilter.columns:
		
			# if column != date and column != "Total Crack Scraps" and column != "SFG Part Family" and column != "Operator ID":
			
				# print "\n\nCorr between ", column, "and Total Crack Scrap: ", dataFilter ["Total Crack Scrap"].corr (dataFilter [column])
				
				







# Class DataStructure ():

	# def __init__ (self, file):
		
		# self.file = file
		
		# self.data = null
		
		# self.dataFilter = null
	
	# def readin (self):
	
		# self.data = pd.read_csv (file)
		
	# def filter (self, partType, pressTime, responseVar):
	
		# for self.data [partType].unique ():
		
			# for self.data [pressTime].unique ():
			
				
		
	# def readout (self):
	
		# return self.data