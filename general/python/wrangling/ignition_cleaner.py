import pandas as pd
import numpy as np
import datetime as dt


#class ignition_cleaner (object):
	#def __init__ (self, filename)
	#def __del__ (self)
	#def insertConvertHour (self, item)
	#def insertConvertWeekday (self, item)
	#def insertConvertShift (self, item_1, item_2)
	#def insertColumnSplit (self, column, column_number)
	#def insertColumnConvert (self, subset, column_number, convert_type)
	#def insertColumnTime (self, column_name, column_number)
	#def insertColumnOther (self, column_name, column_number)
	#def insertColumnData (self, column_name, column_number)
	#def insertProcessBegin (self, )
	#def insertNewDF (self, )
	#def insertColumnCalculate (self)
	#def insertColumnQC (self)

#xls_ignition = pd.ExcelFile ("RunSummary 20180801_20180831.xls") #This name will need to be updated with the new Ignition file name

#data_raw_ignition = pd.read_excel (xls_ignition, "Dataset 1") #This is the name of the worksheet in the Ignition file
data_raw_ignition = pd.read_csv ("RunSummary 20180801_20180831.csv") #This name will need to be updated with the NEW Ignition file AFTER it has been saved in a ".csv" format
print data_raw_ignition.columns, "\n\n"

data_raw_ignition = data_raw_ignition [data_raw_ignition.columns] [data_raw_ignition ["CycleOutcome"] != "Invalid"]



dict_insert_ignition = {}



















#Convert "H:M:S" from the Timestamp into the encoded decimal Hour representation
def insertConvertHour (item):
    
    #=IF(HOUR(B2)<4,0.1,IF(HOUR(B2)<16,0.2,0.3))
    insert_convert_hour = None
    
    item_convert_hour = int (item.split (":") [0])
    
    if item_convert_hour < 4:
        
        insert_convert_hour = 0.1
        
    elif item_convert_hour < 16:
        
        insert_convert_hour = 0.2
        
    else:
        
        insert_convert_hour = 0.3
        
    return insert_convert_hour
	
	
	
	

#Convert "Y-M-D" string into the matching (full name) Weekday equivalent	
def insertConvertWeekday (item):

	insert_convert_weekday = None
	
	item_convert_list = item.split ("-")
	
	#This will convert the inputted "Y-M-D" string into a date object 
	insert_convert_weekday = dt.date (int (item_convert_list [0]), int (item_convert_list [1]), int (item_convert_list [2].split (" ") [0]))
	
	#This converts the above converted Date object into its Day of the Week (full name) equivalent and returns that to the calling function for matching the name with the correct number representation
	return insert_convert_weekday.strftime ("%A")





#Convert the EARLIER computed Weekday and Time values into Shift values
def insertConvertShift (item_1, item_2):
     #F is "Weekday" and G is "Time"; therefore, subset_1 = "Weekday", subset_2 = "Time"
                
    insert_convert_shift = None

    #=IF(AND(F2>0,F2<4,G2=0.2),"A"
    if item_1 > 0 and item_1 < 4 and item_2 == 0.2:

        insert_convert_shift = "A"

    #,IF(OR(AND(F2>0,F2<4,OR(G2=0.1,G2=0.3)*(F2+G2<>1.1)),(F2+G2)=4.1),"B"
    elif item_1 > 0 and item_1 < 4 and ((item_2 == 0.1 or item_2 == 0.3)*(item_1 + item_2) != 1.1) and (item_1 + item_2 == 4.1):  

        insert_convert_shift = "B"

    #,IF(AND(F2>3,F2<7,G2=0.2),"C"
    elif (item_1 > 3) and (item_1 < 7) and (item_2 == 0.2):

        insert_convert_shift = "C"
    #,IF(OR(AND(F2>3,F2<7,OR(G2=0.1,G2=0.3)*(F2+G2<>4.1)),(F2+G2)=7.1),"D"    
    elif ((item_1 > 3) and (item_1 < 7) and ((item_2 == 0.1 or item_2 == 0.3) * (item_1 + item_2) != 4.1)) or (item_1 + item_2 == 7.1):

        insert_convert_shift = "D"

    #,"Sunday"))))
    else:

        insert_convert_shift = "Sunday"
    
    return insert_convert_shift





