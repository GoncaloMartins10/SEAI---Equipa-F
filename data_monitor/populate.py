import os
import time
import datetime
import numpy as np
# For string manipulation
# https://stackabuse.com/using-regex-for-text-manipulation-in-python/
import re

from excel_extract import Excel_extract
from db_populate import DataBase, DatabaseException, Dissolved_gas_measurements, Oil_quality_measurements


def convertToFloat(value):
	if type(value) is str:
		filtered = value.split("x") # Não consigo filtrar o ^ por algum motivo...
		i = float(filtered[0].replace(',','.'))
		i = i*pow(10, int(filtered[1][3:]))
		return i
	elif type(value) is int or type(value) is float:
		return float(value)
	else:
		# Não levanta excessão, apenas devolve o valor (meio trolha eu sei)
		return value

def insert_DGA(db:DataBase, dga):
	for _, data in dga.iteritems():
		a = []
		for d in data:
			a.append(convertToFloat(d))
		sample = Dissolved_gas_measurements(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7])
		db.insert(sample)

def insert_GOT(db:DataBase, got):
	for _, data in got.iteritems():
			a = []
			for d in data:
				a.append(convertToFloat(d))
			sample = Oil_quality_measurements(a[0], a[1], a[2], a[3], a[4], a[5])
			db.insert(sample)

# https://stackoverflow.com/questions/42950/how-to-get-the-last-day-of-the-month
def last_day_of_month(any_day):
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    return next_month - datetime.timedelta(days=next_month.day)

def insert_Load(db:DataBase, transformer: str, load, Sb):
	substation = re.search(r"SE\d?", transformer)
	if substation is None:
		raise Exception
	substation = substation.group(0)

	year = 0
	for _, data in load.iterrows():

		if year != data.iloc[0] and not np.isnan(data.iloc[0]):
			year = int(data.iloc[0])
			print(year)
		months = {"jan": 1, "fev" : 2, "mar": 3, "abril": 4, "maio": 5, "jun": 6, "jul": 7, "agosto": 8, "set": 9, "out": 10, "nov": 11, "dez": 12}
		print(data[substation])
		timestamp = last_day_of_month(datetime.datetime(year, months[data.iloc[1]], 1))
		print(timestamp)

def insert_Maintenance(db:DataBase, maintenance):
	transformer_voltage = None

	has_descriptive_datetime = (len(maintenance.columns)) > 2

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
		

	return transformer_voltage
		

if __name__ == "__main__":
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

	# db = DataBase(db_url,False)

	# transformer_1 = Excel_extract(r'dados/Template SE1.xlsx')

	# ver glob.glob (permite fazer regex)
	transformers = os.listdir(excel_parent_path)
	for number, transformer in enumerate(transformers):
		t = Excel_extract(os.path.join(excel_parent_path,transformer))
		
		load, Sb, _ = t.filter_Load()

		insert_Load(None, transformer, load, Sb)

		# dga = t.filter_DGA()
		# got = t.filter_GOT()
		# _, _, maintenance = t.filter_Maintenance()

		# insert_DGA(db, dga)
		# insert_GOT(db, got)
		# rated_voltage = insert_Maintenance(db, maintenance)
	
	
	# load, Sb, _ = t.filter_Load()
	# for _, data in load.iteritems():
	# 	a = []
	# 	for d in data:
	# 		a.append(convertToFloat(d))
		# print(a)
			

		#sample = Dissolved_gas_measurements(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7])
		#db.insert(sample)
			
	#db.commit()