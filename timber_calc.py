#!/usr/bin/env python

import numpy, csv
from numpy.lib import recfunctions


# Set user variables, this will migrate to command line arg
input_path = "/home/eaerdmann/git/osforestry/Timber-Calculations/sample_data/ExampleA-TreeSpeciesDBH.csv"
output_path = "/home/eaerdmann/git/osforestry/Timber-Calculations/tmp.csv"
delimiter = ","
plot_type = ""
unit_type = ""
log_length= ""

def import_data(path,delimiter):
	# Generate numpy array from input
	return numpy.genfromtxt(path,dtype=None,delimiter=delimiter,filling_values=0,names=True,case_sensitive="lower",autostrip=True)

def export_data(path,data):
	# Open file
	out_csv = csv.writer(open(path,"w"), dialect="excel")
	# Write field names then the data
	out_csv.writerow(list(data.dtype.names))
	out_csv.writerows(data.tolist())
	return

def basalarea_sqft(data,dbh):
	ba = ((numpy.pi*(data[dbh]**2))/576)
	return recfunctions.append_fields(data,"basal_area",ba)

def vol_international(data,dbh,log_length):
	if log_length == 8:
		vol_8log = ((0.44*(data[dbh]))**2)-(1.20*(data[dbh])-(1.30))
		return recfunctions.append_fields(data, "8 ft log volume", vol_8log)
	elif log_length == 12:
		vol_12log = ((0.66*(data[dbh]))**2)-(1.47*(data[dbh])-(0.79))
		return recfunctions.append_fields(data, "12 ft log volume", vol_12log)
	elif log_length == 16:
		vol_16log = ((0.88*(data[dbh]))**2)-(1.52*(data[dbh])-(1.36))
		return recfunctions.append_fields(data, "16 ft log volume", vol_16log)
	else:
		print "No valid log lenth entered!"

# Calculate Basal Area in SqFt Example (Replace the basalarea_sqft function with what ever funciton is being tested)
data = import_data(input_path,delimiter)  # Import the data from csv
data = basalarea_sqft(data[dbh]) 
export_data(output_path, data)  # Exhow to return multiple values from a function in pythonport the newly edited data to csv


""" 
	Optionally you could use:
	export_data(output_path, basalarea_sqft(import_data(input_path,delimiter),"dbh"))
	but this is fairly confusing to interpret.
"""