#Splits submitted Timestamp into Month, Day, and Year columns
def insertColumnSplit (column, column_number):
    
    insert_current_list = []
    
    insert_current_series = None
    
    for item in column:
        
        if column_number < 3:
            #Split the Date portion of Timestamp and retain the desired column from splitting the Date
            insert_current_list.append (item.split (" ") [0].split ("-") [column_number])
			#print item.split (" ") [0].split ("-") [column_number], "\n"

    insert_current_series = pd.Series (insert_current_list)
    #print insert_current_series.head (), "\n\n"
    return insert_current_series





#Performs computations to convert submitted information into appropriate output
def insertColumnConvert (subset, column_number, convert_type):
	
	insert_current_list = []
	
	insert_current_series = None
	
	#Converts submitted portions of data into TIME related output (TIME of DAY of RUN, WEEKDAY, and SHIFT)
	if convert_type == "time":
		
		#If submitted Column Number = 3 (from dict_insert_columns), then current conversion is TIME of Day of RUN (decimal representation)
		if column_number == 3:
			
			for item in subset:
				
                #Split the Time portion of Timestamp and retain the desired column from splitting the Time
				insert_current_list.append (insertConvertHour (item.split (" ") [1].split (" ") [0]))
				
		#If submitted Column Number = 4 (from dict_insert_columns), then current conversion is WEEKDAY
        #Convert date portion of Timestamp to Weekday
		elif column_number == 4:
			
			#Match each computed weekday with its integer representation as dictated by the "2" Return Type in the Excel equivalent of this computation
			dict_weekday_value = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7}
			#print "In insertColumnConvert and prepping to convert Date to Weekday!", subset, "\n\n\n\n"
			for item in subset:
				
				insert_current_list.append (dict_weekday_value [insertConvertWeekday (item)])#dt.datetime.weekday (dt.date (item.split (" ") [0])))#str (item.split (" ") [0]))#		
				
		#If submitted Column Number = 5 (from dict_insert_columns), then current conversion is SHIFT
		#Convert Timestamp to Shift using the formula from Excel spreadsheet for Ignition data
		else:
			
			subset_1 = subset [0].tolist ()
			subset_2 = subset [1].tolist ()
			
			row = 0
			
			while row < len (subset_1):
				
				insert_current_list.append (insertConvertShift (subset_1 [row], subset_2 [row]))
				
				row += 1
				
				#F is "Weekday" and G is "Time"; therefore, subset_1 = "Weekday", subset_2 = "Time"
				
				#insert_current_shift = None
				
				##=IF(AND(F2>0,F2<4,G2=0.2),"A"
				#if subset_1 [row] > 0 and subset_1 [row] < 4 and subset_2 [row] == 0.2:
					
				#    insert_current_shift = "A"
				
				##,IF(OR(AND(F2>0,F2<4,OR(G2=0.1,G2=0.3)*(F2+G2<>1.1)),(F2+G2)=4.1),"B"
				#elif (subset_1 [row] > 0 and subset_1 [row] < 4 and ((subset_2 [row] == 0.1 or subset_2 [row] == 0.3)*(subset_1 [row] + subset_2 [row]) != 1.1) and (subset_1 [row] + subset_2 [row] == 4.1)):  
					
				#    insert_current_shift = "B"
				
				##,IF(AND(F2>3,F2<7,G2=0.2),"C"
				#elif (subset_1 [row] > 3) and (subset_1 [row] < 7) and (subset_2 [row] == 0.2):
					
				#    insert_current_shift = "C"
				##,IF(OR(AND(F2>3,F2<7,OR(G2=0.1,G2=0.3)*(F2+G2<>4.1)),(F2+G2)=7.1),"D"    
				#elif ((subset_1 [row] > 3) and (subset_1 [row] < 7) and ((subset_2 [row] == 0.1 or subset_2 [row] == 0.3) * (subset_1 [row] + subset_2 [row]) != 4.1)) or (subset_1 [row] + subset_2 [row] == 7.1):
					
				#    insert_current_shift = "D"
				
				##,"Sunday"))))
				#else:
					
				#    insert_current_shift = "Sunday"
					
				#insert_current_list.append (insert_current_shift)

	#Converts submitted portions of data into RESISTANCE
	#Convert Voltage and Amps to "Resistance" (Voltage/Amps)
	elif convert_type == "resistance":
		
		subset_1 = subset [0]
		subset_2 = subset [1]
		
		row = 0
		
		while row < len (subset_1):
			
			if subset_2 [row] != 0:
				
				insert_current_list.append (float (subset_1 [row] / subset_2 [row]))
				
			else:
			
				insert_current_list.append (None)
			
			row += 1
        
    
	
	
	#Converts submitted portions of data into PowerOffsetEnd - PowerOffsetStart
	#Convert PowerOffsetStart and PowerOffsetEnd to "Offset End - Start" (PowerOffsetEnd - PowerOffsetStart)
	else:
		
		subset_1 = subset [0]
		subset_2 = subset [1]
		
		row = 0
		
		while row < len (subset_1):
		
			insert_current_list.append (float (subset_2 [row] - subset_1 [row]))
			
			row += 1
			
	insert_current_series = pd.Series (insert_current_list)
	
	return insert_current_series




