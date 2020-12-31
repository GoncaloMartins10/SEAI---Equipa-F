import os
import glob
import time
import datetime
import numpy as np
import re

from excel_extract import Excel_extract
from db_populate import DataBase, DatabaseException, Dissolved_gas_measurements, Oil_quality_measurements

import sys
sys.path.insert(0, sys.path[0] + '/../server/')
from resources.db_classes import Transformer, Furfural, Oil_Quality, Load, Dissolved_Gases
from resources import Session
from resources.Mixins import MixinsTables

def _convert_to_float(value):
	if type(value) is str:
		filtered = value.split("x") # Não consigo filtrar o ^ por algum motivo...
		i = float(filtered[0].replace(',','.'))
		if len(filtered) == 1:
			return i
		else:
			i = i*pow(10, int(filtered[1][3:]))
			return i
	elif type(value) is int or type(value) is float:
		return float(value)
	else:
		# Não levanta excessão, apenas devolve o valor (meio trolha eu sei)
		return value

def _extract_transformer_ID(transformer: str):
	substation = re.search(r"SE\d\d?", transformer)
	is_TP = re.search(r"TP\d\d?", transformer)
	if is_TP: # If it starts or ends with SE_ return id, if it has TP put it in the id
		return substation.group(0) + "_" + is_TP.group(0)
	else:
		return substation.group(0)


def _parse_data_to_object_DGA(transformer, dga):
	samples = []
	for _, data in dga.iteritems():
		a = []
		for d in data:
			a.append(_convert_to_float(d))

		samples.append(Dissolved_Gases(id_transformer=transformer, datestamp = a[0], h2 = a[1], co = a[2], coh2 = a[3], ch4 = a[4], c2h4 = a[5], c2h6 = a[6], c2h2 = a[7]))
	return samples

def _parse_data_to_object_FAL(transformer, fal):
	samples = []
	for _, data in fal.iterrows():
		a = []
		for d in data:
			if type(d) is int or type(d) is float:
				d = _convert_to_float(d)
			a.append(d)
		samples.append(Furfural(id_transformer=transformer, datestamp = a[0], quantity = a[1]))
	
	return samples

def _parse_data_to_object_GOT(transformer, got):
	samples = []
	for _, data in got.iteritems():
		a = []
		for d in data:
			a.append(_convert_to_float(d))
		
		sample = Oil_quality_measurements(a[0], a[1], a[2], a[3], a[4], a[5])
		samples.append(Oil_Quality(id_transformer=transformer, datestamp = a[0], breakdown_voltage = a[1], water_content = a[2], acidity = a[3], color = a[4], interfacial_tension = a[5]))
	return samples

# https://stackoverflow.com/questions/42950/how-to-get-the-last-day-of-the-month
def _last_day_of_month(any_day):
	# this will never fail
	# get close to the end of the month for any day, and add 4 days 'over'
	next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
	# subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
	return next_month - datetime.timedelta(days=next_month.day)

def _parse_data_to_object_Load(transformer: str, load, Sb):
	months = {"jan": 1, "fev" : 2, "mar": 3, "abril": 4, "maio": 5, "jun": 6, "jul": 7, "agosto": 8, "set": 9, "out": 10, "nov": 11, "dez": 12}
	
	substation = re.search(r"SE\d?", transformer)
	if substation is None:
		raise Exception
	substation = substation.group(0)

	year = 0
	samples = []
	for _, data in load.iterrows():

		if year != data.iloc[0] and not np.isnan(data.iloc[0]):
			year = int(data.iloc[0])
		timestamp = _last_day_of_month(datetime.date(year, months[data.iloc[1]], 1))
		samples.append(Load(id_transformer= transformer, datestamp= timestamp, load_factor= data[substation], power_factor = 1))

	return samples


def _parse_data_to_object_Maintenance(transformer: str, maintenance):
	transformer_voltage = None

	has_descriptive_datetime = (len(maintenance.columns)) > 2

	samples = []
	for _, data in maintenance.iterrows():

		prev_timestamp = 0
		
		description = re.search(r"^ ?-? ?SE\d\d? ?-? ?| ?-? ?SE\d\d? ?-? ?$",data[0])
		if description: # If it starts or ends with SE_ doesn't insert space
			replace_txt = ""
		else:
			replace_txt = " "
		description = re.sub(r" ?-? ?SE\d\d? ?-? ?", replace_txt, data[0])

		#	Extracts the rated voltage of the tranformer
		if transformer_voltage is None:
			found_transformer_voltage = re.search(r"\d\d\d ?[kK][vV]", description)
			if found_transformer_voltage:
				transformer_voltage = int(found_transformer_voltage.group(0)[:3])

		# Formats to the correct date time
		if has_descriptive_datetime:
			timestamp = data[1]
		else:
			if prev_timestamp < data[1]:
				prev_timestamp = data[1]
				timestamp = datetime.datetime(int(data[1]),12,31)
		
		# TODO: Score the impact of the maintenance based on the description

		# samples.append()

	return samples, transformer_voltage
		
def populate_database():
	"""
	Populates the database with all the excel files 
	"""
	excel_parent_path = "dados"
	session = Session()

	transformers = glob.glob(os.path.join(excel_parent_path,"*.xlsx"))

	for _, transformer in enumerate(transformers):
		t = Excel_extract(transformer)
		ID = _extract_transformer_ID(transformer)

		load, Sb, _ = t.filter_Load()
		dga = t.filter_DGA()
		got = t.filter_GOT()
		fal = t.filter_FAL()
		_, _, maintenance = t.filter_Maintenance()

		dga_samples = _parse_data_to_object_DGA(ID, dga)
		fal_samples = _parse_data_to_object_FAL(ID, fal)
		got_samples = _parse_data_to_object_GOT(ID, got)
		load_samples = _parse_data_to_object_Load(ID, load, Sb)
		maint_samples, rated_voltage = _parse_data_to_object_Maintenance(ID, maintenance)

		# First, insert the transformer in the database because of the foreign key constraint
		trans = Transformer(id_transformer= ID, nominal_voltage= rated_voltage)
		trans.add(session)

		MixinsTables.add_batch(session, dga_samples)
		MixinsTables.add_batch(session, fal_samples)
		MixinsTables.add_batch(session, got_samples)
		MixinsTables.add_batch(session, load_samples)
		# MixinsTables.add_batch(session, maint_samples)

	session.close()

if __name__ == "__main__":

	populate_database()

	excel_parent_path = "dados"
	db_select = "docker"
	if db_select is "docker":
		db_url = {'drivername': 'postgres',
			'username': 'postgres',
			'password': 'postgres',
			'host': 'localhost',
			'port': 5432,
			'database':'seai'}
	elif db_select is "feup": 
		db_url = {'drivername': 'postgres',
			'username': 'seai',
			'password': 'HEJt4ZGJc',
			'host': 'db.fe.up.pt',
			'port': 5432,
			'database':'seai'}
	else:
		raise DatabaseException("No database selected, database " + db_select + " none existent")