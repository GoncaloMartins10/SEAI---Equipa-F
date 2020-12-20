from excel_extract import Excel_extract
from db_populate import DataBase, DatabaseException, Dissolved_gas_measurements, Oil_quality_measurements
import time
import datetime

def convertToFloat(value):
	if type(value) is str:
		filtered = value.split("x") # Não consigo filtrar o ^ por algum motivo...
		i = float(filtered[0].replace(',','.'))
		i = i*pow(10, int(filtered[1][3:]))
		#return float(value[:4].replace(',','.'))*pow(10, int(value[-1]))
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

if __name__ == "__main__":
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

	db = DataBase(db_url,False)

	transformer_1 = Excel_extract(r'dados/Template SE1.xlsx')

	# insert_DGA(db, transformer_1.filter_DGA())
	# insert_GOT(db, transformer_1.filter_GOT())
	load,_ = transformer_1.filter_Load()
	for _, data in load.iteritems():
		a = []
		for d in data:
			a.append(convertToFloat(d))
		print(a)
		#sample = Dissolved_gas_measurements(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7])
		#db.insert(sample)

	#db.commit()