#Arrange the processing of Date and Time related data
def insertColumnTime (column_name, column_number):
    
    insert_date_list = ["Year", "Month", "Day"]
    
    insert_current_result = None
    
	#If the Column Number < 3 (from dict_insert_columns), then current processing is extracting portions of the RUN START TIME (so that portion of data needs to be split appropriately)
    if column_number < 3:
        
        insert_current_result = insertColumnSplit (data_raw_ignition ["RunStartTime"].tolist (), column_number)
        
    else:
        
		#If the Column Number >= 3 AND Column Number < 5 (from dict_insert_columns), then it must be 4, and so current processing is CONVERTING the RUN START TIME to a decimal representation of the TIME of Day for the RUN
        if column_number < 5:
        
            insert_current_result = insertColumnConvert (data_raw_ignition ["RunStartTime"].tolist (), column_number, "time")
        
		#If the Column Number = 5 (from dict_insert_columns), then current processing is calculating the SHIFT (this requires the previously calculated WEEKDAY and the previously calculated TIME of DAY for the RUN)
        else:
            
            insert_current_result = insertColumnConvert ((dict_insert_ignition ["Weekday"], dict_insert_ignition ["Time"]), column_number, "time")
    
    return insert_current_result




#Arrange the processing of Other data (Resistance and PowerOffsetEnd - PowerOffsetStart)
def insertColumnOther (column_name, column_number):
    
    insert_current_result = None
    
	#If the Column Name is Resistance, submit the portions of data that will be needed for computing Resistance
    if column_name == "Resistance":
        
        insert_current_result = insertColumnConvert ((data_raw_ignition ["Voltage"].tolist (), data_raw_ignition ["Amps"].tolist ()), column_number, "resistance")
    
	#Otherwise, submit the portions of data that will be needed for computing PowerOffsetEnd - PowerOffsetStart
    else:
        
        insert_current_result = insertColumnConvert ((data_raw_ignition ["PowerOffsetStart"].tolist (), data_raw_ignition ["PowerOffsetEnd"].tolist ()), column_number, "end-start")
        
    return insert_current_result
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
#This breaks up the the Processing so that it focuses (1) on Time related data and (2) on Other kind of data
insert_time_list = ["Year", "Month", "Day", "Weekday", "Time", "Shift"]

insert_other_list = ["Resistance", "End-Start"]

#Differentiate between Date and Time related data in order to arrange the correct processing approach
def insertColumnData (column_name, column_number):
    
    insert_current_result = None
    
    if column_name in insert_time_list:
        
        insert_current_result = insertColumnTime (column_name, column_number) #Pass in which column the current Start time portion should match when the Start time is split
        
    else:
        
        insert_current_result =  insertColumnOther (column_name, column_number)
        
    return insert_current_result
    
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
#This is where the Processing begins
#This is the insertBeginProcess function	
	
#New columns that need to be computed for Ignition raw dataset: Year, Month, Day, Weekday, Time, Shift, Resistance, End - Start
list_insert_columns = ["PressID", "RunStartTime", "Year", "Month", "Day", "Weekday", "Time", "Shift",
                        "RunEndTime", "Recipe", "Lot", "OperatorID", "CycleOutcome", "AbortName", "RunType", "RunLength", 
                        "TimeBetwRuns", "PressurePV", "PressureCalc", "Voltage", "Amps", "PowerTrue", "Resistance", 
                        "PowerOffsetStart", "PowerOffsetEnd", "TempAtTC", "CubeLotNum", "HeaterLotNum", "End-Start"]

