from .algorithms.method_1 import Method_1
from .algorithms.method_2 import Method_2
from .algorithms.method_4 import Method_4
from .algorithms.method_3 import MultiFeatureIndex
from ..resources.db_classes import Transformer
from ..resources.Mixins import MixinsTables

method_switcher = { 1: Method_1, \
					2: Method_2,\
					3: MultiFeatureIndex, \
					4: Method_4 }

def populate_health_index(session, batch):
	MixinsTables.add_batch(session, batch)

def calculate_for_transformer(session, transformer, method_id, populate = True):
	m = method_switcher[method_id]()

	result = m.calculate_for_transformer(transformer)

	return result



def calculate_all_transformers(session, method_id, populate = True):
	"""
	Returns a list of tupples with the following structure:
		[(transformer_id, [(datestamp, result), (datestamp, result), ...]),
		(transformer_id, [(datestamp, result), (datestamp, result), ...]),...]
	If a transformer as missing data, it doesn't append to the final result
	"""
	transfomer_list = session.query(Transformer)
	
	m = method_switcher[method_id]()

	results = []
	for tr in transfomer_list:
		result = m.calculate_for_transformer(tr)
		if result:
			results.append((tr.id_transformer, result))

		if populate: populate_health_index(session, result)

	return results
