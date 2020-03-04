import numpy as np
import pandas as pd



data_raw_scrap = pd.read_csv ("c:\\Users\\SCarron\\OneDrive - Schlumberger\\Desktop\\analysis\\dataCleaning\\scrap_raw_data.csv")
data_raw_wo = pd.read_csv ("c:\\Users\\SCarron\\OneDrive - Schlumberger\\Desktop\\analysis\\dataCleaning\\wo_raw_data.csv")

print "Raw Scrap Data Head: ", data_raw_scrap.head ()
print "Raw WO Data Head: ", data_raw_wo.head ()


def adjustRawData (data_raw_scrap, data_raw_wo):
	adjustment = None

	#Because the separate WO and Scrap datasets ARE NOT guaranteed to be the same length, if one is longer than the other, the shorter one needs to have a length that matches the other
	#This is necessary so that Numpy.Where() can be used for obtaining the Scrap WO# based on the matching the Scrap FROM WO# with a given WO ID in the Work Order dataset
	#If the datasets are of DIFFERENT length, Numpy.Where() throws an error that the function could not broadcast the columns together
	if data_raw_scrap.shape [0] > data_raw_wo.shape [0]:
		
		print "Entered Row Adjustment for Data Raw WO because Scrap has more rows than WO\n\n"
		
		'''
		for column in data_raw_wo.columns:
			
			adjustment = data_raw_wo [column].append (pd.Series (np.repeat (None, data_raw_scrap.shape [0] - data_raw_wo.shape [0])))
		'''
		#Calculate the number of FILLER cells needed for adjusting the shorter datasest to match the length of the longer dataset
		data = np.repeat (None, (data_raw_scrap.shape [0] - data_raw_wo.shape [0])*len(data_raw_wo.columns))
		#Create a FILLER DataFrame using the calculated number of FILLER cells above
		adjustment = pd.DataFrame (data = data.reshape (data_raw_scrap.shape [0] - data_raw_wo.shape [0], data_raw_wo.shape [1]), index = range (data_raw_scrap.shape [0] - data_raw_wo.shape [0]), columns = data_raw_wo.columns) #
		#Append the FILLER DataFrame to the SHORTER DataFrame
		data_raw_wo = data_raw_wo.append (adjustment)

		print "Appended the Adjustment to the end of the Data Raw WO df"
		print "Data Raw WO df AFTER appending Adjustment: ", data_raw_wo.shape
			
	elif data_raw_wo.shape [0] > data_raw_scrap.shape [0]:
		
		print "Entered Row Adjustment for Data Raw Scrap because Wo has more rows than Scrap\n\n"
		
		'''
		for column in data_raw_scrap.columns:
			
			adjustment = data_raw_scrap [column].append (pd.Series (np.repeat (None, data_raw_wo.shape [0] - data_raw_scrap.shape [0])))
		'''
		#Calculate the number of FILLER cells needed for adjusting the shorter datasest to match the length of the longer dataset
		data = np.repeate (None, (data_raw_wo.shape [0] - data_raw_scrap.shape [0])*data_raw_scrap.shape [1])
		#Create a FILLER DataFrame using the calculated number of FILLER cells above
		adjustment = pd.DataFrame (data = data.reshape (data_raw_wo.shape [0] - data_raw_scrap.shape [0], data_raw_scrap.shape [1]), index = range (data_raw_wo.shape [0] - data_raw_scrap.shape [0]), columns = data_raw_scrap.columns)
		#Append the FILLER DataFrame to the SHORTER DataFrame
		data_raw_scrap = data_raw_scrap.append (adjustment)
			
			
	print "Data Raw Scrap Shape: ", data_raw_scrap.shape
	print "Data Raw WO Shape: ", data_raw_wo.shape
	print "Row Adjustment: ", adjustment.shape