dict_insert_columns = {"Year":0,"Month":1,"Day":2,"Weekday":4,"Time":3,"Shift":5,"Resistance":None,"End-Start":None}

#This actually gets declared up at the very beginning so that it can be referenced for converting Weekday and Time into Shift,
#in the function calls insertConvertTime -> insertConvertShift
#dict_insert_ignition = {}


#Differentiate between data that ALREADY exists in the RAW data, and NEW data that needs to be constructed out of the RAW data, and then appended for creating a FULLER RAW data set
for column_name in list_insert_columns:
    
    if column_name in data_raw_ignition.columns:
        
        dict_insert_ignition [column_name] = data_raw_ignition [column_name]
        
    else:
        
        dict_insert_ignition [column_name] = insertColumnData (column_name, dict_insert_columns [column_name])
		
		
		
		
		
#Compute the Resistance Value for each row of data

		
		
		

		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
for key in dict_insert_ignition.keys ():
    
    print "Current Key: ", key, "\n"
	
	
	
	
	
	
	
	
	
	
	
#This will be the insertNewDF function
	
#Create the NEW data set and check to make sure that all of the intended columns (old RAW data as well as new COMPUTED data) exist	
data_insert_ignition = pd.DataFrame (dict_insert_ignition)

print "\n\n\n", data_insert_ignition.columns

#Check that the computed data looks accurate 
for column in data_insert_ignition.columns:
	
	print "Column Name: ", column, "\n\n", data_insert_ignition [column].head (), "\n\n\n"
	
	
	
	
	
	
	
	
	
	

#This will be the insertColumnCalculate function	
	
#Now that the NEW data set is complete, perform computations needed to prepare the data for compilation

#All of the following are grouped by LOT NUMBER
#Avg of TempAtTC, StdDev of TempAtTC
#Avg of End - Start, StdDev of End - Start
#Avg of TimeBetwRuns, StdDev of TimeBetwRuns
#Avg of PowerOffsetStart, StdDev of PowerOffsetStart
#Avg of Amps, StdDev of Amps
#Avg of PowerTrue, StdDev of PowerTrue
#Avg of Voltage, StdDev of Voltage
#Avg of Resistance, StdDev of Resistance
dict_calculation_list = {"TempAtTC": ([], []), "End-Start": ([], []), "TimeBetwRuns": ([], []), "PowerOffsetStart": ([], []), "Amps": ([], []), "PowerTrue": ([], []), "Voltage": ([], []), "Resistance": ([], [])}

 
for calculation in dict_calculation_list.keys ():

	data_insert_ignition ["Average of " + calculation] = data_insert_ignition [calculation]
	data_insert_ignition ["StdDev of " + calculation] = data_insert_ignition [calculation]
	data_insert_ignition ["Min of " + calculation] = pd.Series ([])
	data_insert_ignition ["Max of " + calculation] = pd.Series ([])

	for lot in data_insert_ignition ["Lot"].unique ():
	
		data_calculation_lot = data_insert_ignition [data_insert_ignition.columns] [data_insert_ignition ["Lot"] == lot]
		
		#Because Resistance is sometimes computed as "None" (whenever the denominator value was 0, preventing the computation from taking place) I will substitute in the AVERAGE Resistance value for the LOT in place of the None values
		#Pandas treats NULL values differently from the way fundamental Python does. Python treats them as None dtype. In Pandas, use the "isnull()" function to compare a set of values against their representation of NULL
		data_calculation_lot [calculation] = np.where (data_calculation_lot [calculation].isnull () == True, np.mean (data_calculation_lot [calculation]), data_calculation_lot [calculation])
		#data_calculation_lot [calculation] = np.where (data_calculation_lot [calculation] == '', np.mean (data_calculation_lot [calculation]), data_calculation_lot [calculation])
		
		data_insert_ignition ["Average of " + calculation] = np.where (data_insert_ignition ["Lot"] == lot, np.mean (data_calculation_lot [calculation].tolist ()), data_insert_ignition ["Average of " + calculation])
		data_insert_ignition ["StdDev of " + calculation] = np.where (data_insert_ignition ["Lot"] == lot, np.std (data_calculation_lot [calculation].tolist ()), data_insert_ignition ["StdDev of " + calculation])

		
		
	
