import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt



data_crack_rate = pd.read_csv (os.getcwd () + "\\crackRateAnalysis_rawData_7.csv")
data_crack_rate.sort_values (by=["Date"], ascending=True, inplace=True)



print data_crack_rate.head (), "\n\n"
print data_crack_rate.columns, "\n\n"



data_crack_insert = data_crack_rate ["powder lot 2"] + "_" + data_crack_rate ["Family"]

print data_crack_insert.head (), "\n\n"



data_crack_rate ["Insert"] = data_crack_insert

data_crack_rate ["Total Adjusted Cracks divided by Qty 2 NUMERIC"] = data_crack_rate ["Total Adjusted Cracks divided by Qty 2"].str.replace ("%", "").astype (float) / 100.00
data_crack_rate ["LotNum"] = data_crack_rate ["LotNum"].str.lower ()
data_crack_rate.sort_values (by=["LotNum"], ascending=True, inplace=True)

data_crack_rate ["Overall Rate by Insert Mean"] = pd.Series ()
data_crack_rate ["Overall Rate by Insert Sum/Sum"] = pd.Series ()

data_crack_rate ["Overall Rate by PowderLot Mean"] = pd.Series ()
data_crack_rate ["Overall Rate by PowderLot Sum/Sum"] = pd.Series ()

data_crack_rate ["Early Rate Sum/Sum by PowderLot"] = pd.Series ()
data_crack_rate ["Early Rate Mean by PowderLot"] = pd.Series ()

data_crack_rate ["Early Rate Sum/Sum by Insert"] = pd.Series ()
data_crack_rate ["Early Rate Mean by Insert"] = pd.Series ()
#data_crack_rate ["Overall Rate by Insert"] = data_crack_rate.groupby (["Insert"]) ["Total Adjusted Cracks divided by Qty 2 NUMERIC"].mean ()

print data_crack_rate.columns, "\n\n"
print data_crack_rate.head (), "\n\n"
#print data_crack_rate ["Total Adjusted Cracks divided by Qty 2 NUMERIC"].head (), "\n\n"
#print type (data_crack_rate ["Total Adjusted Cracks divided by Qty 2"]), "\n\n"




def crackRateCompute (total_comp_group, overall_comp_1, overall_comp_2, early_comp_1, early_comp_2):
	
	#powder = iter_comp_group, "powder lot 2" = total_comp_group, "Overall Rate by PowderLot Mean" = overall_comp_1, "Overall Rate by PowderLot Sum/Sum" = overall_comp_2, "Early Rate Mean by PowderLot" = early_comp_1, "Early Rate Sum/Sum by PowderLot" = early_comp_2
	for iter_comp_group in data_crack_rate [total_comp_group].unique ():
		
		data_crack_current = data_crack_rate [data_crack_rate.columns] [data_crack_rate [total_comp_group] == iter_comp_group]
		data_crack_current.sort_values (by=["Date"], ascending=True, inplace=True)
		
		overall_rate_current = data_crack_current ["Total Adjusted Cracks divided by Qty 2 NUMERIC"].mean ()
		
		overall_crack_current = data_crack_current ["Total Adjusted Cracks"].sum ()
		overall_qty_current = data_crack_current ["Qty 2"].sum ()
		
		data_crack_rate [overall_comp_1] = np.where (data_crack_rate [total_comp_group] == iter_comp_group, overall_rate_current, data_crack_rate [overall_comp_1])
		data_crack_rate [overall_comp_2] = np.where (data_crack_rate [total_comp_group] == iter_comp_group, overall_crack_current / (overall_qty_current * 1.0), data_crack_rate [overall_comp_2])
		
		early_sum_current = 0
		early_qty_current = 0
		
		early_avg_current = 0
		early_count_current = 1
		
		early_crack_index = 0
		
		while early_qty_current < 200 and early_crack_index < data_crack_current.shape [0]:
			
			early_qty_current += data_crack_current ["Qty 2"].iloc [early_crack_index]
			
			early_sum_current += data_crack_current ["Total Adjusted Cracks"].iloc [early_crack_index]
			
			
			early_avg_current += data_crack_current ["Total Adjusted Cracks divided by Qty 2 NUMERIC"].iloc [early_crack_index]
			early_count_current += 1
			
			early_crack_index += 1
		
		
		data_crack_rate [early_comp_2] = np.where (data_crack_rate [total_comp_group] == iter_comp_group, early_sum_current / (early_qty_current * 1.0), data_crack_rate [early_comp_2])
		
		data_crack_rate [early_comp_1] = np.where (data_crack_rate [total_comp_group] == iter_comp_group, early_avg_current / (early_count_current * 1.0), data_crack_rate [early_comp_1])



