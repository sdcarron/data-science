from JoblotDataConstruction import joblotdataconstructor as jc
import pandas as pd
import numpy as np
import os
import re
import sys
import datetime as dt

from functools import reduce


class CarbideComponentReconciler (object):
	
	
	
	
	def __init__(self, directory_base = os.getcwd ()):
		
		self.directory_acs = directory_base + "\\Access\\"
		self.directory_coc = directory_base + "\\CoC\\"
		self.directory_jlc = directory_base + "\\JoblotDataConstruction\\"
		self.directory_old = directory_base
		
		self.filelist_acs = os.listdir (self.directory_acs)
		self.filelist_coc = os.listdir (self.directory_coc)
		self.filelist_jlc = None #os.listdir (self.directory_jlc + "\\output\\")
		
		self.raw_acs = pd.DataFrame ()
		self.raw_coc = pd.DataFrame ()
		self.raw_jlc = pd.DataFrame ()
		#self.out_ccr = pd.DataFrame ()
		
		self.matches_trueALL = []
		self.matches_trueALLIndices = []
		
		self.matches_trueACSCOC = []
		self.matches_trueACSCOC_ACSIndices = []
		self.matches_trueACSCOC_COCIndices = []
		
		self.matches_trueACSJLC = []
		self.matches_trueACSJLC_ACSIndices = []
		self.matches_trueACSJLC_JLCIndices = []
		
		self.matches_onlyACS = []
		self.matches_onlyCOC = []
		self.matches_onlyJLC = []
		#matches_trueALL, matches_trueACSCOC, matches_trueACSJLC, matches_onlyACS, matches_onlyCOC, matches_onlyJLC
		
		self.JoblotDataConstructor = jc#.JoblotDataConstructor (os.getcwd () + "\\JoblotDataConstruction\\")
		
	
	
	def PrepareRawDataframes (self):
		
		#filematch = re.search (".py", file)
		for filename in self.filelist_acs:
			current_acs = pd.DataFrame ()
			#If filename includes ".csv", use pd.read_csv
			filematch = re.search (".csv", filename)
			
			if not (filematch is None):
				current_acs = pd.read_csv (self.directory_acs + filename, encoding="latin1")
				self.raw_acs = self.raw_acs.append (current_acs)
				#self.raw_acs = self.raw_acs.drop_duplicates ()
			
			#If filename includes ".xls" or ".xlsx", use pd.read_excel
			else:
				filematch = re.search (".xls", filename)
				
				if not (filematch is None):
					current_acs = pd.read_excel (self.directory_acs + filename)
					self.raw_acs = self.raw_acs.append (current_acs)
					#self.raw_acs = self.raw_acs.drop_duplicates ()
			
			self.raw_acs = self.raw_acs.fillna ("missing")
			self.raw_acs.reset_index (drop=True, inplace=True)
			#self.raw_acs.replace (to_replace=NaN, value="missing")
			#self.raw_acs.where (self.raw_acs.notna(), "missing", axis="columns")
			
			print ("Self Raw ACS shape at insertion: ", self.raw_acs.shape, "\n\n")
			
			
			#Now I need to remove rows from the ACS data that has the following issue:
			#CompLotNum doesn't start with "R" or "r" AND CompLotNum IS NOT just a numeric value
			
		#self.raw_acs = self.raw_acs [((self.raw_acs ["CompLotNum"].str.find ("r") == 1) & (self.raw_acs ["CompLotNum"].str.find ("R") == 1)) | (self.raw_acs ["CompLotNum"].str.isnumeric () == True)]
			
		
		
		for filename in self.filelist_coc:
			current_coc = pd.DataFrame ()
			#If filename includes ".csv", use pd.read_csv
			filematch = re.search (".csv", filename)
			
			if not (filematch is None):
				current_coc = pd.read_csv (self.directory_coc + filename, encoding="latin1")
				self.raw_coc = self.raw_coc.append (current_coc)
				#self.raw_coc = self.raw_coc.drop_duplicates ()
			
			#If filename includes ".xls" or ".xlsx", use pd.read_excel
			else:
				filematch = re.search (".xls", filename)
				
				if not (filematch is None):
					current_coc = pd.read_excel (self.directory_coc + filename, sheet_name="Sheet1")
					self.raw_coc = self.raw_coc.append (current_coc)
					#self.raw_coc = self.raw_coc.drop_duplicates ()
			
			self.raw_coc = self.raw_coc.fillna ("missing")
			self.raw_coc.reset_index (drop=True, inplace=True)
			#self.raw_coc.replace (to_replace=NaN, value="missing")
			#self.raw_coc.where (self.raw_coc.notna (), "missing", axis="columns")
			
			print ("Self Raw COC Shape at insertion: ", self.raw_coc.shape, "\n\n")
		
		
		if len (sys.argv) > 1:
			
			print ("In Prepare DataFrames and Length of Sys.Argv = ", len (sys.argv), "\n\n")
			
			print ("Sys.Argv 1 = ", sys.argv [1], "\n\n")
				
			if sys.argv [1].lower () == "y":
				
				self.JoblotDataConstructor.JoblotInputDestruct ()
				self.JoblotDataConstructor.JoblotOutputConstruct ()
				
			self.filelist_jlc = os.listdir (self.directory_jlc + "\\output\\")
			
			for filename in self.filelist_jlc:
				
				#Filename is guaranteed to be ".csv" because it is explicitly outputted as ".csv" in the joblotdataconstructor script
				filematch = re.search (".csv", filename)
				
				if not (filematch is None):
					current_jlc = pd.read_csv (self.directory_jlc + "\\output\\" + filename, encoding="latin1")
					self.raw_jlc = self.raw_jlc.append (current_jlc)
					
				else:
					filematch = re.search (".xls", filename)
					
					if not (filematch is None):
						current_jlc = pd.read_excel (self.directory_jlc + "\\output\\" + filename, sheet_name="Sheet1")
						self.raw_jlc = self.raw_jlc.append (current_jlc)
						
			self.raw_jlc = self.raw_jlc.drop_duplicates ()
			
		else:
			
			self.filelist_jlc = os.listdir (self.directory_jlc + "\\output\\")
			
			for filename in self.filelist_jlc:
				
				#Filename is guaranteed to be ".csv" because it is explicitly outputted as ".csv" in the joblotdataconstructor script
				filematch = re.search (".csv", filename)
				
				if not (filematch is None):
					current_jlc = pd.read_csv (self.directory_jlc + "\\output\\" + filename, encoding="latin1")
					self.raw_jlc = self.raw_jlc.append (current_jlc)
					
				else:
					filematch = re.search (".xls", filename)
					
					if not (filematch is None):
						current_jlc = pd.read_excel (self.directory_jlc + "\\output\\" + filename, sheet_name="Sheet1")
						self.raw_jlc = self.raw_jlc.append (current_jlc)
						
			self.raw_jlc = self.raw_jlc.drop_duplicates ()
			
			
		#Now I need to remove rows from the JLC data that has the following issue:
		#Remove rows where the JLC Description contains "Semi Finished" OR possibly the "production quantity" is a NEGATIVE value
		#self.raw_jlc = self.raw_jlc [(self.raw_jlc ["Description"].str.find ("semi finished") == -1) | (self.raw_jlc ["Description"].str.find ("semi finished") == -1) | (self.raw_jlc ["SFG Qty"] >= 0)]
	
		
		self.raw_jlc = self.raw_jlc.fillna ("missing")
		self.raw_jlc.reset_index (drop=True, inplace=True)
		#self.raw_jlc.replace (to_replace=NaN, value="missing")
		#self.raw_jlc.where (self.raw_jlc.notna (), "missing", axis="columns")
		
		print ("Self Raw JLC Shape at insertion: ", self.raw_jlc.shape, "\n\n")
	
	
	
	def GetCurrentDataframe (self, dataframe):
		
		df = None
		
		if dataframe == "ACS":
			df = self.raw_acs
			
		elif dataframe == "COC":
			df = self.raw_coc
		
		elif dataframe == "JLC":
			df = self.raw_jlc
		
		else:
			df = self.out_ccr
		
		return df
	
	
	
	def PrintCurrentDataframes (self):
		
		print ("Head Self Raw Access: ", self.raw_acs.head (), "\n\n")
		print ("Head Self Raw CoC: ", self.raw_coc.head (), "\n\n")
		print ("Head Self Raw Job Lot Comp: ", self.raw_jlc.head (), "\n\n")
		#print "Head Self Output CCR: ", self.out_ccr.head (), "\n\n"
		
		print ("Shape Self Raw Access: ", self.raw_acs.shape, "\n\n")
		print ("Shape Self Raw CoC: ", self.raw_coc.shape, "\n\n")
		print ("Shape Self Raw Job Lot Comp: ", self.raw_jlc.shape, "\n\n")
		#print "Shape Self Output CCR: ", self.out_ccr.shape, "\n\n"
		
		print ("Null Count Self Raw Access: ", self.raw_acs.isna ().sum (), "\n\n")
		print ("Null Count Self Raw CoC: ", self.raw_coc.isna ().sum (), "\n\n")
		print ("Null Count Self Raw Job Lot Comp: ", self.raw_jlc.isna ().sum (), "\n\n")
		#print "Null Count Self Output CCR: ", self.out_ccr.isnull ().count (), "\n\n"
	
	
	
	def ExpandDimensionsDataframes (self, df1, dataframe1, df2, dataframe2):
		
		#NOTE: It cannot be guaranteed that the first 2 DFs passed in for comparison are going to have the two greatest row counts. Must compare all 3 DF row counts at once and then output the two largest and compare those first
		match = self.CompareDimensionsDataframes (df1, df2)
		
		if match == "DF1":
			
			#Expand DF1's dimensions to match DF2's dimensions for broadcasting
			data = np.repeat ("missing_1", (df2.shape [0] - df1.shape [0])*len(df1.columns))
			#Create a FILLER DataFrame using the calculated number of FILLER cells above
			adjustment = pd.DataFrame (data = data.reshape (df2.shape [0] - df1.shape [0], df1.shape [1]), index = range (df2.shape [0] - df1.shape [0]), columns = df1.columns) #
			#Append the FILLER DataFrame to the SHORTER DataFrame
			df1 = df1.append (adjustment)
		
		elif match == "DF2":
			
			#Expand DF2's dimensions to match DF1's dimensions for broadcasting
			data = np.repeat ("missing_2", (df1.shape [0] - df2.shape [0])*len(df2.columns))
			#Create a FILLER DataFrame using the calculated number of FILLER cells above
			adjustment = pd.DataFrame (data = data.reshape (df1.shape [0] - df2.shape [0], df2.shape [1]), index = range (df1.shape [0] - df2.shape [0]), columns = df2.columns) #
			#Append the FILLER DataFrame to the SHORTER DataFrame
			df2 = df2.append (adjustment)
			
		
		
		if dataframe1 == "ACS":
			self.raw_acs = df1
			
		elif dataframe1 == "COC":
			self.raw_coc = df1
		
		else:
			self.raw_jlc = df1
		
		
		if dataframe2 == "ACS":
			self.raw_acs = df2
		
		elif dataframe2 == "COC":
			self.raw_coc = df2
		
		else:
			self.raw_jlc = df2
			
		#print ("Expanded Dataframe = ", match, "\n\n")
		#print ("DF1 dimensions after expansion: ", df1.shape, "\n\n")
		#print ("DF2 dimensions after expansion: ", df2.shape, "\n\n")
		
		print ("Self Raw ACS shape after expansion: ", self.raw_acs.shape, "\n\n")
		print ("Self Raw COC shape after expansion: ", self.raw_coc.shape, "\n\n")
		print ("Self Raw JLC shape after expansion: ", self.raw_jlc.shape, "\n\n")
		
		#return (df1, df2)
	
	
	
	
	def CompareDimensionsDataframes (self, df1, df2):
		
		match = "EQL"
		
		if df1.shape [0] < df2.shape [0]:
			
			match = "DF1"
		
		elif df1.shape [0] > df2.shape [0]:
			
			match = "DF2"
		
		return match
	
	
	
	
	
	def MergeContentsDataframes (self):
		
		print ("Shape of ACS: ", self.raw_acs.shape, "\n\n")
		print ("Shape of COC: ", self.raw_coc.shape, "\n\n")
		print ("Shape of JLC: ", self.raw_jlc.shape, "\n\n")
		
		headers_combined = self.CombineHeadersDataframes ()
		
		
			
		
		out_1 = self.raw_acs.merge(self.raw_coc,left_on='CompLotNum', right_on='Batch', suffixes=['', '_COC'])
		#out_1.columns = out_1.columns.str.replace ('_COC', '')
		
		out_2 = self.raw_acs.merge(self.raw_jlc,left_on='LotNum', right_on='SFG Lot', suffixes=['', '_JLC'])
		out_2.columns = out_2.columns.str.replace ('_JLC', '')
		
		out_new = out_1.merge (out_2, on='LotNum')
		out_new.columns = out_new.columns.str.replace ('_x', '')
		
		#out_new = out_new [[headers_combined]]
		#out_new = out_new [headers_combined]
		
		#out_new.remove (3)
		#out_new.remove (43)
		#out_new.drop (out_new.columns [[3,43]], axis=1, inplace=True)
		
		
		
		out_new = out_new [((out_new ["CompLotNum"].str.find ("r") == 1) | (out_new ["CompLotNum"].str.find ("R") == 1) | (out_new ["CompLotNum"].str.isnumeric () == True)) | ((out_new ["Description"].str.find ("semi finished") == -1) | (out_new ["Description"].str.find ("semi finished") == -1) | (out_new ["SFG Qty"].astype ("int64") >= 0))]
		#self.raw_jlc = self.raw_jlc [(self.raw_jlc ["Description"].str.find ("semi finished") == -1) | (self.raw_jlc ["Description"].str.find ("semi finished") == -1) | (self.raw_jlc ["SFG Qty"] >= 0)]
		#self.raw_acs = self.raw_acs [(self.raw_acs ["CompLotNum"].str.find ("r") == 1) | (self.raw_acs ["CompLotNum"].str.find ("R") == 1) | (self.raw_acs ["CompLotNum"].str.isnumeric () == True)]
		
		'''
		out_ccr_set = set (out_ccr.columns)
		out_new_set = set (out_new.columns)
		out_diff1_set = out_ccr_set - out_new_set
		out_diff2_set = out_new_set - out_ccr_set
		
		print "out ccr - new columns: ", out_diff1_set, "\n\n"
		print "out new - ccr columns: ", out_diff2_set, "\n\n"
		'''
		
		
		
		
		
		
		'''
		out_ccr = None#pd.DataFrame (data=[], columns=out_new.columns)
		
		if os.path.exists (self.directory_old + "\\composition.csv"):
			out_ccr = pd.read_csv (self.directory_old + "\\composition.csv")
			out_ccr = out_ccr.append (out_new)
		
		else:
			out_ccr = out_new
		'''
		out_ccr = out_new
		
		print ("RAW ACS columns: ", self.raw_acs.columns, "\n\n")
		print ("RAW COC columns: ", self.raw_coc.columns, "\n\n")
		print ("RAW JLC columns: ", self.raw_jlc.columns, "\n\n")
		
		print ("Out NEW columns: ", out_new.columns, "\n\n")
		print ("Out CCR columns: ", out_ccr.columns, "\n\n")
		
		
		
		print ("CCR Shape: ", out_ccr.shape, "\n\n")
		print ("NEW Shape: ", out_new.shape, "\n\n")
		
		
		print ("Shape of CCR: ", out_ccr.shape, "\n\n")
		#.drop(columns=['col_name2', 'col_name3']).rename(columns={'col_name1':'col_name'})
		print ("Unique Batch Count: ", len (out_ccr ["Batch"].unique ()), "\n")
		print ("RAW COC Batch Count: ", len (self.raw_coc ["Batch"].unique ()), "\n\n")
		
		print ("Unique CompLotNum Count: ", len (out_ccr ["CompLotNum"].unique ()), "\n")
		print ("RAW ACS CompLotNum Count: ", len (self.raw_acs ["CompLotNum"].unique ()), "\n\n")
		
		print ("Unique LotNum Count: ", len (out_ccr ["LotNum"].unique ()), "\n")
		print ("RAW ACS LotNum Count: ", len (self.raw_acs ["LotNum"].unique ()), "\n\n")
		
		print ("Unique SFG Lot Count: ", len (out_ccr ["SFG Lot"].unique ()), "\n")
		print ("RAW JLC SFG Lot Count: ", len (self.raw_jlc ["SFG Lot"].unique ()), "\n\n")
		#self.out_ccr.to_csv (os.getcwd () + "outputAllCombined_" + dt.datetime.now ().strftime ("%Y-%m-%d_%H-%M-%S") + "_.csv")
		out_ccr.drop_duplicates ()
		
		
		
		#print ("Data Type of Column Date: ", type (out_ccr ["Date"].tolist () [0]))
		#out_ccr ["Year"] = pd.Series ()
		#out_ccr ["Year"] = out_ccr ["Date"].str.split ("/") [2]
		#for year in out_ccr ["Date"].str.split ("/") [len (out_ccr ["Date"].str.split ("/")) - 1].unique ().tolist ():
		#when I attempted to do above, I encountered this error because there are MANY duplicate rows: "python pandas dataframe split string into columns ValueError: cannot reindex from a duplicate axis"
		dates = out_ccr ["Date"].astype (str).unique ().tolist ()
		years = []
		for date in dates:
			#date = str (date)
			if date.lower () != "missing" and date.lower () != "missing_1" and date.lower () != "missing_2":
				if not (date.split ("-") [0] in years):
					years.append (date.split ("-") [0])
				
		print ("Extracted Years: ", years)
		'''
		for year in years:
			if lower (year) != "missing":
				out_year = out_ccr [out_ccr.columns] [out_ccr ["Date"].str.split ("/") [len (out_ccr ["Date"].str.split ("/")) - 1] == year]
				out_year.to_csv ("composition_" + str (year) + ".csv")
		#out_ccr.to_csv ("composition.csv")
		'''
		
		
		for year in years:
			out_year = out_ccr [out_ccr.columns] [out_ccr ["Date"].astype (str).str.contains (year) == True]
			out_year.to_csv ("composition_" + str (year) + ".csv")
		
		#out_ccr.to_csv ("composition.csv")
	#matches_trueall are indices where all 3 dataframes match
	#matches_true1 are indices where ACS matches COC, but does NOT match JLC
	#matches_false1 are indices where ACS matches NEITHER COC NOR JLC
	#matches_false2 are indices where COC matches NEITHER ACS NOR JLC
	#matches_true2 are indices where ACS matches JLC, but does NOT match COC
	#matches_false3 are indices where ACS matches NEITHER JLC NOR COC
	#matches_false4 are indices where JLC matches NEITHER ACS NOR COC
	def CombineContentsDataframes (self):#, match_indicesAll, match_indicesOnlyACSCOC, match_indicesOnlyACSJLC, match_indicesOnlyACS, match_indicesOnlyCOC, match_indicesOnlyJLC):#, match_indicesTotalACSCOC, match_indicesTotalACSJLC, matches_false3, matches_false4):
		
		#Combine the contents of raw_acs, raw_coc, and raw_jlc
		#Combination takes place on raw_acs ["CompLotNum"] = raw_coc ["Batch"] and on raw_acs ["LotNum"] = raw_jlc ["SFG Lot"]
		#If raw_acs NOT MATCH coc, discard row for that data
		#pass
		headers_combined = self.CombineHeadersDataframes ()
		
		print ("Headers for RAW ACS: ", self.raw_acs.columns.values, "\n\n")
		print ("Headers for RAW COC: ", self.raw_coc.columns.values, "\n\n")
		print ("Headers for RAW JLC: ", self.raw_jlc.columns.values, "\n\n")
		print ("Combined headers: ", headers_combined, "\n\n")
		
		#self.out_ccr.columns = headers_combined
		self.out_ccr = pd.DataFrame (columns=headers_combined)
		
		print ("Headers for OUT CCR: ", self.out_ccr.columns.values, "\n\n")
		
		'''
		self.matches_trueALL = None
		self.matches_trueACSCOC = None
		self.matches_trueACSJLC = None
		self.matches_onlyACS = None
		self.matches_onlyCOC = None
		self.matches_onlyJLC = None
		'''
		
		for index in self.matches_trueALLIndices:#match_indicesAll:
			
			#if (self.raw_acs.iloc [index].tolist () [].find ("missing") == -1) and (self.raw_coc.iloc [index].tolist () [].find ("missing") == -1) and (self.raw_jlc.iloc [index].tolist () [].find ("missing") == -1):
		
			print ("Joining All 3 Dataframes on Index: ", index, "\n\n")
			
			#current_acs = set (self.raw_acs [self.raw_acs.iloc [index]])
			print ("Type of ACS extracted at index: ", type (self.raw_acs.iloc [index]), "\n\n")
			current_acs = self.raw_acs.iloc [index].tolist ()#set (self.raw_acs.iloc [index])
			print ("Shape of ACS for extraction at index: ", index, " IS ", self.raw_acs.shape, "\n\n")
			print ("Extracted the data from ACS at index: ", index, "\n\n")
			print ("Extracted ACS at index: ", index, " === ", current_acs, "\n\n")
			
			#current_coc = set (self.raw_coc [self.raw_coc.iloc [index]])
			print ("Type of COC extracted at index: ", type (self.raw_coc.iloc [index]), "\n\n")
			current_coc = self.raw_coc.iloc [index].tolist ()#set (self.raw_coc.iloc [index])
			print ("Shape of COC for extraction at index: ", index, " IS ", self.raw_coc.shape, "\n\n")
			print ("Extracted the data from COC at index: ", index, "\n\n")
			print ("Extracted COC at index: ", index, " === ", current_coc, "\n\n")
			
			#current_jlc = set (self.raw_jlc [self.raw_jlc.iloc [index]])
			print ("Type of JLC extracted at index: ", type (self.raw_jlc.iloc [index]), "\n\n")
			current_jlc = self.raw_jlc.iloc [index].tolist ()#set (self.raw_jlc.iloc [index])
			print ("Shape of JLC for extraction at index: ", index, " IS ", self.raw_jlc.shape, "\n\n")
			print ("Extracted the data from JLC at index: ", index, "\n\n")
			print ("Extracted JLC at index: ", index, " === ", current_jlc, "\n\n")
			
			current_list = self.CombineContentsExtracted (current_acs, current_coc, current_jlc)
			print ("Current Set from combining the 3 at index: ", index, " === ", current_list, "\n\n")
			
			print ("Extracted the Data from each of the 3 Dataframes at index: ", index, "\n\n")
			#current_list = list (current_set)
			
			current_combinedict = self.CombineContentsDictionary (headers_combined, current_list)
			if current_combinedict [0] is True:
				current_dictionary = current_combinedict [1]#self.CombineContentsDictionary (headers_combined, current_list)
				#current_df = pd.DataFrame (data=current_list, columns=headers_combined)#, na=False)
				current_df = pd.DataFrame (current_dictionary, index=[0])#pd.DataFrame (current_dictionary, orient="columns", index=[0])#pd.DataFrame.from_dict (current_dictionary, orient="columns", index=[0])
				current_df = current_df [headers_combined]
				#current_df = pd.concat ([self.raw_acs [self.raw_acs.iloc [index]], self.raw_coc [self.raw_coc.iloc [index]], self.raw_jlc [self.raw_jlc.iloc [index]]])
				print ("Constructed NEW Insertion Dataframe (single row) by combining data from each of the 3 Dataframes at index: ", index, "\n\n")
				
				print ("Headers for NEW Constructed INSERTION Dataframe: ", current_df.columns, "\n\n")
				print ("Headers for OUTPUT Dataframe: ", self.out_ccr.columns, "\n\n")
				self.out_ccr = self.out_ccr.append (current_df)
				
				print ("out_ccr Shape After Match ALL Insert: ", str (self.out_ccr.shape [0]), ", ", str (self.out_ccr.shape [1]))
				print ("\n\n\n\n")
		
		#Insert data into OUTPUT DF where ACS and COC match, but ACS and JLC do not
		#for index in self.matches_trueACSCOC:#match_indicesOnlyACSCOC:
		for iterator_1 in range (0, len (self.matches_trueACSCOC_ACSIndices) - 1):
			
			index = self.matches_trueACSCOC_ACSIndices [iterator_1]
			
			print ("Joining ACS and COC on index: ", index, "\n\n")
			
			#current_acs = set (self.raw_acs [self.raw_acs.iloc [index]])
			#print "Type of ACS extracted at index: ", type (self.raw_acs.iloc [index]), "\n\n"
			if index != -1 and index < self.raw_acs.shape [0]:
				current_acs = self.raw_acs.iloc [index].tolist ()#set (self.raw_acs.iloc [index])
			else:
				current_acs = list (np.repeat ("missing", len (self.raw_acs.columns)))
			print ("Shape of ACS for extraction at index: ", index, " IS ", self.raw_acs.shape, "\n\n")
			print ("Extracted the data from ACS at index: ", index, "\n\n")
			print ("Extracted ACS at index: ", index, " === ", current_acs, "\n\n")
			
			index = self.matches_trueACSCOC_COCIndices [iterator_1]
			#current_coc = set (self.raw_coc [self.raw_coc.iloc [index]])
			#print "Type of COC extracted at index: ", type (self.raw_coc.iloc [index]), "\n\n"
			if index != -1 and index < self.raw_coc.shape [0]:
				current_coc = self.raw_coc.iloc [index].tolist ()#set (self.raw_coc.iloc [index])
			else:
				current_coc = list (np.repeat ("missing", len (self.raw_coc.columns)))
			print ("Shape of COC for extraction at index: ", index, " IS ", self.raw_coc.shape, "\n\n")
			print ("Extracted the data from COC at index: ", index, "\n\n")
			print ("Extracted COC at index: ", index, " === ", current_coc, "\n\n")
			
			'''
			current_jlc = list (np.repeat ("missing", len (self.raw_jlc.columns)))#(len (self.out_ccr.columns) - len (self.raw_jlc.columns))))
			#print "Type of JLC constructed at index: ", type (current_jlc), "\n\n"
			print "Shape of JLC for construction at index: ", index, " IS ", str (len (current_jlc)), "\n\n"
			print "Constructed missing data for JLC at index: ", index, "\n\n"
			print "Constructed JLC at index: ", index, " === ", current_jlc, "\n\n"
			'''
			
			#Insert data into OUTPUT DF where ACS and JLC match, but ACS and COC do not
			#for index in self.matches_trueACSJLC:#match_indicesOnlyACSJLC:
			#for iterator_2 in range (0, len (self.matches_trueACSJLC_ACSIndices)):
			index = self.matches_trueACSCOC_ACSIndices [iterator_1]
			if index in self.matches_trueACSJLC_ACSIndices:
				
				#index = self.matches_trueACSJLC_ACSIndices [iterator_2]
				
				print ("Joining ACS and JLC on index: ", index, "\n\n")
				
				index = self.matches_trueACSJLC_JLCIndices [iterator_1]
				#current_jlc = set (self.raw_jlc [self.raw_jlc.iloc [index]])
				#print "Type of JLC extracted at index: ", type (self.raw_jlc.iloc [index]), "\n\n"
				print ("Extracting data for JLC at Index: ", index, "\n\n")
				print ("shape of JLC is: ", self.raw_jlc.shape, "\n\n")
				print ("shape of ACS is: ", self.raw_acs.shape, "\n\n")
				print ("shape of COC is: ", self.raw_coc.shape, "\n\n")
				if index != -1 and index < self.raw_jlc.shape [0]:
					current_jlc = self.raw_jlc.iloc [index].tolist ()#set (self.raw_jlc.iloc [index])
				else:
					current_jlc = list (np.repeat ("missing", len (self.raw_jlc.columns)))
				print ("Shape of JLC for extraction at index: ", index, " IS ", self.raw_jlc.shape, "\n\n")
				print ("Extracted the data from JLC at index: ", index, "\n\n")
				print ("Extracted JLC at index: ", index, " === ", current_jlc, "\n\n")
			
			else:
				current_jlc = list (np.repeat ("missing", len (self.raw_jlc.columns)))
				
			
			current_list = self.CombineContentsExtracted (current_acs, current_coc, current_jlc)#current_acs | current_coc | current_jlc
			print ("Current Set from combining the 3 at index: ", index, " === ", current_list, "\n\n")
			
			
			print ("Extracted the Data from ACS and COC at index: ", index, "\n\n")
			
			current_combinedict = self.CombineContentsDictionary (headers_combined, current_list)
			if current_combinedict [0] is True:
				current_dictionary = current_combinedict [1]#self.CombineContentsDictionary (headers_combined, current_list)
				#current_df = pd.DataFrame (data=current_list, columns=headers_combined)#, na=False)
				current_df = pd.DataFrame (current_dictionary, index=[0])#pd.DataFrame (current_dictionary, orient="columns", index=[0])#pd.DataFrame.from_dict (current_dictionary, orient="columns", index=[0])
				current_df = current_df [headers_combined]
				#current_df = pd.concat ([self.raw_acs [self.raw_acs.iloc [index]], self.raw_coc [self.raw_coc.iloc [index]], np.repeat (None, (self.out_ccr.shape [1] - self.raw_jlc.shape [1]))])
				
				print ("Constructed NEW Insertion Dataframe (single row) by combining data from ACS and COC Dataframes at index: ", index, "\n\n")
				
				print ("Headers for NEW Constructed INSERTION Dataframe: ", current_df.columns, "\n\n")
				print ("Headers for OUTPUT Dataframe: ", self.out_ccr.columns, "\n\n")
				self.out_ccr = self.out_ccr.append (current_df)
				
				print ("out_ccr Shape After Match ACS COC Insert: ", str (self.out_ccr.shape [0]), ", ", str (self.out_ccr.shape [1]))
				print ("\n\n\n\n")
		
		
		#Insert data into OUTPUT DF where ACS and JLC match, but ACS and COC do not
		#for index in self.matches_trueACSJLC:#match_indicesOnlyACSJLC:
		for iterator_2 in range (0, len (self.matches_trueACSJLC_ACSIndices)):
			
			index = self.matches_trueACSJLC_ACSIndices [iterator_2]
			
			if not (index in self.matches_trueACSCOC_ACSIndices):
				
				print ("Joining ACS and JLC on index: ", index, "\n\n")
				
				#current_acs = set (self.raw_acs [self.raw_acs.iloc [index]])
				#print "Type of ACS extracted at index: ", type (self.raw_acs.iloc [index]), "\n\n"
				if index != -1 and index < self.raw_acs.shape [0]:
					current_acs = self.raw_acs.iloc [index].tolist ()#set (self.raw_acs.iloc [index])
				else:
					current_acs = list (np.repeat ("missing", len (self.raw_acs.columns)))
				print ("Shape of ACS for extraction at index: ", index, " IS ", self.raw_acs.shape, "\n\n")
				print ("Extracted the data from ACS at index: ", index, "\n\n")
				print ("Extracted ACS at index: ", index, " === ", current_acs, "\n\n")
				
				current_coc = list (np.repeat ("missing", len (self.raw_coc.columns)))#(len (self.out_ccr.columns) - len (self.raw_coc.columns))))
				#print "Type of COC constructed at index: ", type (current_coc), "\n\n"
				print ("Shape of COC for construction at index: ", index, " IS ", str (len (current_coc)), "\n\n")
				print ("Constructed missing data for COC at index: ", index, "\n\n")
				print ("Constructed COC at index: ", index, " === ", current_coc, "\n\n")
				
				index = self.matches_trueACSJLC_JLCIndices [iterator_2]
				#current_jlc = set (self.raw_jlc [self.raw_jlc.iloc [index]])
				#print "Type of JLC extracted at index: ", type (self.raw_jlc.iloc [index]), "\n\n"
				print ("Extracting data for JLC at Index: ", index, "\n\n")
				print ("shape of JLC is: ", self.raw_jlc.shape, "\n\n")
				print ("shape of ACS is: ", self.raw_acs.shape, "\n\n")
				print ("shape of COC is: ", self.raw_coc.shape, "\n\n")
				if index != -1 and index < self.raw_jlc.shape [0]:
					current_jlc = self.raw_jlc.iloc [index].tolist ()#set (self.raw_jlc.iloc [index])
				else:
					current_jlc = list (np.repeat ("missing", len (self.raw_jlc.columns)))
				print ("Shape of JLC for extraction at index: ", index, " IS ", self.raw_jlc.shape, "\n\n")
				print ("Extracted the data from JLC at index: ", index, "\n\n")
				print ("Extracted JLC at index: ", index, " === ", current_jlc, "\n\n")
				
				current_list = self.CombineContentsExtracted (current_acs, current_coc, current_jlc)#current_acs | current_coc | current_jlc
				print ("Current Set from combining the 3 at index: ", index, " === ", current_list, "\n\n")
				
				print ("Extracted the Data from ACS and JLC at index: ", index, "\n\n")
				
				current_combinedict = self.CombineContentsDictionary (headers_combined, current_list)
				if current_combinedict [0] is True:
					current_dictionary = current_combinedict [1]#self.CombineContentsDictionary (headers_combined, current_list)
					#current_df = pd.DataFrame (data=current_list, columns=headers_combined)#, na=False)
					current_df = pd.DataFrame (current_dictionary, index=[0])#pd.DataFrame (current_dictionary, orient="columns", index=[0])#pd.DataFrame.from_dict (current_dictionary, orient="columns", index=[0])
					current_df = current_df [headers_combined]
					#current_df = pd.concat ([self.raw_acs [self.raw_acs.iloc [index]], np.repeat (None, (self.out_ccr.shape [1] - self.raw_coc.shape [1])), self.raw_jlc [self.raw_jlc.iloc [index]]])
					
					print ("Constructed NEW Insertion Dataframe (single row) by combining data from ACS and JLC Dataframes at index: ", index, "\n\n")
					
					print ("Headers for NEW Constructed INSERTION Dataframe: ", current_df.columns, "\n\n")
					print ("Headers for OUTPUT Dataframe: ", self.out_ccr.columns, "\n\n")
					self.out_ccr = self.out_ccr.append (current_df)
					
					print ("out_ccr Shape After Match ACS JLC Insert: ", str (self.out_ccr.shape [0]), ", ", str (self.out_ccr.shape [1]))
					print ("\n\n\n\n")
			
			else:
				
				continue
			
				
		#Insert data into OUTPUT DF where ACS doesn't match either JLC or COC
		for index in self.matches_onlyACS:#match_indicesOnlyACS:
			
			if index < self.raw_acs.shape [0]:
				current_acs = self.raw_acs.iloc [index].tolist ()
				
				current_coc = list (np.repeat ("missing", len (self.raw_coc.columns)))
				
				current_jlc = list (np.repeat ("missing", len (self.raw_jlc.columns)))
				
				current_list = self.CombineContentsExtracted (current_acs, current_coc, current_jlc)
				
				current_combinedict = self.CombineContentsDictionary (headers_combined, current_list)
				
				if current_combinedict [0] is True:
					
					current_dictionary = current_combinedict [1]
					
					current_df = pd.DataFrame (current_dictionary, index=[0])
					
					current_df = current_df [headers_combined]
					
					self.out_ccr = self.out_ccr.append (current_df)
		
		#Insert data into OUTPUT DF where COC doesn't match either ACS or JLC
		for index in self.matches_onlyCOC:#match_indicesOnlyCOC:
			
			if index < self.raw_coc.shape [0]:
				current_acs = list (np.repeat ("missing", len (self.raw_acs.columns)))
				
				current_coc = self.raw_coc.iloc [index].tolist ()
				
				current_jlc = list (np.repeat ("missing", len (self.raw_jlc.columns)))
				
				current_list = self.CombineContentsExtracted (current_acs, current_coc, current_jlc)
				
				current_combinedict = self.CombineContentsDictionary (headers_combined, current_list)
				
				if current_combinedict [0] is True:
					
					current_dictionary = current_combinedict [1]
					
					current_df = pd.DataFrame (current_dictionary, index=[0])
					
					current_df = current_df [headers_combined]
					
					self.out_ccr = self.out_ccr.append (current_df)
		
		#Insert data into OUTPUT DF where JLC doesn't mathc either ACS or COC
		#print "Item in ACS at index 25160 = ", self.raw_acs.iloc [25160].tolist (), "\n\n"
		for index in self.matches_onlyJLC:#match_indicesOnlyJLC:
			
			if index < self.raw_jlc.shape [0]:
				current_acs = list (np.repeat ("missing", len (self.raw_acs.columns)))
				
				current_coc = list (np.repeat ("missing", len (self.raw_coc.columns)))
				
				print ("Current JLC Only Index: ", index, "\n\n")
				
				current_jlc = self.raw_jlc.iloc [index].tolist ()
				
				current_list = self.CombineContentsExtracted (current_acs, current_coc, current_jlc)
				
				current_combinedict = self.CombineContentsDictionary (headers_combined, current_list)
				
				if current_combinedict [0] is True:
					
					current_dictionary = current_combinedict [1]
					
					current_df = pd.DataFrame (current_dictionary, index=[0])
					
					current_df = current_df [headers_combined]
					
					self.out_ccr = self.out_ccr.append (current_df)
		
		
		self.out_ccr.to_csv (os.getcwd () + "outputAllCombined_" + dt.datetime.now ().strftime ("%Y-%m-%d_%H-%M-%S") + "_.csv")
		
		
		print ("Count of Unique ACS CompLotNum", len (self.out_ccr ["CompLotNum"].unique ()), "\n\n")
		print ("Count of RAW Unique ACS CompLotNum", len (self.raw_acs ["CompLotNum"].unique ()), "\n\n")
		
		print ("Count of Unique ACS Lot Num", len (self.out_ccr ["LotNum"].unique ()), "\n\n")
		print ("Count of RAW Unique ACS Lot Num", len (self.raw_acs ["LotNum"].unique ()), "\n\n")
		
		print ("Count of Unique COC Batch", len (self.out_ccr ["Batch"].unique ()), "\n\n")
		print ("Count of RAW Unique COC Batch", len (self.raw_coc ["Batch"].unique ()), "\n\n")
		
		print ("Count of Unique JLC SFG Lot", len (self.out_ccr ["SFG Lot"].unique ()), "\n\n")
		print ("Count of RAW Unique JLC SFG Lot", len (self.raw_jlc ["SFG Lot"].unique ()), "\n\n")
		
		
		#Insert data into OUTPUT DF where ACS doesn't match either COC nore JLC
		
		#Insert data into OUTPUT DF where COC doesn't match ACS
		
		#Insert data into OUTPUT DF where JLC doesn't match ACS
		'''
		df1 = df1.merge (df2, left_on="CompLotNum", right_on="Batch", how="outer")
		df1 = df1.merge (df3, left_on="LotNum", right_on="SFG Lot", how="outer")
		#self.out_ccr.columns = headers_combined
		
		self.out_ccr = df1
	
		for match in matches_trueall:
			
			pass
		'''
	
	#Combine the elements extracted from each of the 3 RAW Dataframes at the current index
	def CombineContentsExtracted (self, list_1, list_2, list_3):
		
		combined_extracted = []
		
		for item in list_1:
			
			combined_extracted.append (item)
		
		for item in list_2:
			
			combined_extracted.append (item)
		
		for item in list_3:
			
			combined_extracted.append (item)
		
		return combined_extracted



	#Combines the headers from the 3 different RAW DFs into a single list of headers
	def CombineHeadersDataframes (self):
		'''
		headers_acs = set (self.raw_acs.columns)
		headers_coc = set (self.raw_coc.columns)
		headers_jlc = set (self.raw_jlc.columns)
		
		#Join the seperate SETs into a single set
		headers_combined = headers_acs | headers_coc | headers_jlc
		#headers_combined = list (headers_combined)
		'''
		
		headers_combined = []
		
		for header in self.raw_acs.columns:
			
			headers_combined.append (header)
		
		for header in self.raw_coc.columns:
			
			headers_combined.append (header)
		
		for header in self.raw_jlc.columns:
			
			headers_combined.append (header)
		
		#print "What is NOT in headers_combined is: ", (((headers_combined - headers_acs) - headers_coc) - headers_jlc), "\n\n"
		#headers_combined = list (headers_combined)
		
		return headers_combined
	
	
	
	#Convert the COMBINED data extracted from the 3 RAW DF's into a dictionary so that it can be converted into a new DF that can be appended to the OUTPUT DF
	def CombineContentsDictionary (self, list_headers, list_combined):
		current_lenmatch = False
		current_dictionary = {}
		
		index = 0
		
		print ("In CombineContentsDictionary, and LENGTH of Combined Headers = ", len (list_headers), " and LENGTH of Combined Values = ", len (list_combined), "\n\n")
		
		if len (list_headers) == len (list_combined):
			
			current_lenmatch = True
			
			while index < len (list_headers):
				
				current_dictionary [list_headers [index]] = list_combined [index]
				
				index += 1
			
		
		return (current_lenmatch, current_dictionary)
		
		
	
	
	#Take in Dataframe Identifiers and return a list of matching elements for those dataframes
	def MatchElementsDataframes (self):#, df1, df2):
		
		'''
		matches_trueACSCOC = None
		matches_trueACSJLC = None
		matches_trueALL = None
		matches_onlyACS = None
		matches_onlyCOC = None
		matches_onlyJLC = None
		'''
		indices_ACS_ACSCOC = None
		indices_ACS_ACSJLC = None
		
		indices_COC_ACSCOC = None
		indices_COC_ALLCOC = None
		
		indices_JLC_ACSJLC = None
		indices_JLC_ALLJLC = None
		
		try:
			#matches_trueACSCOC = np.intersect1d (self.raw_acs ["CompLotNum"].str.lower (), self.raw_coc ["Batch"].str.lower (), assume_unique=True, return_indices=True)
			self.matches_trueACSCOC = np.intersect1d (self.raw_acs ["CompLotNum"].str.lower (), self.raw_coc ["Batch"].str.lower (), assume_unique=False, return_indices=True)
		except Exception as e:
			print ("Matching TOTAL ACS and COC exception: ", e.message, "\n\n")
		
		try:
			#matches_trueACSJLC = np.intersect1d (self.raw_acs ["Lot Num"].str.lower (), self.raw_jlc ["SFG Lot"].str.lower (), assume_unique=True, return_indices=True)
			self.matches_trueACSJLC = np.intersect1d (self.raw_acs ["LotNum"].str.lower (), self.raw_jlc ["SFG Lot"].str.lower (), assume_unique=False, return_indices=True)
		except Exception as e:
			print ("Matching TOTAL ACS and JLC exception: ", e.message, "\n\n")
			
		try:
			#matches_trueALL = np.intersect1d (matches_trueACSCOC [0], matches_trueACSJLC [0], assume_unique=True, return_indices=True)
			self.matches_trueALL = np.intersect1d (self.matches_trueACSCOC [0], self.matches_trueACSJLC [0], assume_unique=True, return_indices=True)
			#self.matches_trueALLIndices = reduce (np.intersect1d (self.matches_trueACSCOC [1], self.matches_trueACSCOC [2], self.matches_trueACSJLC [1], self.matches_trueACSJLC [2], assume_unique=True, return_indices=True))
			self.matches_trueALLIndices = set (self.matches_trueACSCOC [1]) & set (self.matches_trueACSCOC [2]) & set (self.matches_trueACSJLC [1]) & set (self.matches_trueACSJLC [2])
			print ("Finished Identifying True ALL Indices: ", self.matches_trueALLIndices, "\n\n")
		except Exception as e:
			print ("Matching ALL ACS, COC, and JLC exception: ", e.message, "\n\n")
		
		'''
		print "trueACSCOC matches: ", self.matches_trueACSCOC, "\n\n\n\n"
		
		print "trueACSJLC matches: ", self.matches_trueACSJLC, "\n\n\n\n"
		
		print "true ALL matches: ", self.matches_trueALL, "\n\n"
		'''
		
		try:
			#matches_onlyACS = set (self.raw_acs.index.get_values ()) - matches_trueACSCOC - matches_trueACSJLC - set (matches_trueALL [1].tolist ())
			self.matches_onlyACS = set (self.raw_acs.index.get_values ()) - set (self.matches_trueACSCOC [1].tolist ()) - set (self.matches_trueACSJLC [1].tolist ())
			print ("ONLY ACS Indices: ", self.matches_onlyACS, "\n\n")
		except Exception as e:
			print ("ONLY ACS exception: ", e.message, "\n\n")
			
		try:
			#matches_onlyCOC = set (self.raw_coc.index.get_values ()) - matches_trueACSCOC - set (matches_trueALL [1].tolist ())
			self.matches_onlyCOC = set (self.raw_coc.index.get_values ()) - set (self.matches_trueACSCOC [1].tolist ())
			print ("Only COC Indices: ", self.matches_onlyCOC, "\n\n")
		except Exception as e:
			print ("ONLY COC exception: ", e.message, "\n\n")
			
		try:
			#matches_onlyJLC = set (self.raw_jlc.index.get_values ()) - matches_trueACSJLC - set (matches_trueALL [1].tolist ())
			self.matches_onlyJLC = set (self.raw_jlc.index.get_values ()) - set (self.matches_trueACSJLC [1].tolist ())
			#print "Self Raw JLC get_values: ", set (self.raw_jlc.index.get_values ()), "\n\n"
			#print "Self Matches ACSJLC [1]: ", set (self.matches_trueACSJLC.index.get_values ()), "\n\n"
			#print "Only JLC Indices: ", self.matches_onlyJLC, "\n\n"
		except Exception as e:
			print ("ONLY JLC excepton: ", e.message, "\n\n")
			
		
		
		
		
		try:
			#matches_trueACSCOC = set (matches_trueACSCOC [0].tolist ()) - set (matches_trueALL [1].tolist ())
			self.matches_trueACSCOC = set (self.matches_trueACSCOC [0].tolist ()) - set (self.matches_trueALL [0].tolist ())
			print ("ACS COC Indices: ", self.matches_trueACSCOC, "\n\n")
		except Exception as e:
			print ("Matching REDUCED ACS and COC exception: ", e.message, "\n\n")
			
		try:
			#matches_trueACSJLC = set (matches_trueACSJLC [0].tolist ()) - set (matches_trueALL [1].tolist ())
			self.matches_trueACSJLC = set (self.matches_trueACSJLC [0].tolist ()) - set (self.matches_trueALL [0].tolist ())
			print ("ACS JLC Indices: ", self.matches_trueACSJLC, "\n\n")
		except Exception as e:
			print ("Matching REDUCED ACS and JLC exception: ", e.message, "\n\n")
		
		
		
		
		'''
		#Identify locations where DF1 and DF2 match for combining
		matches_true1 = None
		
		matches_false2 = None
		matches_false3 = None
		
		if df1 == "ACS" and df2 == "COC":
			
			matches_true1 = np.intersect1d (self.raw_acs ["CompLotNum"].str.lower (), self.raw_coc ["Batch"].str.lower (), assume_unique=False, return_indices=True)
			matches_true1 = set (pd.Series (matches_true1 [0]).tolist ())
			
			matches_false2 = set (self.raw_acs ["CompLotNum"].tolist ()) - matches_true1
			matches_false3 = set (self.raw_coc ["Batch"].tolist ()) - matches_true1
		
		elif df1 == "ACS" and df2 == "JLC":
			
			matches_true1 = np.intersect1d (self.raw_acs ["LotNum"].str.lower (), self.raw_jlc ["SFG Lot"].str.lower (), assume_unique=False, return_indices=True)
			matches_true1 = set (pd.Series (matches_true1 [0]).tolist ())
			
			matches_false2 = set (self.raw_acs ["LotNum"].tolist ()) - matches_true1
			matches_false3 = set (self.raw_jlc ["SFG Lot"].tolist ()) - matches_true1
			
		else:
			
			pass
		
		return matches_true1, matches_false2, matches_false3
		'''
	def MatchElementsIndices (self):
		#Now obtain index values from the appropriate Dataframes for the common elements in matches_trueALL, matches_trueACSCOC, and matches_trueACSJLC
		
		
		for item in self.matches_trueACSCOC:
			
			indices1 = self.raw_acs [self.raw_acs ["CompLotNum"].str.lower () == str (item).lower ()].index.get_values ().tolist ()
			#indices1 = list (indices1)
			indices2 = self.raw_coc [self.raw_coc ["Batch"].str.lower () == str (item).lower ()].index.get_values ().tolist ()
			#indices2 = list (indices2)
			
			'''
			print "Extracted ACCESS Indices for ACSJLC: ", indices1, "\n\n"
			print "TYPE of ACCESS Indices: ", type (indices1), "\n\n"
			print "Extracted JOBLOTCOMP Indices for ACSJLC: ", indices2, "\n\n"
			print "TYPE of JOBLOTCOMP Indices: ", type (indices2), "\n\n"
			'''
			
			
			if len (indices1) > len (indices2):
				count = len (indices2)
				
				while count < len(indices1):
					indices2.append (-1)
				
					count += 1
			
			elif len (indices1) < len (indices2):
				count = len (indices1)
				
				while count < len (indices2):
					indices1.append (-1)
					
					count += 1
			
			else:
				pass
				
				
			
			for index in indices1:
				self.matches_trueACSCOC_ACSIndices.append (index)
			
			
			for index in indices2:
				self.matches_trueACSCOC_COCIndices.append (index)
				
				
		
		for item in self.matches_trueACSJLC:
			
			indices1 = self.raw_acs [self.raw_acs ["LotNum"].str.lower () == str (item).lower ()].index.get_values ().tolist ()
			#indices1 = list (indices1)
			indices2 = self.raw_jlc [self.raw_jlc ["SFG Lot"].str.lower () == str (item).lower ()].index.get_values ().tolist ()
			#indices2 = list (indices2)
			
			'''
			print "Extracted ACCESS Indices for ACSJLC: ", indices1, "\n\n"
			print "TYPE of ACCESS Indices: ", type (indices1), "\n\n"
			print "Extracted JOBLOTCOMP Indices for ACSJLC: ", indices2, "\n\n"
			print "TYPE of JOBLOTCOMP Indices: ", type (indices2), "\n\n"
			'''
			
			
			if len (indices1) > len (indices2):
				count = len (indices2)
				
				while count < len(indices1):
					indices2.append (-1)
				
					count += 1
			
			elif len (indices1) < len (indices2):
				count = len (indices1)
				
				while count < len (indices2):
					indices1.append (-1)
				
					count += 1
			
			else:
				pass
			
			for index in indices1:
				self.matches_trueACSJLC_ACSIndices.append (index)
			
			
			for index in indices2:
				self.matches_trueACSJLC_JLCIndices.append (index)
			
		
		#return False
		
	#Take in a list of elements for either COC or JLC and return the indices of those elements (these indices are where COC or JLC don't match any other DF)
	def MatchIndicesFalse (self, match_false, df):
		
		match_indicesfalse = []
		
		match_indicesfalseinit = []
		
		for element in match_false:
			if df == "COC":
				
				match_indicesfalseinit = self.raw_coc [self.raw_coc ["Batch"].str.lower () == str (element).lower ()].index
				
			elif df == "JLC":
					
				match_indicesfalseinit = self.raw_jlc [self.raw_jlc ["SFG Lot"].str.lower () == str(element).lower ()].index
			
			for index in match_indicesfalseinit:
				
				match_indicesfalse.append (index)
		
		return match_indicesfalse
	
	
	
	#Take in a list of matching elements for 2 dataframes, return a list of indices where each element occurs in each dataframe
	def MatchIndicesDataframes (self, match_elements, df1, df2):
		
		match_indices1 = []
		match_indices2 = []
		
		for element in match_elements:
			
			match_indicesInit1 = []
			match_indicesInit2 = []
			
			if df1 == "ACS" and df2 == "COC":
				
				match_indicesInit1 = self.raw_acs [self.raw_acs ["CompLotNum"].str.lower () == str (element).lower ()].index
				match_indicesInit2 = self.raw_coc [self.raw_coc ["Batch"].str.lower () == str (element).lower ()].index
				
			
			elif df1 == "ACS" and df2 == "JLC":
				
				match_indicesInit1 = self.raw_acs [self.raw_acs ["LotNum"].str.lower () == str (element).lower ()].index
				match_indicesInit2 = self.raw_jlc [self.raw_jlc ["SFG Lot"].str.lower () == str (element).lower ()].index
			
			else:
				
				pass
				
		
			for index in match_indicesInit1:
				
				match_indices1.append (index)
				
				#print ("Appended " + str (index) + "\n\n")
			
			for index in match_indicesInit2:
				
				match_indices2.append (index)
				
				#print ("Appended " + str (index) + "\n\n")

		return match_indices1, match_indices2
	
	
	
	
	#Take in 2 sets of indices, "ab" is the set of matching indices for ACS and COC, "bc" is the set of matching indices for ACS and JLC
	#Return 3 sets "match_all" is set of indices where ALL 3 dataframes match, "match_ab" is set of indices where ACS matches ONLY COC, "match_bc" is set of indices where ACS matches ONLY JLC
	def MatchAllDataframes (self, match_indicesab1, match_indicesab2, match_indicesbc1, match_indicesbc2):
		
		match_indicesab1 = set (match_indicesab1)
		match_indicesab2 = set (match_indicesab2)
		match_indicesbc1 = set (match_indicesbc1)
		match_indicesbc2 = set (match_indicesbc2)
		
		#Identify indices where ACS, COC, and JLC all match
		match_list = [match_indicesab1, match_indicesab2, match_indicesbc1, match_indicesbc2]
		
		match_indicesall = set.intersection (*match_list)
		
		#Identify potential indices where only ACS and COC match
		match_indicesab1 = match_indicesab1 - match_indicesall
		match_indicesab2 = match_indicesab2 - match_indicesall
		
		#Identify indices where ACS and COC match
		match_listab = [match_indicesab1, match_indicesab2]
		
		match_indicesaball = set.intersection (*match_listab)
		
		#Identify indices where ACS and COC don't match
		match_indicesab1 = match_indicesab1 - match_indicesaball
		#match_indicesab2 = match_indicesab2 - match_indicesaball
		
		#Identify potential indices where only ACS and JLC match
		match_indicesbc1 = match_indicesbc1 - match_indicesall
		match_indicesbc2 = match_indicesbc2 - match_indicesall
		
		#Identify indices where ACS and JLC match
		match_listbc = [match_indicesbc1, match_indicesbc2]
		
		match_indicesbcall = set.intersection (*match_listbc)
		
		#Identify indices where ACS and JLC don't match
		match_indicesbc1 = match_indicesbc1 - match_indicesbcall
		#match_indicesbc2 = match_indicesbc2 - match_indicesbcall
		
		
		#Identify indices where ACS doesn't match either COC or JLC
		match_listacs = [match_indicesab1, match_indicesbc1]
		
		match_indicesacs = set.intersection (*match_listacs)
		
		return match_indicesall, match_indicesaball, match_indicesbcall, match_indicesacs