print "Column Names AFTER Avg and Std Dev calculations: ", data_insert_ignition.columns, "\n\n"



# for calculation in dict_calculation_list.keys ():

	

	# print "Avg of ", calculation, ": \n\n", data_insert_ignition ["Average of " + calculation], "\n\n\n\n\n\n"
	# print "StdDev of ", calculation, ": \n\n", data_insert_ignition ["StdDev of " + calculation], "\n\n\n\n\n\n"
	
print data_insert_ignition, "\n\n\n"
#print data_insert_ignition ["Lot"]












#This will be the insertColumnQC function

#print data_insert_ignition [data_insert_ignition.columns.values] [data_insert_ignition ["Lot"] == "1958453-3"]

#Now that the Averages and Standard Deviations for the Ignition Data are getting inserted properly, I need to insert the Counts data and the Single/Multiple Data
list_QC_column = ["PressID", "OperatorID", "HeaterLotNum", "CubeLotNum", "Shift"]

for column in list_QC_column:

	data_insert_ignition [column + " QC"] = data_insert_ignition [column]

for lot in data_insert_ignition ["Lot"].unique ():

	data_QC_lot = data_insert_ignition [data_insert_ignition.columns] [data_insert_ignition ["Lot"] == lot]
	
	for column in list_QC_column:
		
		if len (data_QC_lot [column].unique ()) > 1:
		
			data_insert_ignition [column + " QC"] = np.where (data_insert_ignition ["Lot"] == lot, "Multiple", data_insert_ignition [column + " QC"])
			
		elif len (data_QC_lot [column].unique ()) == 1:
		
			data_insert_ignition [column + " QC"] = np.where (data_insert_ignition ["Lot"] == lot, "Single", data_insert_ignition [column + " QC"])
			
		#print data_insert_ignition [["Lot", column, column + " QC"]] [data_insert_ignition ["Lot"] == lot]
		
		#data_insert_ignition [column + " QC"] = np.where (data_QC_lot [column].unique () > 1, "Multiple", "Single")
		
		#"=IF(RC[-5]=" & Chr(34) & Chr(34) & "," & Chr(34) & Chr(34) & ",IF(AND(R[1]C[-5]=" & Chr(34) & Chr(34) & ",RC[-5]<>" & Chr(34) & Chr(34) & ")," & Chr(34) & "Multiple" & Chr(34) & "," & Chr(34) & "Single" & Chr(34) & "))" 'This replaces the line of code below
		
		
		
# print data_insert_ignition, "\n\n\n"
#print data_insert_ignition [[lot, column, column + " QC"]] #[data_insert_ignition ["Lot"] == lot]






#Now calculate Pass, Abort, and Reload values
print data_insert_ignition [["AbortName"]], "\n\n\n"





list_outcome_column = ["Pass", "Scrap", "Reload"]

for column in list_outcome_column:

	data_insert_ignition [column] = data_insert_ignition ["CycleOutcome"]
	

data_insert_ignition ["OutcomeMarker"] = data_insert_ignition ["CycleOutcome"]
data_insert_ignition ["LotMarker"] = data_insert_ignition ["CycleOutcome"]
	
for lot in data_insert_ignition ["Lot"].unique ():

	data_outcome_lot = data_insert_ignition [data_insert_ignition.columns] [data_insert_ignition ["Lot"] == lot]
	
	lot_outcome_count = 0
	
	for column in list_outcome_column:
	
		lot_outcome_count = sum (np.where (data_outcome_lot ["CycleOutcome"] == column, 1, 0))
	
		#if len (data_outcome_lot ["CycleOutcome"].unique ()) > 1:
		
		data_insert_ignition ["OutcomeMarker"] = np.where (data_insert_ignition ["CycleOutcome"] == column, 1, 0)
		data_insert_ignition ["LotMarker"] = np.where (data_insert_ignition ["Lot"] == lot, 1, 0)
			
		data_insert_ignition [column] = np.where (data_insert_ignition ["OutcomeMarker"] == data_insert_ignition ["LotMarker"], lot_outcome_count, data_insert_ignition [column])
			
		#else:
		
		#	data_insert_ignition [column] = np.where (data_insert_ignition ["Lot"] == lot, lot_outcome_count, data_insert_ignition [column])
		