crackRateCompute ("powder lot 2", "Overall Rate by PowderLot Mean", "Overall Rate by PowderLot Sum/Sum", "Early Rate Mean by PowderLot", "Early Rate Sum/Sum by PowderLot")
crackRateCompute ("Insert", "Overall Rate by Insert Mean", "Overall Rate by Insert Sum/Sum", "Early Rate Mean by Insert", "Early Rate Sum/Sum by Insert")


'''
for powder in data_crack_rate ["powder lot 2"].unique ():
	
	data_crack_current = data_crack_rate [data_crack_rate.columns] [data_crack_rate ["powder lot 2"] == powder]
	data_crack_current.sort_values (by=["Date"], ascending=True, inplace=True)
	
	overall_rate_current = data_crack_current ["Total Adjusted Cracks divided by Qty 2 NUMERIC"].mean ()
	
	overall_crack_current = data_crack_current ["Total Adjusted Cracks"].sum ()
	overall_qty_current = data_crack_current ["Qty 2"].sum ()
	
	data_crack_rate ["Overall Rate by PowderLot Mean"] = np.where (data_crack_rate ["powder lot 2"] == powder, overall_rate_current, data_crack_rate ["Overall Rate by PowderLot Mean"])
	data_crack_rate ["Overall Rate by PowderLot Sum/Sum"] = np.where (data_crack_rate ["powder lot 2"] == powder, overall_crack_current / (overall_qty_current * 1.0), data_crack_rate ["Overall Rate by PowderLot Sum/Sum"])
	
	early_sum_current = 0
	early_qty_current = 0
	
	early_avg_current = 0
	early_count_current = 1
	
	early_crack_index = 0
	
	while early_qty_current < 200 and early_crack_index < data_crack_current.shape [0]:
		
		early_qty_current += data_crack_current ["Qty 2"].iloc [early_crack_index]
		
		early_sum_current += data_crack_current ["Total Adjusted Cracks"].iloc [early_crack_index]
		
		
		early_avg_current += data_crack_current ["Total Adjusted Cracks divided by Qty 2 NUMERIC"].iloc [early_crack_index]
		early_count_current += 1
		
		early_crack_index += 1
	
	
	data_crack_rate ["Early Rate Sum/Sum by PowderLot"] = np.where (data_crack_rate ["powder lot 2"] == powder, early_sum_current / (early_qty_current * 1.0), data_crack_rate ["Early Rate Sum/Sum by PowderLot"])
	
	data_crack_rate ["Early Rate Mean by PowderLot"] = np.where (data_crack_rate ["powder lot 2"] == powder, early_avg_current / (early_count_current * 1.0), data_crack_rate ["Early Rate Mean by PowderLot"])





for insert in data_crack_rate ["Insert"].unique ():
	
	data_crack_current = data_crack_rate [data_crack_rate.columns] [data_crack_rate ["Insert"] == insert]
	data_crack_current.sort_values (by=["Date"], ascending=True, inplace=True)
	
	overall_rate_current = data_crack_current ["Total Adjusted Cracks divided by Qty 2 NUMERIC"].mean ()
	
	overall_crack_current = data_crack_current ["Total Adjusted Cracks"].sum ()
	overall_qty_current = data_crack_current ["Qty 2"].sum ()
	
	data_crack_rate ["Overall Rate by Insert Mean"] = np.where (data_crack_rate ["Insert"] == insert, overall_rate_current, data_crack_rate ["Overall Rate by Insert Mean"])
	data_crack_rate ["Overall Rate by Insert Sum/Sum"] = np.where (data_crack_rate ["Insert"] == insert, overall_crack_current / (overall_qty_current * 1.0), data_crack_rate ["Overall Rate by Insert Sum/Sum"])
	
	
	early_sum_current = 0
	early_qty_current = 0
	
	early_avg_current = 0
	early_count_current = 1
	
	early_crack_index = 0
	
	while early_qty_current < 200 and early_crack_index < data_crack_current.shape [0]:
		
		early_qty_current += data_crack_current ["Qty 2"].iloc [early_crack_index]
		
		early_sum_current += data_crack_current ["Total Adjusted Cracks"].iloc [early_crack_index]
		
		early_avg_current += data_crack_current ["Total Adjusted Cracks divided by Qty 2 NUMERIC"].iloc [early_crack_index]
		early_count_current += 1
		
		early_crack_index += 1
	
	
	data_crack_rate ["Early Rate Sum/Sum by Insert"] = np.where (data_crack_rate ["Insert"] == insert, early_sum_current / (early_qty_current * 1.0), data_crack_rate ["Early Rate Sum/Sum by Insert"])
	
	data_crack_rate ["Early Rate Mean by Insert"] = np.where (data_crack_rate ["Insert"] == insert, early_avg_current / (early_count_current * 1.0), data_crack_rate ["Early Rate Mean by Insert"])


#print data_crack_rate.head (), "\n\n"

'''

