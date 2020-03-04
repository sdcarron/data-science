import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




data = pd.read_csv ("C:\\Users\\SCarron\\Desktop\\compilation.csv", low_memory=False)







for partType in data ["SFG Part Family"].unique ():

	for date in data ["Year-Month Press"].unique ():
	
		dataFilter = data [["Part Size", "Total Crack Scrap", "1064 CRACK - EDGE, INTERFACIAL", "1152 CRACK - VERTICAL", "Total Starts", "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "Resistance Avg", "TempTC Avg", "Offset Delta (E-S) Avg", "TIMEbRuns Avg", "Press"]] [(data ["Part Size"].notnull()) & (data ["SFG Part Family"] == partType) & (data ["SFG Part Family"].notnull ()) & (data ["Total Crack Scrap"].notnull ()) & (data ["Total Starts"].notnull ()) & (data ["Bad Carbide flag"] == "Good") & (data ["Carbide Density"].notnull ()) & (data ["Carbide MS"].notnull ()) & (data ["Carbide HC"].notnull ()) & (data ["PCD Density"].notnull ()) & (data ["Year-Month Press"] == date) & (data ["Power Avg"].notnull ()) & (data ['Resistance Avg'].notnull ()) & (data ["TempTC Avg"].notnull ()) & (data ['Delta Offset (E-S) Avg'].notnull ()) & (data ["TIMEbRuns Avg"].notnull ()) & (data ["Press"].notnull ())]
	
		for column in dataFilter.columns.values:
		
			if column != "Total Crack Scrap" and column != "1064 CRACK - EDGE, INTERFACIAL" and column != "1152 CRACK - VERTICAL":
			
				fig = plt.figure (figsize=(19.2,10.8), dpi=100)
				plt.scatter (dataFilter [column], dataFilter ["Total Crack Scrap"])
				plt.title (str (partType) + "_" + str (date) + "_TotalCrackScrap")
				plt.xlabel (column)
				plt.ylabel ("Total Crack Scrap")
				#plt.show ()
				plt.savefig (str (partType) + "_" + str (date) + "_TotalCrackScrap_Plot.png")
				
				
				#if partType.find ("D82") != -1:
				
				
				
				
				
				
				# ax1 = figInterfacial.add_subplot(111)
				# cmap = cm.get_cmap('jet', 30)
				# cax = ax1.imshow(corrInterfacial, interpolation="nearest", cmap=cmap)
				# ax1.grid(True)
				# plt.title(str (partType) + "_" + str (date) + "_Interfacial")
				# labels=["Part Size", "Crack IF", "Total Starts", "Carbide Density", "Carbide MS", "Carbide HC", "PCD Density", "Power Avg", "TempTC Avg", "TIMEbRuns Avg", "Press"]
				
				# #Force ALL of the varible names to be displayed
				# ax1.set_xticks(np.arange(len(labels)))
				# ax1.set_yticks(np.arange(len(labels)))
				
				# # Make x-axis variable names display vertically
				# ax1.xaxis.label.set_rotation(90)
				# # Make y-axis variable names display horizontally
				# ax1.yaxis.label.set_rotation (0)
				
				# #Force the tick marks to be identified by the variable names
				# ax1.set_xticklabels(labels,fontsize=6)
				# ax1.set_yticklabels(labels,fontsize=6)
				
				# # Add colorbar, make sure to specify tick locations to match desired ticklabels
				# fig.colorbar(cax, ticks=[.75,.8,.85,.90,.95,1])
				
				figInterfacial = plt.figure(figsize=(19.2,10.8), dpi=100)
				plt.scatter (dataFilter [column], dataFilter ["1064 CRACK - EDGE, INTERFACIAL"])
				plt.title (str (partType) + "_" + str (date) + "_Interfacial")
				plt.xlabel (column)
				plt.ylabel ("Interfacial Crack")
				plt.savefig (str (partType) + "_" + str (date) + "_Interfacial_Plot.png")
				
				
				
				
				figVertical = plt.figure (figsize=(19.2,10.8), dpi=100)
				plt.scatter (dataFilter [column], dataFilter ["1152 CRACK - VERTICAL"])
				plt.title (str (partType) + "_" + str (date) + "_Vertical")
				plt.xlabel (column)
				plt.ylabel ("Vertical Crack")
				plt.savefig (str (partType) + "_" + str (date) + "_Vertical_Plot.png")
	
		