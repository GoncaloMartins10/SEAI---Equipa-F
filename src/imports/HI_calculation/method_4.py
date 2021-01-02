from datetime import date

from .fetch_data import *
from ..resources.db_classes import *

session = Session()

def test(session):
	transfomer_list = session.query(Transformer)
	
	for tr in transfomer_list:
		queries = fetch_data(tr)
		while True:
			oldest_events_queries, datestamp = get_next_chronological_envents(queries)
			print(oldest_events_queries[0].get_data().datestamp)
			if not oldest_events_queries:
				print("Terminado")
				break
			else:
				for query in oldest_events_queries:
					if isinstance(query.get_data(), Dissolved_Gases):
						print(query.get_data().h2)
			#if prev_datestamp == datestamp:
			#	break
			#else:
			#	#print("#####")
			#	#for q in oldest_events_queries:
			#		#print(q.get_date(), q.type())
			#	prev_datestamp = datestamp
		print(datestamp)
		break

	dict_queries = tr.get_by_time_interval(session,mindate='2002-11-01',maxdate='2020-11-30')
	print(dict_queries['Furfural'][0].quantity)

