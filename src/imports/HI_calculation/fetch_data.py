from ..resources.db_classes import *
from datetime import date

# Should not be here, should be passed to function arguments (or instantiated in __init__.py??, não sei como esse funciona)
from ..resources import Session 
session = Session()
####

class Queried_data:
	def __init__(self, query):
		self.query = query
		self.type = type(query[0])
		self._position = None

	def get_data_as_list(self):
		data_list = []
		for i in range(self.query.count()):
			data_list.append(self.query[i])
		return data_list

	def get_length(self):
		return self.query.count()

	def get_data(self):
		return self.query[self._position]

	def get_query(self):
		if self._position is None:
			return None
		elif self._position <= (self.query.count() - 1):
			return self.query[self._position]
		else:
			return None

	def get_next_query(self):
		if self._position is None:
			return self.query[0]
		elif self._position < (self.query.count() - 1):
			return self.query[self._position + 1]
		else:
			return None

	def get_date(self):
		if self._position is None:
			return None
		elif self._position <= (self.query.count() - 1):
			return self.query[self._position].datestamp
		else:
			return None

	def get_next_date(self):
		if self._position is None:
			return self.query[0].datestamp
		elif self._position < (self.query.count() - 1):
			return self.query[self._position + 1].datestamp
		else:
			return None

	def add_position(self):
		"""
		Returns 1 if it was successful adding to the position, if it's at the end of the array, doesn't modify position and returns 0
		"""
		if self._position is None:
			self._position = 0
			return 1
		elif self._position < (self.query.count() - 1):
			self._position += 1
			return 1
		else:
			return 0

def query_table(table , session, id):
	return session.query(table).filter(table.id_transformer==id).order_by(table.datestamp)

def get_next_chronological_envents(queries):
	same_date_q = []
	new_date = date.today()

	for q in queries:
		# print(q.get_next_date(), q.type)
		d = q.get_next_date()
		if d is None:
			continue
		elif new_date > d:
			new_date = d

	# Check all event with the same date as the oldest event
	for q in queries:
		d = q.get_next_date()
		if d is None:
			continue
		while d == new_date:
			same_date_q.append(q)
			q.add_position()
			d = q.get_next_date() # Checks if there is any event with the same date and appends to the list
			

	return same_date_q, new_date

# Usar o isinstance() para averiguar de que tipo é o objeto
# isinstance(queries[0].get_next_query(), Dissolved_Gases)

def fetch_data(transformer):
	""" Returns list of the 5 types of data for HI calculation """
	queries = []

	queries.append( Queried_data( query_table(Dissolved_Gases, session, transformer.id_transformer)))
	queries.append( Queried_data( query_table(Furfural, session, transformer.id_transformer)))
	queries.append( Queried_data( query_table(Oil_Quality, session, transformer.id_transformer)))
	queries.append( Queried_data( query_table(Load, session, transformer.id_transformer)))
	queries.append( Queried_data( query_table(Maintenance, session, transformer.id_transformer)))

	return queries