import os
import glob
import re
import pandas as pd



		

parse_dict = {}
		
count_assembly = 0

directory = ""
if os.getcwd ().find ("JoblotDataConstruction") == -1:
	directory = os.getcwd () + "\\JoblotDataConstruction\\texts\\"
else:
	directory = os.getcwd () + "\\texts\\"
print ("Directory: ", directory, "\n\n")

files = os.listdir (directory)

for file in files:
	
	print ("File: ", file, "\n\n")
	
	filematch = re.search (".py", file)
	
	if filematch is None:
		
		print ("File: ", file, "\n\n")
		
		file = open (directory + file, "r")
		
		print ("File is: ", file, "\n\n")
		
		text = file.readlines ()
		
		index = 0
		
		item_mark = None
		
		while index < len(text):
			line = text [index]
			line_assmebly = ""
			line_lot = ""
			line_sfg = ""
			line_status = ""
			
			match_assembly = re.search (r"Assembly:\s+([a-z]*[A-Z]*[0-9]*)*\s", line)
			match_lot = re.search (r"Lot:\s+([a-z]*[A-Z]*[0-9]*)*\s", line)
			match_sfg = re.search (r"([0-9]+(-)*\d*)\s+EA", line)
			match_status = re.search (r"Status:\s+([a-z]*[A-Z]*[0-9]*)*\s", line)
			match_item = re.search (r"Item", line)
			
			if match_assembly:
				print ("Matched Assembly: ", line, "\n\n")
				count_assembly += 1
				line_assembly = line
				parse_dict [count_assembly] = {}
				#parse_dict [count_assembly] ["File Name"] = file
				parse_dict [count_assembly] ["SFG Lines"] = []
				parse_dict [count_assembly] ["SFG Items"] = []
				parse_dict [count_assembly] ["Description Line"] = line
				
			elif match_lot:
				print ("Matched FI: ", line, "\n\n")
				line_lot = line
				parse_dict [count_assembly] ["FI Line"] = line
				parse_dict [count_assembly] ["Release Date"] = None
				
			elif match_status:
				print ("Matched Status: ", line, "\n\n")
				line_status = line
				parse_dict [count_assembly] ["Status Line"] = line
				
			elif match_item:
				parse_dict [count_assembly] ["Item Mark"] = line.find ("Item")
				item_mark = None
				
			elif match_sfg:
				print ("Matched SFG: ", line, "\n\n")
				line_sfg = line
				parse_dict [count_assembly] ["SFG Lines"].append (line)
				if line [parse_dict [count_assembly] ["Item Mark"]] != " ":
					parse_dict [count_assembly] ["SFG Items"].append (line.split () [0])
					item_mark = line.split () [0]
				else:
					parse_dict [count_assembly] ["SFG Items"].append (item_mark)
			'''
			#if index < len (text):
			
			line = text [index]
			
			lotmatch = re.search (r"Lot:\s+([a-z]*[A-Z]*[0-9]*)*\s", line)
			
			if lotmatch:
				
				print "Lot Match: ", lotmatch, "\n"
				print "Line: ", line, "\n\n"
				
				dict [line] = {}
				
				index += 1
				line = text [index]
				newlot = re.search (r"Lot:\s+([a-z]*[A-Z]*[0-9]*)*\s", line)
				
				while not newlot and index < len(text):
					
					newline = re.search (r"Lot\s+([a-z]*[A-Z]*[0-9]*)*\s+UOM", line)
					index += 1
					
					
					while not newline and index < len (text):
						line = text [index]
						newline = re.search (r"Lot\s+([a-z]*[A-Z]*[0-9]*)*\s+UOM", line)
						newtext = re.search (r"EA", line)
						
						if newtext:
							print "NON Parent Lot Match:", newline, "\n"
							print "Line: ", line, "\n\n"
							
						index += 1
						
						
						
					index += 1
					line = text [index]
					newlot = re.search (r"Lot:\s+([a-z]*[A-Z]*[0-9]*)*\s", line)
					
				index -= 1
				
				
			'''
			index += 1
			
composition_dict = {}
composition_dict ["SFG Lot"] = []
composition_dict ["SFG PN"] = []
composition_dict ["SFG Qty"] = []
composition_dict ["Description"] = []
composition_dict ["FI Lot"] = []
composition_dict ["FI PN"] = []
composition_dict ["Planned Qty"] = []
composition_dict ["Completed Qty"] = []
composition_dict ["Release Date"] = []
composition_dict ["Complete Date"] = []
#composition_dict ["File Name"] = []

		

for id in parse_dict.keys ():
	
	item_index = 0
	for sfg_line in parse_dict [id] ["SFG Lines"]:
		
		composition_dict ["SFG Lot"].append (sfg_line.split () [len (sfg_line.split ()) - 3])
		composition_dict ["SFG PN"].append (parse_dict [id] ["SFG Items"] [item_index])#(sfg_line.split () [0])
		composition_dict ["SFG Qty"].append (sfg_line.split () [len (sfg_line.split ()) - 1])
		composition_dict ["Description"].append (" ".join (parse_dict [id] ["Description Line"].split () [2:]))
		composition_dict ["FI Lot"].append (parse_dict [id] ["FI Line"].split () [1].split () [0])
		composition_dict ["FI PN"].append (parse_dict [id] ["Description Line"].split () [1])
		composition_dict ["Planned Qty"].append (parse_dict [id] ["FI Line"].split () [6])
		composition_dict ["Completed Qty"].append (parse_dict [id] ["Status Line"].split () [8])
		composition_dict ["Release Date"].append (parse_dict [id] ["FI Line"].split () [len (parse_dict [id] ["FI Line"].split ()) - 1])
		composition_dict ["Complete Date"].append (parse_dict [id] ["Status Line"].split () [len (parse_dict [id] ["Status Line"].split ()) - 1].replace ("Date:", ""))
		#composition_dict ["File Name"].append (parse_dict [id] ["File Name"])
		item_index += 1
		
	
composition_columns = ["SFG Lot", "SFG PN", "FI Lot", "FI PN", "FI Description", "SFG Qty", "Planned Qty", "Completed Qty", "Release Date", "Complete Date"]
composition_df = pd.DataFrame.from_dict (composition_dict)			

print ("Composition DF Head: ", composition_df.head (), "\n\n")
#with open (os.getcwd () + '1.csv', 'a') as f:
#	composition_df.to_csv (f, header=True)
composition_df.to_csv ('master job lot comp.csv')
'''
print "SFG Lot Length: ", len (composition_dict ["SFG Lot"]), "\n\n"
print "SFG PN Length: ", len (composition_dict ["SFG PN"]), "\n\n"
print "SFG Qty Length: ", len (composition_dict ["SFG Qty"]), "\n\n"
print "Description Length: ", len (composition_dict ["Description"]), "\n\n"
print "FI Lot Length: ", len (composition_dict ["FI Lot"]), "\n\n"
print "FI PN Length: ", len (composition_dict ["FI PN"]), "\n\n"
print "Planned Qty Length: ", len (composition_dict ["Planned Qty"]), "\n\n"
print "Completed Qty Length: ", len (composition_dict ["Completed Qty"]), "\n\n"
'''