#Columns names for the WO and Scrap portions of the compilation file
#<WO Portion> WO ID SFG/Rhodes/Stinger,	Assembly,	Description,	Class Code,	Type,	Size,	Bevel,	Size and Type,	Size and Bevel,	SFG WO Completion Date,	SFG Completed Qty,	 SFG Scrapped Qty,	
#<Scrap Portion>	WO ID FI,	FI Assembly,	FI Description,	Class Code,	FI Type,	FI Size,	FI Bevel,	FI Size and Type,	FI Size and Vevel,	FI WO Completion Date,	 FI Completed Qty,	FI Scrapped Qty,	
#<Scrap Code Portion> 1001	1002	1004	1005	1006	1007	1009	1011	1012	1013	1014	1015	1016	1017	1018	1019	1020	1021	1022	1023	1024	1025	1026	1027	1028	1029	1030	1031	1033	1034	1035	1036	1037	1038	1040	1044	1045	1046	1047	1048	1049	1050	1053	1055	1056	1057	1058	1059	1060	1061	1062	1063	1064	1065	1066	1068	1070	1071	1072	1073	1101	1102	1103	1104	1105	1108	1113	1133	1141	1152	1160	1162	1164	1168	1180	1200	1201	1202	7004	7029	7034	7064	7162	8004	9000	blank	Total Scrap	Diff
data_wo_columns = {"WO ID SFG/Rhodes/Stinger":"Work Order", "Assembly":"Assembly", "Description":"Desciption", "Class Code":"Class Code", "Type":"Part Type", "Size":"Desciption", "Bevel":"Desciption", "Size and Type":"Desciption", "Size and Bevel":"Desciption", "SFG WO Completion Date":"Date Completed", "SFG Completed Qty":"Completed Qty", "SFG Scrapped Qty":"Scrapped Qty"}
data_scrap_columns = {"FI Assembly":"Assembly", "FI Description":"Desciption", "FI Class Code":"Class Code", "FI Type":"Part Type", "FI Size":"Desciption", "FI Bevel":"Desciption", "FI Size and Type":"Desciption", "FI Size and Bevel":"Desciption", "FI WO Completion Date":"Date Completed", "FI Completed Qty":"Completed Qty", "FI Scrapped Qty":"Scrapped Qty"} #"WO ID FI":("WO #", "From WO#"), 
data_scrapcode_columns = [1001, 1002, 1004, 1005, 1006, 1007, 1009, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1033, 1034, 1035, 1036, 1037, 1038, 1040, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1053, 1055, 1056, 1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1068, 1070, 1071, 1072, 1073, 1101, 1102, 1103, 1104, 1105, 1108, 1113, 1133, 1141, 1152, 1160, 1162, 1164, 1168, 1180, 1200, 1201, 1202, 7004, 7029, 7034, 7064, 7162, 8004, 9000, ""]#	Total Scrap	Diff]
#["1001", "1002", "1004", "1005", "1006", "1007", "1009", "1011", "1012", "1013", "1014", "1015", "1016", "1017", "1018", "1019", "1020", "1021", "1022", "1023", "1024", "1025", "1026", "1027", "1028", "1029", "1030", "1031", "1033", "1034", "1035", "1036", "1037", "1038", "1040", "1044", "1045", "1046", "1047", "1048", "1049", "1050", "1053", "1055", "1056", "1057", "1058", "1059", "1060", "1061", "1062", "1063", "1064", "1065", "1066", "1068", "1070", "1071", "1072", "1073", "1101", "1102", "1103", "1104", "1105", "1108", "1113", "1133", "1141", "1152", "1160", "1162", "1164", "1168", "1180", "1200", "1201", "1202", "7004", "7029", "7034", "7064", "7162", "8004", "9000", "blank"]#	Total Scrap	Diff]
data_output_columns = ["WO ID SFG/Rhodes/Stinger", "Assembly", "Description", "Class Code", "Type", "Size", "Bevel", "Size and Type", "Size and Bevel", "SFG WO Completion Date", "SFG Completed Qty", "SFG Scrapped Qty", "FI WO ID", "FI Assembly", "FI Description", "FI Class Code", "FI Type", "FI Size", "FI Bevel", "FI Size and Type", "FI Size and Bevel", "FI WO Completion Date", "FI Completed Qty", "FI Scrapped Qty", 1001, 1002, 1004, 1005, 1006, 1007, 1009, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1033, 1034, 1035, 1036, 1037, 1038, 1040, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1053, 1055, 1056, 1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1068, 1070, 1071, 1072, 1073, 1101, 1102, 1103, 1104, 1105, 1108, 1113, 1133, 1141, 1152, 1160, 1162, 1164, 1168, 1180, 1200, 1201, 1202, 7004, 7029, 7034, 7064, 7162, 8004, 9000, ""]
data_output_woscrap = pd.DataFrame (columns = data_output_columns)