#Calculate correlation
data_crack_correlationI = data_crack_rate ["Overall Rate by Insert Sum/Sum"].corr (data_crack_rate ["Early Rate Sum/Sum by Insert"])
data_crack_correlationP = data_crack_rate ["Overall Rate by PowderLot Sum/Sum"].corr (data_crack_rate ["Early Rate Sum/Sum by PowderLot"])


data_max_value = max ([max (data_crack_rate ["Overall Rate by Insert Sum/Sum"].tolist ()), max (data_crack_rate ["Early Rate Sum/Sum by Insert"].tolist ()), max (data_crack_rate ["Overall Rate by PowderLot Sum/Sum"].tolist ()), max (data_crack_rate ["Early Rate Sum/Sum by PowderLot"].tolist ())])

'''
def crackRatePlot (title_comp_concatenation, title_comp_correlation, early_comp_2, overall_comp_2):
	x = data_crack_rate [early_comp_2].tolist ()
	y = data_crack_rate [overall_comp_2].tolist ()
	plt.scatter (x, y)
	plt.title ("Early Rate vs Overall Rate for " + title_comp_concatenation + " w/ Corr Coeff: " + str (title_comp_correlation))#str (data_crack_correlationI)) 
	plt.xlabel ("Early Rate")
	plt.ylabel ("Overall Rate")
	plt.xlim (0,1)
	plt.ylim (0,1)
	fit = np.polyfit (x, y, 1)
	f = np.poly1d (fit)
	plt.plot (x, f(x), "r--")

	plt.show ()
	#return None
'''

# Bokeh libraries
from bokeh.io import output_file, output_notebook, curdoc
from bokeh.client import push_session, pull_session

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, CustomJS, Select
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel

#Use the next four lines if 
# Import reset_output (only needed once) 
#from bokeh.plotting import reset_output

# Use reset_output() between subsequent show() calls, as needed
#reset_output()

def crackRatePlot (title_comp_concatenation, title_comp_correlation, early_comp_2, overall_comp_2, source):#, data_max_value):
	output_file ("output_file_" + title_comp_concatenation + ".html", title="Empty Bokeh Figure")
	
	plot = figure ()
	#plot = figure(plot_width=1, plot_height=1)
	#plot.segment(x0=[1, 2, 3], y0=[1, 2, 3], x1=[1, 2, 3], y1=[1.2, 2.5, 3.7], color="#F4A582", line_width=3)
	#plot.scatter (early_comp_2, overall_comp_2, source=source)
	
	
	#menu = []
	#for partfamily in data_crack_rate ["Family"].unique ():
	#	menu.append ((partfamily, partfamily))
	
	#dropdown = Dropdown (label="Part Family", button_type="warning", menu=menu, width=150, callback=CustomJS (crackRateCallback))
	#layout = column(dropdown, plot)

	#show(layout)
	#show (plot)
	return plot




