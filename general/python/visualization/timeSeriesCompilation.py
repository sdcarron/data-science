import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


data = pd.read_csv ("C:\\Users\SCarron\\Desktop\\compilation.csv", low_memory=False)






#Prepare the data structures for collecting and organizing the data for correlation computation
timeSeriesTotalDict = {}

timeSeriesInterfacialDict = {}

timeSeriesVerticalDict = {}

timeSeriesDateList = []

#Capture the Time Units in their proper order (These aren't recognized by Python as Dates, so they can't be compared by value) 
for date in data ["Year-Month Press"].unique ():
	
	timeSeriesDateList.append (date)

#Drop the FIRST Date Unit from the list because it is a NaN value for some reason
timeSeriesDateList = timeSeriesDateList [1:]

print "\n\n\n\n\n\nUNIQUE PART TYPES: ", data ["SFG Part Family"].unique ()








#Work through each UNIQUE Part Description 
for partType in data ["SFG Description"].unique ():

	#Work through each UNIQUE Date Unit for the CURRENT Unique Part Description
	for date in data ["Year-Month Press"].unique ():


	
	
	
		#Collect the Data for Total Crack Scrap for the CURRENT Unique Date AND Unique Part Description
		dataFilter = data [["Part Size", "Total Crack Scrap", "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "Resistance Avg", "TempTC Avg", "Offset Delta (E-S) Avg", "Press"]] [(data ["Part Size"].notnull()) & (data ["SFG Description"] == partType) & (data ["SFG Part Family"].notnull ()) & (data ["Total Crack Scrap"].notnull ()) & (data ["Bad Carbide flag"] == "Good") & (data ["Carbide Density"].notnull ()) & (data ["Carbide MS"].notnull ()) & (data ["Carbide HC"].notnull ()) & (data ["PCD Density"].notnull ()) & (data ["Year-Month Press"] == date) & (data ["Power Avg"].notnull ()) & (data ['Resistance Avg'].notnull ()) & (data ["TempTC Avg"].notnull ()) & (data ['Offset Delta (E-S) Avg'].notnull ()) & (data ["Press"].notnull ())]
		
		#Collect the Data for Interfacial Crack Scrap for the CURRENT Unique Date AND Unique Part Description
		dataFilterInterfacial = data [["Part Size", "1064 CRACK - EDGE, INTERFACIAL", "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "Resistance Avg", "TempTC Avg", "Offset Delta (E-S) Avg", "Press"]] [(data ["Part Size"].notnull()) & (data ["SFG Description"] == partType) & (data ["SFG Part Family"].notnull ()) & (data ["Total Crack Scrap"].notnull ()) & (data ["Bad Carbide flag"] == "Good") & (data ["Carbide Density"].notnull ()) & (data ["Carbide MS"].notnull ()) & (data ["Carbide HC"].notnull ()) & (data ["PCD Density"].notnull ()) & (data ["Year-Month Press"] == date) & (data ["Power Avg"].notnull ()) & (data ['Resistance Avg'].notnull ()) & (data ["TempTC Avg"].notnull ()) & (data ['Offset Delta (E-S) Avg'].notnull ()) & (data ["Press"].notnull ())]
		
		#Collect the Data for Vertical Crack Scrap for the CURRENT Unique Date AND Unique Part Description
		dataFilterVertical = data [["Part Size", "1152 CRACK - VERTICAL",  "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "Resistance Avg", "TempTC Avg", "Offset Delta (E-S) Avg", "Press"]] [(data ["Part Size"].notnull()) & (data ["SFG Description"] == partType) & (data ["SFG Part Family"].notnull ()) & (data ["Total Crack Scrap"].notnull ()) & (data ["Bad Carbide flag"] == "Good") & (data ["Carbide Density"].notnull ()) & (data ["Carbide MS"].notnull ()) & (data ["Carbide HC"].notnull ()) & (data ["PCD Density"].notnull ()) & (data ["Year-Month Press"] == date) & (data ["Power Avg"].notnull ()) & (data ['Resistance Avg'].notnull ()) & (data ["TempTC Avg"].notnull ()) & (data ['Offset Delta (E-S) Avg'].notnull ()) & (data ["Press"].notnull ())]
		
	
	
	
	


		#Filter Data to ONLY work with Data associated with D82 Part Descriptions for now
		if str (partType).find ("D82") != -1:
		
			if not (partType in timeSeriesTotalDict.keys ()):#timeSeriesTotalDict [partType] is None:
			
				timeSeriesTotalDict [partType] = []
				
			else:
			
				#for column in dataFilter.columns:
				
				#	if column != "Total Crack Scrap":
					
				timeSeriesTotalDict [partType].append (dataFilter.drop (columns="Total Crack Scrap").corrwith (dataFilter ["Total Crack Scrap"]))#"%.2f" % round(dataFilter ["Total Crack Scrap"].corr (column).astype (float)))
				
			if not (partType in timeSeriesInterfacialDict.keys ()): #timeSeriesInterfacialDict [partType] is None:
			
				timeSeriesInterfacialDict [partType] = []
				
			else:
			
				#for column in dataFilterInterfacial.columns:
				
				#	if column != "1064 CRACK - EDGE, INTERFACIAL":
					
				timeSeriesInterfacialDict [partType].append (dataFilterInterfacial.drop (columns="1064 CRACK - EDGE, INTERFACIAL").corrwith (dataFilterInterfacial ["1064 CRACK - EDGE, INTERFACIAL"]))#"%.2f" % round(dataFilterInterfacial ["1064 CRACK - EDGE, INTERFACIAL"].corr (column).astype (float)))
				
			if not partType in timeSeriesVerticalDict.keys (): #timeSeriesVerticalDict [partType] is None:
			
				timeSeriesVerticalDict [partType] = []

			else:
			
				#for column in dataFilterVertical.columns:
				
				#	if column != "1152 CRACK - VERTICAL":
					
				timeSeriesVerticalDict [partType].append (dataFilterVertical.drop (columns="1152 CRACK - VERTICAL").corrwith (dataFilterVertical ["1152 CRACK - VERTICAL"]))#"%.2f" % round(dataFilterVertical ["1152 CRACK - VERTICAL"].corr (column).astype (float)))
				
				
				
				
				
				
				
				
				
			
			
			
#Collect Total Crack Scrap Correlation Values in proper Time Unit Order BY Variable Name for each UNIQUE Part Description
timeSeriesTotalDictPartVars = {}
		
#Cycle through each UNIQUE Part Description and the corresponding Correlation Values
for partType in timeSeriesTotalDict.keys ():

	print "\n\nT Series (", partType, ") is ", timeSeriesTotalDict [partType]
	
	#if str (partType).lower ().find ("16 mm") != -1:
	
	
	#If the CURRENT Unique Part Description is NOT in the new Data Structure separating out Correlation Values BY Variable Name
	if not partType in timeSeriesTotalDictPartVars.keys ():
	
		#Add the NEW Unique Part Description as a Primary Key
		timeSeriesTotalDictPartVars [partType] = {}
		
		#Cycle through each CORRELATION MATRIX associated with the CURRENT Unique Part Description
		for corrmat in timeSeriesTotalDict [partType]:

		#for column in corrmat.columns:
			
			#Cycle through each VARIABLE in the CURRENT Correlation Matrix associated with the CURRENT Unique Part Description
			for row in np.arange (corrmat.size):
		
				#if column != "Total Crack Scrap":
			
				#If the CURRENT Variable Name is NOT in the data structure
				if not corrmat.index [row] in timeSeriesTotalDictPartVars [partType].keys ():
			
					#Add the NEW Unique Variable Name as a Secondary Key into the data structure
					timeSeriesTotalDictPartVars [partType] [corrmat.index [row]] = []
					
					#Insert the CURRENT Correlation Value (from the current row) into the new area of the data structure
					timeSeriesTotalDictPartVars [partType] [corrmat.index [row]].append (corrmat.iloc [row])#["Total Crack Scrap", column])

				#If the CURRENT Variable Name IS in the data structure then insert the CURRENT Correlation Value (from the current row) into the appropriate area of the data structure
				else:
			
					timeSeriesTotalDictPartVars [partType] [corrmat.index [row]].append (corrmat.iloc [row])#["Total Crack Scrap", column])
	
	
	
	#If the CURRENT Unique Part Description IS in the new Data Structure separating out Correlation Values BY Variable Name
	else:
	
		#Cycle through each CORRELATION MATRIX associated with the CURRENT Unique Part Description
		for corrmat in timeSeriesTotalDict [partType]:

		#for column in corrmat.columns:
			
			#Cycle through each VARIABLE in the CURRENT Correlation Matrix associated with the CURRENT Unique Part Description
			for row in np.arange (corrmat.size):
		
				#if column != "Total Crack Scrap":
			
				#If the CURRENT Variable Name is NOT in the data structure
				if not corrmat.index [row] in timeSeriesTotalDictPartVars [partType].keys ():
			
					#Add the NEW Unique Variable Name as a Secondary Key into the data structure
					timeSeriesTotalDictPartVars [partType] [corrmat.index [row]] = []
					
					#Insert the CURRENT Correlation Value (from the current row) into the new area of the data structure
					timeSeriesTotalDictPartVars [partType] [corrmat.index [row]].append (corrmat.iloc [row])#["Total Crack Scrap", column])

				#If the CURRENT Variable Name IS in the data structure then insert the CURRENT Correlation Value (from the current row) into the appropriate area of the data structure
				else:
			
					timeSeriesTotalDictPartVars [partType] [corrmat.index [row]].append (corrmat.iloc [row])#["Total Crack Scrap", column])
					
					
					
					
					

					
					
					
					
					
#Collect Interfacial Crack Scrap Correlation Values in proper Time Unit Order BY Variable Name for each UNIQUE Part Description				
timeSeriesInterfacialDictPartVars = {}

#Cycle through each UNIQUE Part Description and the corresponding Correlation Values
for partType in timeSeriesInterfacialDict.keys ():

	#If the CURRENT Unique Part Description is NOT in the new Data Structure separating out Correlation Values BY Variable Name
	if not partType in timeSeriesInterfacialDictPartVars.keys ():
	
		#Add the NEW Unique Part Description as a Primary Key
		timeSeriesInterfacialDictPartVars [partType] = {}
		
		#Cycle through each CORRELATION MATRIX associated with the CURRENT Unique Part Description
		for corrmat in timeSeriesInterfacialDict [partType]:
		
			#Cycle through each VARIABLE in the CURRENT Correlation Matrix associated with the CURRENT Unique Part Description
			for row in np.arange (corrmat.size):
			
				#If the CURRENT Variable Name is NOT in the data structure
				if not corrmat.index [row] in timeSeriesInterfacialDictPartVars [partType].keys ():
				
					#Add the NEW Unique Variable Name as a Secondary Key into the data structure
					timeSeriesInterfacialDictPartVars [partType] [corrmat.index [row]] = []
					
					#Insert the CURRENT Correlation Value (from the current row) into the new area of the data structure
					timeSeriesInterfacialDictPartVars [partType] [corrmat.index [row]].append (corrmat.iloc [row])
					
				#If the CURRENT Variable Name IS in the data structure then insert the CURRENT Correlation Value (from the current row) into the appropriate area of the data structure
				else:
				
					timeSeriesInterfacialDictPartVars [partType] [corrmat.index [row]].append (corrmat.iloc [row])
	
	#If the CURRENT Unique Part Description IS in the new Data Structure separating out Correlation Values BY Variable Name				
	else:
	
		#Cycle through each CORRELATION MATRIX associated with the CURRENT Unique Part Description
		for corrmat in timeSeriesInterfacialDict [partType]:
		
			#Cycle through each VARIABLE in the CURRENT Correlation Matrix associated with the CURRENT Unique Part Description
			for row in np.arange (corrmat.size):
			
				#If the CURRENT Variable Name is NOT in the data structure
				if not corrmat.index [row] in timeSeriesInterfacialDictPartVars [partType].keys ():
				
					#Add the NEW Unique Variable Name as a Secondary Key into the data structure
					timeSeriesInterfacialDictPartVars [partType] [corrmat.index [row]] = []
					
					#Insert the CURRENT Correlation Value (from the current row) into the new area of the data structure
					timeSeriesInterfacialDictPartVars [partType] [corrmat.index [row]].append (corrmat.iloc [row])
				
				#If the CURRENT Variable Name IS in the data structure then insert the CURRENT Correlation Value (from the current row) into the appropriate area of the data structure
				else:
				
					timeSeriesInterfacialDictPartVars [partType] [corrmat.index [row]].append (corrmat.iloc [row])
					
					
					
					
			
			

			
			
			
#Collect Vertical Crack Scrap Correlation Values in proper Time Unit Order BY Variable Name for each UNIQUE Part Description			
timeSeriesVerticalDictPartVars = {}

#Cycle through each UNIQUE Part Description and the corresponding Correlation Values
for partType in timeSeriesVerticalDict.keys ():

	#If the CURRENT Unique Part Description is NOT in the new Data Structure separating out Correlation Values BY Variable Name
	if not partType in timeSeriesVerticalDictPartVars.keys ():
	
		#Add the NEW Unique Part Description as a Primary Key
		timeSeriesVerticalDictPartVars [partType] = {}
		
		#Cycle through each CORRELATION MATRIX associated with the CURRENT Unique Part Description
		for corrmat in timeSeriesVerticalDict [partType]:
		
			#Cycle through each VARIABLE in the CURRENT Correlation Matrix associated with the CURRENT Unique Part Description
			for row in np.arange (corrmat.size):
			
				#If the CURRENT Variable Name is NOT in the data structure
				if not corrmat.index [row] in timeSeriesVerticalDictPartVars [partType].keys ():
				
					#Add the NEW Unique Variable Name as a Secondary Key into the data structure
					timeSeriesVerticalDictPartVars [partType] [corrmat.index [row]] = []
					
					#Insert the CURRENT Correlation Value (from the current row) into the new area of the data structure
					timeSeriesVerticalDictPartVars [partType] [corrmat.index [row]].append (corrmat.iloc [row])
				
				#If the CURRENT Variable Name IS in the data structure then insert the CURRENT Correlation Value (from the current row) into the appropriate area of the data structure				
				else:
				
					timeSeriesVerticalDictPartVars [partType] [corrmat.index [row]].append (corrmat.iloc [row])
	
	#If the CURRENT Unique Part Description IS in the new Data Structure separating out Correlation Values BY Variable Name	
	else:
	
		#Cycle through each CORRELATION MATRIX associated with the CURRENT Unique Part Description
		for corrmat in timeSeriesVerticalDict [partType]:
		
			#Cycle through each VARIABLE in the CURRENT Correlation Matrix associated with the CURRENT Unique Part Description
			for row in np.arange (corrmat.size):
			
				#If the CURRENT Variable Name is NOT in the data structure
				if not corrmat.index [row] in timeSeriesVerticalDictPartVars [partType].keys ():
				
					#Add the NEW Unique Variable Name as a Secondary Key into the data structure
					timeSeriesVerticalDictPartVars [partType] [corrmat.index [row]] = []
					
					#Insert the CURRENT Correlation Value (from the current row) into the new area of the data structure
					timeSeriesVerticalDictPartVars [partType] [corrmat.index [row]].append (corrmat.iloc [row])
				
				#If the CURRENT Variable Name IS in the data structure then insert the CURRENT Correlation Value (from the current row) into the appropriate area of the data structure
				else:
				
					timeSeriesVerticalDictPartVars [partType] [corrmat.index [row]].append (corrmat.iloc [row])
					
					
					
					
					
					
					
					
					
					
					
					
					
print "\n\n\n\n\n\nTime Series Values"					
					
					
					
#Create Plots for the Total Crack Correlation data 						
for partType in timeSeriesTotalDictPartVars.keys ():

	#print "\n\n\n\n\n\nVariable time Series Correlation Values for Part (", partType, "):\n\n\n"
	
	for variable in timeSeriesTotalDictPartVars [partType].keys ():
	
		#print "\n\n\n\n\n\nVariable time Series Correlation Values for Variable (", variable, ")\n\n", timeSeriesTotalDictPartVars [partType] [variable]
		
		#Create a NP Array of the correlation values
		npCorrVals = np.array (timeSeriesTotalDictPartVars [partType] [variable]).astype (np.double)
		#Create a TRUE/FALSE NP Array indicating which correlation values are FINITE
		npCorrPlotMask = np.isfinite (npCorrVals)
		
		#Create a NP Array of the Time Units
		npDatePlot = np.array (timeSeriesDateList)
		
		# print "NP Date Plot: ", npDatePlot, "\n\n"
		# print "NP Corr Plot Mask: ", npCorrPlotMask, "\n\n"
		# print "NP Corr Vals: ", npCorrVals, "\n\n"
		
		#Instantiate a figure to hold the plot
		figTimeSeries = plt.figure(figsize=(19.2,10.8), dpi=100)
		ax1 = figTimeSeries.add_subplot(111)
		cmap = cm.get_cmap('jet', 30)
		# cax = ax1.imshow(corrVertical, interpolation="nearest", cmap=cmap)
		# ax1.grid(True)
		# plt.title(str (partType) + "_" + str (date) + "_Vertical")
		# labels=["Part Size", "Crack Vert", "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "Resistance", "TempTC Avg", "Offset Delta", "Press"]
		
		#Force ALL of the varible names to be displayed
		#ax1.set_xticks(npDatePlot)
		#ax1.set_yticks(npCorrVals)
		
		# Make x-axis variable names display vertically
		#ax1.xaxis.label.set_rotation(90)
		# Make y-axis variable names display horizontally
		#ax1.yaxis.label.set_rotation (0)
		
		#Force the tick marks to be identified by the variable names
		#ax1.set_xticklabels(labels,fontsize=6)
		#ax1.set_yticklabels(labels,fontsize=6)
		
		# Add colorbar, make sure to specify tick locations to match desired ticklabels
		#fig.colorbar(cax, ticks=[.75,.8,.85,.90,.95,1])
		
		
		
		# for i in range(len(labels)):
			# for j in range(len(labels)):
				# text = ax1.text(j, i, "%.2f" % round(corrVertical.iat [i, j],4),
							   # ha="center", va="center", color="w")


		
		#plt.show()
		#plt.savefig (str (partType) + "_" + str (date) + "_Vertical" + ".png")
		
		#Set the Parameters for the plot (only plot the data points that correspond to FINITE correlation values)
		plt.plot (npDatePlot [npCorrPlotMask], npCorrVals [npCorrPlotMask], linestyle='-', marker='o')
		plt.title ("Correlation Total Crack Time Series Part (" + partType + ") _ Variable (" + variable + ")")
		#plt.show ()
		plt.savefig ("timeSeries_" + partType + "_" + variable + "_TotalScrap")
		plt.close ('all') #close all open figures to prevent too many figures being open at once and, as a result, consuming all the memory
		
		
		
		
		
#Create Plots for the Interfacial Crack Correlation data		
for partType in timeSeriesInterfacialDictPartVars.keys ():

	for variable in timeSeriesInterfacialDictPartVars [partType].keys ():
	
		#Create a NP Array of the correlation values
		npCorrVals = np.array (timeSeriesInterfacialDictPartVars [partType] [variable]).astype (np.double)
		#Create a TRUE/FALSE NP Array indicating which correlation values are FINITE
		npCorrPlotMask = np.isfinite (npCorrVals)
		
		#Create a NP Array of the Time Units
		npDatePlot = np.array (timeSeriesDateList)
		
		#Instantiate a figure to hold the plot
		figTimeSeries = plt.figure (figsize=(19.2,10.8), dpi=100)
		ax1 = figTimeSeries.add_subplot (111)
		cmap = cm.get_cmap ('jet', 30)
		
		#Set the Parameters for the plot (only plot the data points that correspond to FINITE correlation values)
		plt.plot (npDatePlot [npCorrPlotMask], npCorrVals [npCorrPlotMask], linestyle='-', marker='o')
		plt.title ("Correlation Interfacial Time Series Part (" + partType + ") _ Variable (" + variable + ")")
		plt.savefig ("timeSeries_" + partType + "_" + variable + "_InterfacialScrap")
		plt.close ('all') #After the Plot has been saved, close the figure in order to free up memory
		
		
		
		
#Create Plots for the Vertical Crack Correlation data		
for partType in timeSeriesVerticalDictPartVars.keys ():

	for variable in timeSeriesVerticalDictPartVars [partType].keys ():
	
		#Create a NP Array of the correlation values
		npCorrVals = np.array (timeSeriesVerticalDictPartVars [partType] [variable]).astype (np.double)
		#Create a TRUE/FALSE NP Array indicating which correlation values are FINITE
		npCorrPlotMask = np.isfinite (npCorrVals)
		
		#Create a NP Array of the Time Units
		npDatePlot = np.array (timeSeriesDateList)
		
		#Instantiate a figure to hold the plot
		figTimeSeries = plt.figure (figsize=(19.2,10.8), dpi=100)
		ax1 = figTimeSeries.add_subplot (111)
		cmap = cm.get_cmap ('jet', 30)
		
		#Set the Parameters for the plot (only plot the data points that correspond to FINITE correlation values)
		plt.plot (npDatePlot [npCorrPlotMask], npCorrVals [npCorrPlotMask], linestyle='-', marker='o')
		plt.title ("Correlation Vertical Time Series Part (" + partType + ") _ Variable (" + variable + ")")
		plt.savefig ("timeSeries_" + partType + "_" + variable + "_VerticalScrap")
		plt.close ('all') #After the Plot has been saved, close the figure in order to free up memory
		