'''
for wo_key in data_wo_columns.keys ():
	
	data_output_woscrap [wo_key] = data_raw_wo [data_wo_columns [wo_key]]
	#print "Current WO Data Key: ", wo_key, "\n\n"
'''

#data_output_woscrap ["FI WO ID"] = pd.Series ([])	







def identifyWOMatches (data_raw_scrap, data_raw_wo):
	#I tried using numpy.where() for identifying where the Scrap CSV and WO CSV match on "Scrap -> From WO#" = "WO -> Work Order", but because the datasets are two different sizes, the numpy.where() approach was not working as hoped
	#I then found this numpy.intersect1d() approach (this is part of Scipy, from what I can tell) and it appears to not be concerned with differences in array sizes
	#I'll use the SECOND set of returned indices for identifying the "WO #" values that should be kept from the Scrap CSV for the Output file
	#I'll use the FIRST set of returned indices for identifying the information from WO CSV that will be used for filling in the REST of the Scrap PORTION of the compilation file
	data_raw_womatches = np.intersect1d (data_raw_wo ["Work Order"], data_raw_scrap ["From WO#"], assume_unique=False, return_indices=True)
	data_raw_womatches = pd.Series (data_raw_womatches)
	
	#Capture the WO IDs NOT in both the RAW Work Order and RAW Scrap datasets (in case there are fewer of these)
	data_raw_nomatches = set (data_raw_wo ["Work Order"].tolist ()) - set (data_raw_womatches [0].tolist ())
	

	print "Head of Matching WO IDs for WO and Scrap Raw Data: ", data_raw_womatches.head ()
	print "Number of elements in Match WO IDs: ", data_raw_womatches.count ()
	print "Number of WO IDs that Match: ", len (data_raw_womatches [0])


	print "Data Raw Scrap 'From WO#' Shape: ", data_raw_scrap ["From WO#"].shape
	print "Data Raw Scrap 'WO #' Shape: ", data_raw_scrap ["WO #"].shape
	print "Data OutPut 'FI WO ID' Shape: ", data_output_woscrap ["FI WO ID"].shape


	#Testing to see if the data_raw_womatches is a Pandas Series of 3 lists now
	#pd.Series (data_raw_womatches [0]).to_csv ("woscrap_match_ids_0.csv")
	#pd.Series (data_raw_womatches [1]).to_csv ("woscrap_match_ids_1.csv")
	#pd.Series (data_raw_womatches [2]).to_csv ("woscrap_match_ids_2.csv")


	#This portion of code is for tryiing to identify cases in the RAW SCRAP Data where a given "From WO#" matches MULTIPLE "WO #" values
	#data_raw_scrapmultiwo = {}
	data_raw_scrapmultiwo = []

	for wo_id in data_raw_womatches [0].tolist ():
		
		#If the current wo_id that matches a RAW Scrap "FROM WO#" maps to multiple values in RAW Scrap "WO #", then a problem has been encountered in the data
		if len (data_raw_scrap ["WO #"] [data_raw_scrap ["From WO#"] == wo_id].unique ()) > 1:
			
			#data_raw_scrapmultidf [wo_id] = data_raw_scrap ["WO #"] [data_raw_scrap ["From WO#"] == wo_id].unique ()
			data_raw_scrapmultiwo.append (wo_id)
	
	return data_raw_womatches, data_raw_scrapmultiwo

		
		

		
		
		
		
		
		