def crackRateData (data_filter_family, data_filter_powder, source):
	
	if data_filter_family != "All" and data_filter_powder != "All":
		subset = source [source.columns] [(source ["Family"] == data_filter_family) & (source ["powder lot 2"] == data_filter_powder)]
	
	elif data_filter_family != "All":
		subset = source [source.columns] [source ["Family"] == data_filter_family]
	
	elif data_filter_powder != "All":
		subset = source [source.columns] [source ["powder lot 2"] == data_filter_powder]
	
	else:
		subset = source
	
	return ColumnDataSource (subset)


print "PowderLot x Part Family (Insert) Correlation: ", str (data_crack_correlationI), "\n\n"
print "PowderLot Correlation: ", str (data_crack_correlationP), "\n\n"

#iSource = crackRateData ("All", "All", data_crack_rate)
#pSource = crackRateData ("All", "All", data_crack_rate)
iDict = dict (family=data_crack_rate['Family'].tolist (), powder=data_crack_rate['powder lot 2'].tolist (), x=data_crack_rate['Early Rate Sum/Sum by Insert'].tolist (), y=data_crack_rate['Overall Rate by Insert Sum/Sum'].tolist ())
iDictSource = ColumnDataSource (iDict)
iBackupSource = ColumnDataSource (iDict)

iPlot = crackRatePlot ("PowderLot x Part Family", data_crack_correlationI, "Early Rate Sum/Sum by Insert", "Overall Rate by Insert Sum/Sum", iDictSource)#, data_max_value)
#iScatter = iPlot.scatter ("Early Rate Sum/Sum by Insert", "Overall Rate by Insert Sum/Sum", source=iSource)
iScatter = iPlot.scatter ('x', 'y', source=iDictSource)


pDict = dict (family=data_crack_rate['Family'].tolist (), powder=data_crack_rate['powder lot 2'].tolist (), x=data_crack_rate['Early Rate Sum/Sum by PowderLot'].tolist (), y=data_crack_rate['Overall Rate by PowderLot Sum/Sum'].tolist ())
pDictSource = ColumnDataSource (pDict)
pBackupSource = ColumnDataSource (pDict)

pPlot = crackRatePlot ("PowderLot", data_crack_correlationP, "Early Rate Sum/Sum by PowderLot", "Overall Rate by PowderLot Sum/Sum", pDictSource)#, data_max_value)
#pScatter = pPlot.scatter ("Early Rate Sum/Sum by PowderLot", "Overall Rate by PowderLot Sum/Sum", source=pSource)
pScatter = pPlot.scatter ('x', 'y', source=pDictSource)

iSelectFamily = Select (value="All", title="Part Family Filer", options= ["All"] + data_crack_rate ["Family"].unique ().tolist ())
iSelectPowder = Select (value="All", title="Powder Lot Filter", options= ["All"] + data_crack_rate ["powder lot 2"].unique ().tolist ())


pSelectFamily = Select (value="All", title="Part Family Filer", options= ["All"] + data_crack_rate ["Family"].unique ().tolist ())
pSelectPowder = Select (value="All", title="Powder Lot Filter", options= ["All"] + data_crack_rate ["powder lot 2"].unique ().tolist ())