for lot in data_insert_ignition ["Lot"].unique ():

	#for column in list_outcome_column:
	
	if len (data_insert_ignition ["Pass"].unique ()) > 1:
		
		data_insert_ignition ["Pass"] = np.where (data_insert_ignition ["Scrap"] != 0, 0, data_insert_ignition ["Pass"])
		data_insert_ignition ["Pass"] = np.where (data_insert_ignition ["Reload"] != 0, 0, data_insert_ignition ["Pass"])
			










#Condense the insertion data down to one row for each Lot Number which contains the Average, Std Deviation, QC (Single/Multiple), and Scrap/Reload/Pass counts and proportions for the Lot Number
data_insert_condensed = pd.DataFrame (columns=data_insert_ignition.columns)

#I'm trying to use these following two links for constructing a solution to condense the dataframe so that it is the proper arrangement (one row per lot number) for inclusion in the compilation file
#https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.apply.html#pandas.DataFrame.apply
#https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.append.html#pandas.DataFrame.append
for lot in data_insert_ignition ["Lot"].unique ():

	data_insert_condensed = data_insert_condensed.append (data_insert_ignition [data_insert_ignition.columns] [data_insert_ignition ["Lot"] == lot].apply (np.max, axis=0), ignore_index=True)

print "Data Insert Reduced columns: ", data_insert_condensed.columns, "\n\n"
print data_insert_condensed.shape
#Output as a CSV file

list_insert_shiftpress = []

list_insert_abortratio = []

list_insert_reloadratio = []

list_insert_yearmonth = []

for row in range (data_insert_condensed.shape [0]):
	
	list_insert_shiftpress.append (str (data_insert_condensed ["Shift"].loc [row]) + "-" + str (data_insert_condensed ["PressID"].loc [row]))
	
	list_insert_yearmonth.append (str (data_insert_condensed ["Year"].loc [row]) + "-" + str (data_insert_condensed ["Month"].loc [row]))
	
	list_insert_abortratio.append (float (data_insert_condensed ["Scrap"].loc [row])/float ((data_insert_condensed ["Scrap"].loc [row] + data_insert_condensed ["Pass"].loc [row])))
	
	list_insert_reloadratio.append (float (data_insert_condensed ["Reload"].loc [row])/float ((data_insert_condensed ["Scrap"].loc [row] + data_insert_condensed ["Pass"].loc [row])))
	
data_insert_condensed ["Shift Press"] = pd.Series (list_insert_shiftpress)

data_insert_condensed ["Year-Month"] = pd.Series (list_insert_yearmonth)

data_insert_condensed ["Press Abort Ratio"] = pd.Series (list_insert_abortratio)

data_insert_condensed ["Press Reload Ratio"] = pd.Series (list_insert_reloadratio)

data_insert_condensed ["16mm"] = pd.Series ([])