#This will store a separate one-line DataFrame corresponding to each RAW Work Order WO ID that DOES match with RAW Scrap "From WO#" (AND that DOESN'T match to MULTIPLE RAW Scrap "WO #" IDs)
data_interdf_dict = {}
data_wocount_dict = {}
#This will store data relatd to those WO IDs from RAW Work Order that DON'T match with RAW Scrap "From WO#" IDs
#data_skipdf_dict = {}
data_skipdf_df = pd.DataFrame (columns = data_output_columns)
def composeWorkOrderCompilation (data_raw_wo, data_raw_womatches, data_raw_scrapmultiwo, data_skipdf_df):

	for wo_id in data_raw_wo ["Work Order"].tolist ():#matches [0].tolist ():#data_raw_wo ["Work Order"].unique ():
		
		#For Monday 2/25/2019: Only pull in the data IF the MATCHED WO does NOT match multiple RAW SCRAP "WO #"
		if wo_id in data_raw_womatches [0].tolist () and not (wo_id in data_raw_scrapmultiwo):
			data_interdf_dict [wo_id] = pd.DataFrame (columns = data_output_columns)
			data_insert_df = data_raw_wo [data_wo_columns.values ()] [data_raw_wo ["Work Order"] == wo_id]
			data_insert_df.columns = data_wo_columns.keys ()
			data_interdf_dict [wo_id] = data_interdf_dict [wo_id].append (data_insert_df, sort=False)
			#for wo_key in data_wo_columns.keys ():
			
			#	data_interdf_dict [wo_id] [wo_key] = data_raw_wo [data_wo_columns [wo_key]] [data_raw_wo ["Work Order"] == wo_id]
		
		else:
			#data_skipdf_dict [wo_id] = pd.DataFrame (columns = data_output_columns)
			data_insert_df = data_raw_wo [data_wo_columns.values ()] [data_raw_wo ["Work Order"] == wo_id]
			data_insert_df.columns = data_wo_columns.keys ()
			#data_skipdf_dict [wo_id] = data_skipdf_dict [wo_id].append (data_insert_df, sort=False)
			data_skipdf_df = data_skipdf_df.append (data_insert_df, sort=False)
			#for wo_key in data_wo_columns.keys ():
				
			#	data_skipdf_dict [wo_id] [wo_key] = data_raw_wo [data_wo_columns [wo_key]] [data_raw_wo ["Work Order"] == wo_id]
	return data_skipdf_df


				
				
				
				
				

data_multiscrap_dict = {}
scrap_codeqty_dict = {}
scrap_ficolumn_dict = {}
def composeWorkOrderFI (data_raw_scrap, data_raw_wo, data_interdf_dict):
	for df_id in data_interdf_dict.keys ():
		
		'''
		#Verify that the Work Order From RAW Work Order actually match with From WO# in the RAW Scrap`
		print "Looking for ", df_id, " in RAW SCRAP From WO#\n"
		
		if df_id in data_raw_scrap ["From WO#"].tolist ():
			print "Found ", df_id, " in RAW SCRAP From WO#\n\n"
		'''
		
		'''
		#Check if and of the RAW Scrap From WO#s match with multitple RAW Scrap WO #s
		print "Looking for any RAW Scrap From WO#s that match Multiple RAW Scrap WO #s\n"
		if len (data_raw_scrap ["WO #"] [data_raw_scrap ["From WO#"] == df_id].unique ()) > 1:
			
			data_multiscrap_dict [df_id] = True
		'''
		
		
		#Identify what DATATYPE the return value is from subsetting the Dataframe for the matching Work Order id and RAW Scrap From WO#
		'''
		print "RAW Scrap WO # for the current (From WO#", data_raw_scrap ["From WO#"] [data_raw_scrap ["From WO#"] == df_id], " == ", df_id, "): ", data_raw_scrap ["WO #"] [data_raw_scrap ["From WO#"] == df_id].unique (), "\n"
		print "DType of above RAW Scrap WO #: ", type (data_raw_scrap ["WO #"] [data_raw_scrap ["From WO#"] == df_id]), "\n"
		print "Length of above RAW Scrap WO #: ", len (data_raw_scrap ["WO #"] [data_raw_scrap ["From WO#"] == df_id].unique ()), "\n\n"
		
		print "RAW Scrap WO # for the current (From WO#", np.where (data_raw_scrap ["From WO#"] == df_id, data_raw_scrap ["From WO#"], "No Input Value Found"), " == ", df_id, "): ", np.where (data_raw_scrap ["From WO#"] == df_id, data_raw_scrap ["WO #"], "No Output Value Found").tolist (), "\n"
		print "DType of above RAW Scrap WO #: ", type (np.where (data_raw_scrap ["From WO#"] == df_id, data_raw_scrap ["WO #"], "No Output Value Found")), "\n"
		print "Length of above RAW Scrap WO #: ", len (np.where (data_raw_scrap ["From WO#"] == df_id, data_raw_scrap ["WO #"], "No Output Value Found").tolist ()), "\n\n"
		'''
		
		#The below format for subsetting the Dataframe was unnecessary
		#data_interdf_dict [df_id] ["FI WO ID"] = data_raw_scrap ["WO #"] [data_raw_scrap ["From WO#"].astype (str) == str (df_id)]
		#np.where (data_raw_scrap ["From WO#"] == wo_id, data_raw_scrap ["WO #"], data_interdf_dict [wo_id] ["FI WO ID"])
		
		#This is the successful format for subsetting the Dataframe
		fi_id = data_raw_scrap ["WO #"] [data_raw_scrap ["From WO#"] == df_id].unique () [0]
		data_interdf_dict [df_id] ["FI WO ID"] = fi_id
	
	