def crackRateReplot (attr, old, new):
	
	#print "Entered crackRateReplot and Family = ", select_family.value, " and Powder = ", select_powder.value
	family = "All"
	powder = "All"
	
	if source == iSelectFamily or source == iSelectPowder:
		family = iSelectFamily.value
		powder = iSelectPowder.value
	
	else:
		family = pSelectFamily.value
		powder = pSelectPowder.value

    #plot.title.text = "Weather data for " + cities[city]['title']
	src = crackRateData(family, powder, data_crack_rate)
	#source.data.update(src.data)
	#source.data_source.data = src.data
	if source == iSelectFamily or source == iSelectPowder:
		#iScatter = iPlot.scatter ("Early Rate Sum/Sum by Insert", "Overall Rate by Insert Sum/Sum", source=src)
		#show (iPlot)
		#iScatter.data.update (src.data)
		iScatter.data_source.data = src.data
	
	else:
		#pScatter = pPlot.scatter ("Early Rate Sum/Sum by PowderLot", "Overall Rate by PowderLot Sum/Sum", source=src)
		#show (pPlot)
		#pScatter.data.update (src.data)
		pScatter.data_source.data = src.data
'''
source = ColumnDataSource(data=dict(x=x, y=y))

plot = Figure(plot_width=400, plot_height=400)
plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

def callback(source=source, window=None):
    data = source.data
    f = cb_obj.value
    x, y = data['x'], data['y']
    for i in range(len(x)):
        y[i] = window.Math.pow(x[i], f)
    source.trigger('change')

slider = Slider(start=0.1, end=4, value=1, step=.1, title="power",
                callback=CustomJS.from_py_func(callback))
'''





#iSelectFamily.on_change ('value', crackRateReplot)
#iSelectPowder.on_change ('value', crackRateReplot)


#pSelectFamily.on_change ('value', crackRateReplot)
#pSelectPowder.on_change ('value', crackRateReplot)


pCallback = CustomJS (args=dict (source=pDictSource, backup=pBackupSource, family=pSelectFamily, powder=pSelectPowder, ploty=pPlot.y_range, plotx=pPlot.x_range), code="""

	
	var family=family.value;
	var powder=powder.value;
	
	var data=source.data;
	var backup = backup.data;
	
	var familyArrayIn = data ['family'];
	var powderArrayIn = data ['powder'];
	var xArrayIn = data ['x'];
	var yArrayIn = data ['y'];
	
	var familyBackupIn = backup ['family'];
	var powderBackupIn = backup ['powder'];
	var xBackupIn = backup ['x'];
	var yBackupIn = backup ['y'];
	
	
	
	//alert ('Entered the CustomJS callback for Insert and family = ' + family + ' and powder = ' + powder);
	
	//alert ('Input X = ' + xArrayIn.length + ' and Input Y = ' + yArrayIn.length + ' and Input Family = ' + familyArrayIn.length + ' and Input Powder = ' + powderArrayIn.length);
	//alert ('Backup X = ' + xBackupIn.length + ' and Backup Y = ' + yBackupIn.length + ' and Backup Family = ' + familyBackupIn.length + ' and Backup Powder = ' + powderBackupIn.length);
	
	if (familyArrayIn.length < familyBackupIn.length && powderArrayIn.length < powderBackupIn.length && xArrayIn.length < xBackupIn.length && yArrayIn.length < yBackupIn.length)
	{
		//alert ('One of the Input Arrays is smaller than its corresponding Backup Array');
	
		familyArrayIn = familyBackupIn;
		powderArrayIn = powderBackupIn;
		xArrayIn = xBackupIn;
		yArrayIn = yBackupIn;
	}
	
	//alert ('Entered the CustomJS callback for Insert and family = ' + family + ' and powder = ' + powder);
	
	//alert ('Input X = ' + xArrayIn.length + ' and Input Y = ' + yArrayIn.length);
	
	
	var xArrayOut = [];
	var yArrayOut = [];
	var familyArrayOut = [];
	var powderArrayOut = [];
	
	var indexArray = [];
	
	
	//alert ('Set up the Empty Arrays');
	
	
	
	if ((family != 'All' && powder != 'All') || (family != 'All') || (powder != 'All'))
	{
		//alert ('Family and/or Powder != All .... Family = ' + family + ' and Powder = ' + powder);
	
		for (var i=0; i<familyArrayIn.length; i++)
		{
			if (family != 'All' && powder != 'All' && familyArrayIn [i] == family && powderArrayIn [i] == powder)
			{
				indexArray.push (i);
			}
			
			else if (family != 'All' && familyArrayIn [i] == family)
			{
				indexArray.push (i);
			}
			
			else if (powder != 'All' && powderArrayIn [i] == powder)
			{
				indexArray.push (i);
			}
		}
	}
	
	//alert ('Finished identifying indices');
	

	
	if (indexArray.length > 0)
	{
		for (var i=0; i<indexArray.length; i++)
		{
			xArrayOut.push (xArrayIn [indexArray [i]]);
			yArrayOut.push (yArrayIn [indexArray [i]]);
			familyArrayOut.push (familyArrayIn [indexArray [i]]);
			powderArrayOut.push (powderArrayIn [indexArray [i]]);
		}
	}
	
	else
	{
		xArrayOut = xArrayIn;
		yArrayOut = yArrayIn;
		familyArrayOut = familyArrayIn;
		powderArrayOut = powderArrayIn;
	}
	
	
	
	data ['x'] = xArrayOut;
	data ['y'] = yArrayOut;
	data ['family'] = familyArrayOut;
	data ['powder'] = powderArrayOut;
	
	//alert ('Finished identifying output');
	
	alert (' Output X = ' + data ['x'].length + ' and Output Y = ' + data ['y'].length);
	alert (' Output X = ' + data ['x']);
	alert (' Output Y = ' + data ['y']);

	source.change.emit ();
	

	alert ('Calculating X Max');
	plotMaxX = Math.max.apply (Math, data ['x']);
	alert ('Calculated X Max: ' + plotMaxX);
	
	alert ('Initial Plot X Max: ' +  plotx.end);
	plotx.start = -0.02;
	plotx.end = plotMaxX;
	alert ('New Plot X Max: ' + plotx.end);
	
	plotx.change.emit ();
	alert ('Emitted Plot X Max change');
	
	plotMaxY = Math.max.apply (Math, data ['y']);
	ploty.start = -0.02;
	ploty.end = plotMaxY;
	
	ploty.change.emit ();
""")
pSelectFamily.js_on_change ('value', pCallback)
pSelectPowder.js_on_change ('value', pCallback)