#BEFORE outputting the data, force the columns into this order:
#desired output file order: Year Press,	Month Press,	Year-Month Press,	Day Press,	16mm D82 Y31036 Press File,	Shift Press,	Shift QC,	Press,	Press QC,	Operator ID,	Operator QC,	Heater Lot,	Heater QC,	Cube Lot,	Cube QC,	Amps Avg,	Amps Std Dev,	Amps Max,	Amps Min,	Power Avg,	Power Std Dev,	Power Max,	Power Min,	Volt Avg,	Volt Std Dev,	Volt Max,	Volt Min,	Resistance Avg,	Resistance Std Dev,	Resistance Max,	Resistance Min,	TempTC Avg,	TempTC Std Dev,	TempTC Max,	TempTC Min,	Offset Delta (E-S) Avg,	Offset Delta (E - S) Std Dev,	Offset Delta (E-S) Max,	Offset Delta (E-S) Min,	TIMEbRuns Avg,	TimebRuns Std Dev,	TIMEbRuns Max,	TIMEbRuns Min,	Offset S Avg,	Offset S Std Dev,	Offset S Max,	Offset S Min,	Press Pass,	Press Reload,	Press Abort,	Press Reload ratio,	Press Abort Ratio
#old output file order: AbortName,	Amps,	CubeLotNum,	CycleOutcome,	Day,	End-Start,	HeaterLotNum,	Lot,	Month,	OperatorID,	PowerOffsetEnd,	PowerOffsetStart,	PowerTrue,	PressID,	PressureCalc,	PressurePV,	Recipe,	Resistance,	RunEndTime,	RunLength,	RunStartTime,	RunType,	Shift,	TempAtTC,	Time,	TimeBetwRuns,	Voltage,	Weekday,	Year,	Average of Resistance,	StdDev of Resistance,	Min of Resistance,	Max of Resistance,	Average of PowerOffsetStart,	StdDev of PowerOffsetStart,	Min of PowerOffsetStart,	Max of PowerOffsetStart,	Average of End-Start,	StdDev of End-Start,	Min of End-Start,	Max of End-Start,	Average of PowerTrue,	StdDev of PowerTrue,	Min of PowerTrue,	Max of PowerTrue,	Average of Amps,	StdDev of Amps,	Min of Amps,	Max of Amps,	Average of TimeBetwRuns,	StdDev of TimeBetwRuns,	Min of TimeBetwRuns,	Max of TimeBetwRuns,	Average of TempAtTC,	StdDev of TempAtTC,	Min of TempAtTC,	Max of TempAtTC,	Average of Voltage,	StdDev of Voltage,	Min of Voltage,	Max of Voltage,	PressID QC,	OperatorID QC,	HeaterLotNum QC,	CubeLotNum QC,	Pass,	Scrap,	Reload,	OutcomeMarker,	LotMarker,	Shift Press,	Press Abort Ratio,	Press Reload Ratio,	16mm D82 Y31036 Press File
#new output file order: Year, Month, Year-Month, Day, 16mm D82 Y31036 Press File,		Shift Press, Shift QC,		PressID, PressID QC,		OperatorID, OperatorID QC,		HeaterLotNum, HeaterLotNum QC,		CubeLotNum,	CubeLotNum QC, 		Average of Amps, StdDev of Amps, Max of Amps, Min of Amps,		Average of PowerTrue, StdDev of PowerTrue, Max of PowerTrue, Min of PowerTrue,		Average of Voltage, StdDev of Voltage, Max of Voltage, Min of Voltage,		Average of Resistance, StdDev of Resistance, Max of Resistance, Min of Resistance,		Average of TempAtTC, StdDev of TempAtTC, Max of TempAtTC, Min of TempAtTC,		Average of End-Start, StdDev of End-Start, Max of End-Start, Min of End-Start,		Average of TimeBetwRuns, StdDev of TimeBetwRuns, Max of TimeBetwRuns, Min of TimeBetwRuns,		Average of PowerOffsetStart, StdDev of PowerOffsetStart, Max of PowerOffsetStart, Min of PowerOffsetStart,		Pass, Reload, Scrap, Press Reload Ratio, Press Abort Ratio

data_insert_condensed = data_insert_condensed [["Year", "Month", "Year-Month", "Day", "16mm", "Shift Press", "Shift QC", "PressID", "PressID QC", "OperatorID", "OperatorID QC", "HeaterLotNum", "HeaterLotNum QC", "CubeLotNum", "CubeLotNum QC", "Average of Amps", "StdDev of Amps", "Max of Amps", "Min of Amps", "Average of PowerTrue", "StdDev of PowerTrue", "Max of PowerTrue", "Min of PowerTrue", "Average of Voltage", "StdDev of Voltage", "Max of Voltage", "Min of Voltage", "Average of Resistance", "StdDev of Resistance", "Max of Resistance", "Min of Resistance", "Average of TempAtTC", "StdDev of TempAtTC", "Max of TempAtTC", "Min of TempAtTC", "Average of End-Start", "StdDev of End-Start", "Max of End-Start", "Min of End-Start", "Average of TimeBetwRuns", "StdDev of TimeBetwRuns", "Max of TimeBetwRuns", "Min of TimeBetwRuns", "Average of PowerOffsetStart", "StdDev of PowerOffsetStart", "Max of PowerOffsetStart", "Min of PowerOffsetStart", "Pass", "Reload", "Scrap", "Press Reload Ratio", "Press Abort Ratio"]]

data_insert_ignition.to_csv ("ignition_cleaner_insert.csv")
data_insert_condensed.to_csv ("ignition_cleaner_condensed.csv")