#This accompanies the section in the above code block that relates to checking how many RAW Scrap From WO#s match multiple RAW Scrap WO #s
#print "The number of RAW Scrap From WO#s that match Multiple RAW Scrap WO #s is: ", len (data_multiscrap_dict.keys ()), "\n\n"


'''
for df_id in data_interdf_dict.keys ():
	
	for wo_id in data_interdf_dict [df_id] ["FI WO ID"]:
		
		for scrap_id in data_scrapcode_columns:
			
			current_scrap_code = data_raw_scrap ["Code"] [(data_raw_scrap ["From WO#"] == df_id) & (data_raw_scrap ["WO #"] == wo_id)].tolist ()
			
			if scrap_id in current_scrap_code:
				
				data_interdf_dict [df_id] [scrap_id] = data_raw_scrap ["Quantity"] [(data_raw_scrap ["From WO#"] == df_id) & (data_raw_scrap ["WO #"] == wo_id) & (data_raw_scrap ["Code"] == scrap_id)]
				
		for scrap_key in data_scrap_columns.keys ():
			
			data_interdf_dict [df_id] [scrap_key] = data_raw_wo [data_scrap_columns [scrap_key]] [data_raw_wo ["Work Order"] == wo_id]
'''
def composeScrapFI (data_raw_scrap, data_raw_wo, data_interdf_dict):
	#for df_id in scrap_codeqty_dict.keys ():
	for df_id in data_interdf_dict.keys ():
		
		for scrap_key in data_scrap_columns.keys ():
			
			scrap_id = data_scrap_columns [scrap_key]
			
			fi_id = data_raw_scrap ["WO #"] [data_raw_scrap ["From WO#"] == df_id].unique () [0]
			
			data_interdf_dict [df_id] [scrap_key] = data_raw_wo [scrap_id] [data_raw_wo ["Work Order"] == fi_id]
			
			if fi_id in data_raw_wo ["Work Order"]:
				
				scrap_ficolumn_dict [fi_id] = 1
		
		#scrap_codeqty_dict [df_id] = {}
		for code_id in data_raw_scrap ["Code"] [data_raw_scrap ["From WO#"] == df_id].unique ():
			
			if len (data_raw_scrap ["Quantity"] [(data_raw_scrap ["From WO#"] == df_id) & (data_raw_scrap ["Code"] == code_id)].unique ()) > 0:
				
				#scrap_codeqty_dict [df_id] [code_id] = data_raw_scrap ["Quantity"] [(data_raw_scrap ["From WO#"] == df_id) & (data_raw_scrap ["Code"] == code_id)].unique () [0]
				data_interdf_dict [df_id] [code_id] = data_raw_scrap ["Quantity"] [(data_raw_scrap ["From WO#"] == df_id) & (data_raw_scrap ["Code"] == code_id)].unique () [0]
		
		'''
		scrap_codeqty_dict [df_id] = {}
		for code_id in data_raw_scrap ["Code"] [data_raw_scrap ["From WO#"] == df_id].unique ():
			
			if len (data_raw_scrap ["Quantity"] [(data_raw_scrap ["From WO#"] == df_id) & (data_raw_scrap ["Code"] == code_id)].unique ()) > 0:
				
				scrap_codeqty_dict [df_id] [code_id] = data_raw_scrap ["Quantity"] [(data_raw_scrap ["From WO#"] == df_id) & (data_raw_scrap ["Code"] == code_id)].unique () [0]
		
		
		for code_id in scrap_codeqty_dict [df_id].keys ():
			
			data_interdf_dict [df_id] [code_id] = scrap_codeqty_dict [df_id] [code_id]
		'''

