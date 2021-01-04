from .algorithms.method_4 import Method_4
from ..resources.db_classes import Transformer

method_switcher = {4: Method_4}

def calculate_all_transformers(session, method):
	"""
	Returns a list of tupples with the following structure:
		[(transformer_id, [(datestamp, result), (datestamp, result), ...]),
		(transformer_id, [(datestamp, result), (datestamp, result), ...]),...]
	If a transformer as missing data, it doesn't append to the final result
	"""
	transfomer_list = session.query(Transformer)
	
	m = method_switcher[method]()

	results = []
	for tr in transfomer_list:
		result = m.calculate_for_transformer(tr)
		if result:
			results.append((tr.id_transformer, result))

		pass
	return results