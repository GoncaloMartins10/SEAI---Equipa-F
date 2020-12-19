# https://www.pythonsheets.com/notes/python-sqlalchemy.html
from sqlalchemy import MetaData, exc, create_engine, Table, Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class DataBase:
	def __init__(self, db_url, debug:bool = False):
		# create_engine(‘dialect+driver://username:password@host:port/database’)
		# driver can be psycopg2 for example
		# self.engine = create_engine('postgresql://seai:HEJt4ZGJc@db.fe.up.pt/seai', echo=True)
		self.engine = create_engine(URL(**db_url), echo=debug)
		sqlalchemy_txt = """
   _____ ____    __     _    _      _                          
  / ___// __ \\  / /    / \\  | | ___| |__   ___ _ __ ___  _   _ 
  \\__ \\/ / / / / /    / _ \\ | |/ __| '_ \\ / _ \\ '_ ` _ \\| | | |
 ___/ / /_/ / / /___ / ___ \\| | (__| | | |  __/ | | | | | |_| |
/____/\\___\\_\\/_____//_/   \\_\\_|\\___|_| |_|\\___|_| |_| |_|\\__, |
                                                    	 |___/
"""
		try:
			self.engine.connect()
			print(sqlalchemy_txt)

			self.metaData = MetaData(self.engine)
			print(self.metaData.tables)

			Session = sessionmaker(bind=self.engine)
			self.session = Session()
		except (Exception, exc.SQLAlchemyError) as error:
			print("\t<<< Error connecting to DataBase >>>\n", error)

	def __del__(self):
		self.session.close()

	def insert(self, object):
		try:
			self.session.add(object)
			self.session.commit()
		except (Exception, exc.SQLAlchemyError) as error:
			print("\t<<< Error inserting to DataBase >>>\n", error)

	def delete(self, object, id):
		raise NotImplemented
		try:
			object.query.filter_by(id_dissolved_gas_measurement=1).delete()
			self.session.commit()
		except (Exception, exc.SQLAlchemyError) as error:
			print("\t<<< Error deleting row on DataBase >>>\n", error)

class AttributeException(Exception):
	def __init__(self, message=None):
		self.message = self.message if message!=None else self.__class__.__name__
		super.__init__(self.message)

class DatabaseException(Exception):
	def __init__(self, message=None):
		self.message = self.message if message!=None else self.__class__.__name__
		super.__init__(self.message)

class Dissolved_gas_measurements(Base):
	__tablename__="dissolved_gas_measurements"
	__table_args__ ={"schema": "ges_ativos"}
	
	id_dissolved_gas_measurement  = Column(Integer, primary_key=True)
	timestamp_dissolved_gas_measurements = Column(DateTime)
	h2 		= Column(Float)
	ch4		= Column(Float)
	c2h6	= Column(Float)
	c2h4	= Column(Float)
	c2h2	= Column(Float)
	co 		= Column(Float)
	coh2	= Column(Float)


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
	db = DataBase(db_url,True)

	test_data = Dissolved_gas_measurements()
	
	test_data.id_dissolved_gas_measurement = 2
	test_data.h2 = 2.2
	test_data.ch4 = 43
	test_data.c2h6 = 12
	
	db.insert(test_data)