def composeTotalCompilation (data_output_woscrap, data_skipdf_df):
	for df_id in data_interdf_dict.keys ():
		
		data_output_woscrap = data_output_woscrap.append (data_interdf_dict [df_id], sort=False)
		
	#for df_id in data_skipdf_dict.keys ():
	#	data_output_woscrap = data_output_woscrap.append (data_skipdf_dict [df_id], sort=False)
	data_output_woscrap = data_output_woscrap.append (data_skipdf_df, sort=False)
			
			
	print "Raw Scrap Index: ", data_raw_scrap.index, "\n\n"
	print "Raw WO Index: ", data_raw_wo.index, "\n\n"
	print "Unique values in Data Output FI WO ID: ", len (data_output_woscrap ["FI WO ID"].unique ()), "\n\n"

	print "The Number of FI WO IDs found in the RAW Work Order data: ", len (scrap_ficolumn_dict.keys ()), "\n\n"
	
	return data_output_woscrap











#Call the functions on the input data in the appropriate order for composing the desired output dataset	
adjustRawData (data_raw_scrap, data_raw_wo)

data_raw_womatches, data_raw_scrapmultiwo = identifyWOMatches (data_raw_scrap, data_raw_wo)

data_skipdf_df = composeWorkOrderCompilation (data_raw_wo, data_raw_womatches, data_raw_scrapmultiwo, data_skipdf_df)

composeWorkOrderFI (data_raw_scrap, data_raw_wo, data_interdf_dict)

composeScrapFI (data_raw_scrap, data_raw_wo, data_interdf_dict)

data_output_woscrap = composeTotalCompilation (data_output_woscrap, data_skipdf_df)



