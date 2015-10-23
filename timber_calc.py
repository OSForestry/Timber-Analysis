#!/usr/bin/env python

import numpy, csv, sys
from numpy.lib import recfunctions
from ConfigParser import SafeConfigParser


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

def basalarea_sqm(data,dbh):
	ba = ((numpy.pi*(data[dbh]**2))/4000)
	return recfunctions.append_fields(data,"basal_area",ba)

def vol_cubic():
	return

def vol_doyle():
	return

def vol_scribner():
	return

def vol_international(data,dbh,log_length):
	if log_length == 8:
		vol_8log = ((0.44*(data[dbh]))**2)-(1.20*(data[dbh])-(1.30))
		return recfunctions.append_fields(data,"8ft_log_vol",vol_8log)
	elif log_length == 12:
		vol_12log = ((0.66*(data[dbh]))**2)-(1.47*(data[dbh])-(0.79))
		return recfunctions.append_fields(data,"12ft_log_vol",vol_12log)
	elif log_length == 16:
		vol_16log = ((0.88*(data[dbh]))**2)-(1.52*(data[dbh])-(1.36))
		return recfunctions.append_fields(data,"16ft_log_vol",vol_16log)
	else:
		print "No valid log lenth entered!"
		sys.exit(1)

def main():
	# Read config file
	config = SafeConfigParser(allow_no_value=True)
	config.read("config.cfg")

	#Set variables from config
	input_path = config.get("input", "path")
	input_delimiter = config.get("input","delimiter")
	input_units = config.get("input","measurement_system")
	output_path = config.get("output","path")
	fields = config.get("output","fields")

	# Import the data
	data = import_data(input_path,input_delimiter)

	# Basal Area
	if "ba" in fields:
		if input_units == "imperial": data = basalarea_sqft(data,"dbh")  # Assumes DBH in inches
		if input_units == "metric": data = basalarea_sqm(data,"dbh")  # Assumes DBH in cm

	# Volume
	if "vol" in fields:
		# Set log rule and length
		vol_rule = config.get("volume","rule")
		log_length = config.getint("volume","log_length")

		if vol_rule == "cubic": pass
		elif vol_rule == "doyle": pass
		elif vol_rule == "international":
			data = vol_international(data, "dbh", log_length)
		elif vol_rule == "scribner": pass
		else:
			print vol_rule,"is not a valid option the log rule."
			sys.exit(1)

	# Export the newly created data
	export_data(output_path, data)


if __name__ == "__main__":
	main()