iCallback = CustomJS (args=dict (source=iDictSource, backup=iBackupSource, family=iSelectFamily, powder=iSelectPowder), code="""

	
	var family=family.value;
	var powder=powder.value;
	
	var data=source.data;
	var backup = backup.data;
	
	var familyArrayIn = data ['family'];
	var powderArrayIn = data ['powder'];
	var xArrayIn = data ['x'];
	var yArrayIn = data ['y'];
	
	var familyBackupIn = backup ['family'];
	var powderBackupIn = backup ['powder'];
	var xBackupIn = backup ['x'];
	var yBackupIn = backup ['y'];
	
	
	
	//alert ('Entered the CustomJS callback for Insert and family = ' + family + ' and powder = ' + powder);
	
	//alert ('Input X = ' + xArrayIn.length + ' and Input Y = ' + yArrayIn.length + ' and Input Family = ' + familyArrayIn.length + ' and Input Powder = ' + powderArrayIn.length);
	//alert ('Backup X = ' + xBackupIn.length + ' and Backup Y = ' + yBackupIn.length + ' and Backup Family = ' + familyBackupIn.length + ' and Backup Powder = ' + powderBackupIn.length);
	
	if (familyArrayIn.length < familyBackupIn.length && powderArrayIn.length < powderBackupIn.length && xArrayIn.length < xBackupIn.length && yArrayIn.length < yBackupIn.length)
	{
		//alert ('One of the Input Arrays is smaller than its corresponding Backup Array');
	
		familyArrayIn = familyBackupIn;
		powderArrayIn = powderBackupIn;
		xArrayIn = xBackupIn;
		yArrayIn = yBackupIn;
	}
	
	//alert ('Entered the CustomJS callback for Insert and family = ' + family + ' and powder = ' + powder);
	
	//alert ('Input X = ' + xArrayIn.length + ' and Input Y = ' + yArrayIn.length);
	
	
	var xArrayOut = [];
	var yArrayOut = [];
	var familyArrayOut = [];
	var powderArrayOut = [];
	
	var indexArray = [];
	
	
	//alert ('Set up the Empty Arrays');
	
	
	
	if ((family != 'All' && powder != 'All') || (family != 'All') || (powder != 'All'))
	{
		//alert ('Family and/or Powder != All .... Family = ' + family + ' and Powder = ' + powder);
	
		for (var i=0; i<familyArrayIn.length; i++)
		{
			if (family != 'All' && powder != 'All' && familyArrayIn [i] == family && powderArrayIn [i] == powder)
			{
				indexArray.push (i);
			}
			
			else if (family != 'All' && familyArrayIn [i] == family)
			{
				indexArray.push (i);
			}
			
			else if (powder != 'All' && powderArrayIn [i] == powder)
			{
				indexArray.push (i);
			}
		}
	}
	
	//alert ('Finished identifying indices');
	

	
	if (indexArray.length > 0)
	{
		for (var i=0; i<indexArray.length; i++)
		{
			xArrayOut.push (xArrayIn [indexArray [i]]);
			yArrayOut.push (yArrayIn [indexArray [i]]);
			familyArrayOut.push (familyArrayIn [indexArray [i]]);
			powderArrayOut.push (powderArrayIn [indexArray [i]]);
		}
	}
	
	else
	{
		xArrayOut = xArrayIn;
		yArrayOut = yArrayIn;
		familyArrayOut = familyArrayIn;
		powderArrayOut = powderArrayIn;
	}
	
	
	
	data ['x'] = xArrayOut;
	data ['y'] = yArrayOut;
	data ['family'] = familyArrayOut;
	data ['powder'] = powderArrayOut;
	
	//alert ('Finished identifying output');
	
	//alert (' Output X = ' + data ['x'].length + ' and Output Y = ' + data ['y'].length);
	

	source.change.emit ();
""")
iSelectFamily.js_on_change ('value', iCallback)
iSelectPowder.js_on_change ('value', iCallback)