if __name__ == "__main__":
	
	reconciler = CarbideComponentReconciler ()
	reconciler.PrepareRawDataframes ()
	reconciler.PrintCurrentDataframes ()
	reconciler.ExpandDimensionsDataframes (reconciler.GetCurrentDataframe ("ACS"), "ACS", reconciler.GetCurrentDataframe ("COC"), "COC")
	reconciler.ExpandDimensionsDataframes (reconciler.GetCurrentDataframe ("ACS"), "ACS", reconciler.GetCurrentDataframe ("JLC"), "JLC")
	reconciler.ExpandDimensionsDataframes (reconciler.GetCurrentDataframe ("COC"), "COC", reconciler.GetCurrentDataframe ("JLC"), "JLC")
	#reconciler.PrintCurrentDataframes ()
	
	
	#reconciler.CombineContentsDataframes (reconciler.GetCurrentDataframe ("ACS"), reconciler.GetCurrentDataframe ("COC"), reconciler.GetCurrentDataframe ("JLC"))
	#match_trueACSCOC, match_false2ACSCOC, match_false3ACSCOC = reconciler.MatchElementsDataframes ("ACS", "COC")
	#match_trueACSJLC, match_false2ACSJLC, match_false3ACSJLC = reconciler.MatchElementsDataframes ("ACS", "JLC")
	#match_indicesALL, match_indicesACSCOC, match_indicesACSJLC, match_indicesACS, match_indicesCOC, match_indicesJLC = reconciler.MatchElementsDataframes ()
	#reconciler.MatchElementsDataframes ()
	
	#Get indices where COC matches nothing and where JLC matches nothing
	#match_indicesOnlyCOC = reconciler.MatchIndicesFalse (match_false3ACSCOC, "COC")
	#match_indicesOnlyJLC = reconciler.MatchIndicesFalse (match_false3ACSJLC, "JLC")
	
	#Now obtain index values from the appropriate Dataframes for the common elements in matches_trueALL, matches_trueACSCOC, and matches_trueACSJLC
	#reconciler.MatchElementsIndices ()
	'''
	print ("Matched Elements ACS COC: ", match_trueACSCOC)
	print ("\n\n\n\n")
	print ("Matched Elements ACS JLC: ", match_trueACSJLC)
	print ("\n\n\n\n")
	'''
	
	#match_indicesACSCOC1, match_indicesACSCOC2 = reconciler.MatchIndicesDataframes (match_trueACSCOC, "ACS", "COC")
	#match_indicesACSJLC1, match_indicesACSJLC2 = reconciler.MatchIndicesDataframes (match_trueACSJLC, "ACS", "JLC")
	
	'''
	print ("Matched Indices ACS COC for ACS: ", match_indicesACSCOC1)
	print ("\n\n\n\n")
	print ("Matched Indices ACS COC for COC: ", match_indicesACSCOC2)
	print ("\n\n\n\n")
	'''
	
	'''
	print ("Matched Indices ACS JLC for ACS: ", match_indicesACSJLC1)
	print ("\n\n\n\n")
	print ("Matched Indices ACS JLC for JLC: ", match_indicesACSJLC2)
	print ("\n\n\n\n")
	'''
	
	#match_indicesAll, match_indicesOnlyACSCOC, match_indicesOnlyACSJLC, match_indicesOnlyACS = reconciler.MatchAllDataframes (match_indicesACSCOC1, match_indicesACSCOC2, match_indicesACSJLC1, match_indicesACSJLC2)
	
	
	
	#reconciler.CombineContentsDataframes (match_indicesAll, match_indicesOnlyACSCOC, match_indicesOnlyACSJLC, match_indicesOnlyACS, match_indicesOnlyCOC, match_indicesOnlyJLC)
	#reconciler.CombineContentsDataframes ()
	'''
	print ("Indices for ALL Match: ", match_indicesAll)
	print ("\n\n\n\n")
	print ("Indices for ONLY ACS and COC: ", match_indicesOnlyACSCOC)
	print ("\n\n\n\n")
	print ("Indices for ONLY ACS and JLC: ", match_indicesOnlyACSJLC)
	'''
	
	#reconciler.PrintCurrentDataframes ()
	reconciler.MergeContentsDataframes ()
