from datetime import date


from .fetch_data import fetch_data, get_next_chronological_envents
from ..resources.db_classes import *



def test(session):
	transfomer_list = session.query(Transformer)
	
	for tr in transfomer_list:
		queries = fetch_data(tr)

		oldest_events_queries, datestamp = get_next_chronological_envents(queries)
		while oldest_events_queries:  										# Verifica se é uma lista vazia
			calculate_HI_4(oldest_events_queries, datestamp)
			oldest_events_queries, datestamp = get_next_chronological_envents(queries)

		print("Finnished!")
		break
