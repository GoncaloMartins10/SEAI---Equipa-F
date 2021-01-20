from datetime import date
from ...resources.db_classes import *

from ...resources import Session 
session = Session()

class Queried_data:
	def __init__(self, query):
		self.query = query
		self._type = type(query[0])
		self._position = None

	def __repr__(self):
		return f'Type {self._type}'

	def get_data_as_list(self):
		data_list = []
		for i in range(self.query.count()):
			data_list.append(self.query[i])
		return data_list

	def get_length(self):
		return self.query.count()

	def get_data(self):
		if self._position:
			return self.query[self._position]
		else:
			return None
	
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
	
	def _get_oldest_date(self):
		return self.query[0].datestamp

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

def get_oldest_date(queries):
		datestamp = date.today()
		for q in queries:
			d = q._get_oldest_date()
			if d < datestamp:
				datestamp = d
		
		return datestamp

def get_next_chronological_envents(queries):
	""" Returns next list of events whith the corresponding date """
	same_date_q = []
	new_date = date.today()

	# Check all event with the same date as the oldest event
	for q in queries:
		d = q.get_next_date()
		if d is None:
			continue
		elif d < new_date:
			new_date = d
			same_date_q = []
		while d == new_date:
			same_date_q.append(q)
			q.add_position()
			d = q.get_next_date() # Checks if there is any event with the same date and appends to the list
			

	return same_date_q, new_date

def fetch_data(transformer, classes_to_query_list: list):
	""" Returns list of the 5 types of data for HI calculation """
	queries = []

	for c in classes_to_query_list:
		queries.append( Queried_data( query_table(c, session, transformer.id_transformer)))

	return queries