iControl = column (iSelectFamily, iSelectPowder)
pControl = column (pSelectFamily, pSelectPowder)

iLayout = row (iPlot, iControl)
pLayout = row (pPlot, pControl)



show (pLayout)

show (iLayout)


#curdoc.add_root (iLayout, pLayout)
'''
#Scatterplot of Relationship
x = data_crack_rate ["Early Rate Sum/Sum by Insert"].tolist ()
y = data_crack_rate ["Overall Rate by Insert Sum/Sum"].tolist ()
plt.scatter (x, y)
plt.title ("Early Rate vs Overall Rate for PowderLot x Part Family w/ Corr Coeff: " + str (data_crack_correlationI)) 
plt.xlabel ("Early Rate")
plt.ylabel ("Overall Rate")
plt.xlim (0,1)
plt.ylim (0,1)
fit = np.polyfit (x, y, 1)
f = np.poly1d (fit)
plt.plot (x, f(x), "r--")

plt.show ()

x = data_crack_rate ["Early Rate Sum/Sum by PowderLot"].tolist ()
y = data_crack_rate ["Overall Rate by PowderLot Sum/Sum"].tolist ()
plt.scatter (x, y)
plt.title ("Early Rate vs Overall Rate for PowderLot w/ Corr Coeff: " + str (data_crack_correlationP)) 
plt.xlabel ("Early Rate")
plt.ylabel ("Overall Rate")
plt.xlim (0,1)
plt.ylim (0,1)
fit = np.polyfit (x, y, 1)
f = np.poly1d (fit)
plt.plot (x, f(x), "r--")
#plt.title ("Early Rate vs Overall True Rate w/ Corr Coeff: " + str (data_crack_correlation))

plt.show ()


#data_crack_rate.to_csv ("crackRateOutput_8.csv")
#x = data_crack_rate 
'''