#Force the desired column order in the output and then output the data to desired csv filename
data_output_woscrap = data_output_woscrap [data_output_columns]
data_output_woscrap.to_csv ("woscrap_cleaner_output_dataframe_dictionary_18.csv")
data_raw_womatches.to_csv ("woscrap_match_ids.csv")		

		
'''

#pd.DataFrame.from_dict (data_raw_scrapmultiwo, orient='columns').to_csv ("woscrap_scrap_multiwo.csv")
#pd.Series (data_raw_scrapmultiwo).to_csv ("woscrap_scrap_multiwo.csv") #This line has the correct "to_csv" method call
	

#for wo_id in data_raw_wo ["Work Order"].unique ():
#I think this (for wo_id in data_raw_womatches [0]) might be part of the problem with the WOScrap Output. data_raw_womatches starts as the result of a call to Numpy.Intersect1d () and the return value is an an array of 3 lists, which I am then currently passing to
#Pandas.Series () to create a Series. I don't know, at that point, if data_raw_womatches [0] is referring to the same list of matched work order IDs that are originally returned from the Numpy.Intersect1d () call
#This also seemed to cause a problem (for wo_id in np.nditer (data_raw_womatches [0], flags=["refs_ok"])) because I encountered an error at the end of the script: "ValueError: Buffer has wrong number of dimensions (expected 1, got 0)

for wo_id in data_raw_womatches [0].tolist ():
	
	#As long as the current wo_id (that is a match between RAW WO and RAW Scrap) IS NOT one of the problematic RAW Scrap "From WO#" ids identified in above, then move forward on building the cleaned output dataset with it
	if not (wo_id in set (data_raw_scrapmultiwo)):
		
		data_output_woscrap ["FI WO ID"] [data_output_woscrap ["WO ID SFG/Rhodes/Stinger"] == wo_id] =  np.where (data_raw_scrap ["From WO#"] == wo_id, data_raw_scrap ["WO #"], data_output_woscrap ["FI WO ID"])#data_raw_scrap ["From WO#"].iloc [wo_number]#np.where (data_raw_wo ["Work Order"] == data_raw_scrap ["From WO#"], data_raw_scrap ["WO #"], "")
		#data_output_woscrap ["FI WO ID"] [data_output_woscrap ["WO ID SFG/Rhodes/Stinger"] == wo_id] =  np.where (data_raw_scrap ["From WO#"] == wo_id, data_raw_scrap ["WO #"], data_output_woscrap ["FI WO ID"])#data_raw_scrap ["From WO#"].iloc [wo_number]#np.where (data_raw_wo ["Work Order"] == data_raw_scrap ["From WO#"], data_raw_scrap ["WO #"], "")
		#data_output_woscrap ["FI WO ID"] =  np.where (data_raw_scrap ["From WO#"] == data_raw_wo ["Work Order"], data_raw_scrap ["WO #"], data_output_woscrap ["FI WO ID"])#data_raw_scrap ["From WO#"].iloc [wo_number]#np.where (data_raw_wo ["Work Order"] == data_raw_scrap ["From WO#"], data_raw_scrap ["WO #"], "")
		
		'' '
		for scrap_key in data_scrap_columns.keys ():
			
			#Pull information from RAW WO to fill in the FI information based on where the 
			#data_output_woscrap [scrap_key] [data_output_woscrap ["WO ID SFG/Rhodes/Stinger"] == wo_id] = np.where (data_raw_scrap ["From WO#"] == wo_id, data_raw_wo [data_scrap_columns [scrap_key]], data_output_woscrap [scrap_key])
			data_output_woscrap [scrap_key] [data_output_woscrap ["WO ID SFG/Rhodes/Stinger"] == wo_id] = np.where (data_raw_wo ["Work Order"] == wo_id, data_raw_wo [data_scrap_columns [scrap_key]], data_output_woscrap [scrap_key])
		'' '
#If the FI WO ID matches a RAW WO ID, then pull in the respective information from RAW WO to fill in the scrap information for that FI WO ID
#This replaces the code in the Orange BLOCK Comment in the previous code block
for wo_id in data_output_woscrap ["FI WO ID"].tolist ():

	for scrap_key in data_scrap_columns.keys ():
	
		data_output_woscrap [scrap_key] [data_output_woscrap ["FI WO ID"] == wo_id] = np.where (data_raw_wo ["Work Order"] == wo_id, data_raw_wo [data_scrap_columns [scrap_key]], data_output_woscrap [scrap_key])


#For each FI WO ID, populate the respective Scrap Code Columns with the matching data		
for wo_id in data_output_woscrap ["FI WO ID"].tolist ():
	
	data_raw_currentscrap = data_raw_scrap [data_raw_scrap.columns] [data_raw_scrap ["WO #"] == wo_id]
	
	for scrap_code in data_scrapcode_columns:
		
		if scrap_code in data_raw_currentscrap ["Code"].unique ():
			
			#data_output_woscrap [scrap_code] = np.where (data_raw_currentscrap ["Code"] == scrap_code, data_raw_currentscrap ["Quantity"], data_output_woscrap [scrap_code])
			data_output_woscrap [scrap_code] [data_output_woscrap ["FI WO ID"] == wo_id] = np.where (data_raw_currentscrap ["Code"] == scrap_code, data_raw_currentscrap ["Quantity"], data_output_woscrap [scrap_code] [data_output_woscrap ["FI WO ID"] == wo_id])
	
print "Raw Scrap Index: ", data_raw_scrap.index, "\n\n"
print "Raw WO Index: ", data_raw_wo.index, "\n\n"
print "Unique values in Data Output FI WO ID: ", len (data_output_woscrap ["FI WO ID"].unique ())

data_output_woscrap.to_csv ("woscrap_cleaner_output_4.csv")
data_raw_womatches.to_csv ("woscrap_match_ids.csv")

		
'' '
#Initialize SETS to contain the columns for data pulled from the SCRAP sheet for the scrap compilation and one to contain the columns for data pulled from the WO sheet for the scrap compilation 
for scrap_column in data_scrap_columns.keys ():
	
	data_output_woscrap [scrap_column] = np.where (data_output_woscrap ["FI WO ID"] != "", data_raw_wo [data_scrap_columns [scrap_column]], "")
	
	
print "Output Wo Data Head: ", data_output_woscrap.head ()
'' '

'''