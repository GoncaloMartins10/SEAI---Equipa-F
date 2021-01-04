from datetime import date
from math import isnan
import json
import os

from .fetch_data import fetch_data, get_next_chronological_envents, Queried_data
from ..resources.db_classes import *

class WaS: # Weights and Scores
	def __init__(self, weight, start, scores):
		self.weight = weight
		self.start = start
		self.scores = scores

	def get_score(self, value):
		if value < 0 :
			print("Invalid number. ", value, " should be positive")
			raise Exception

		if self.scores[0] < self.scores[1]: # Checks if the scores are in increasing or decreasing order
			for i, s in enumerate(self.scores[::-1]):
				if value >= s:
					result = len(self.scores) - i - 1 + self.start
					return result
		else:
			for i, s in enumerate(self.scores):
				if value >= s:
					result = i + self.start
					return result

class Method_4:
	def __init__(self, transformer_voltage = None):
		cwd = os.getcwd()
		repo_name = 'SEAI---Equipa-F'
		repo_dir = cwd[:cwd.rindex(repo_name) + len(repo_name)] # retira tudo depois de 'SEAI---Equipa-F'
		weight_path = os.path.join(repo_dir,"src/imports/HI_calculation/weights.json")

		with open(weight_path, "r") as file: 
		    self.config = json.load(file)
		
		if transformer_voltage:
			self.update_method_weights(transformer_voltage)


	def update_method_weights(self, transformer_voltage):
		w = "weight"
		s = "starts"
		sc = "scores"

		for key, val in self.config["Method 4"].items():
			if key == "Dissolved_Gases":
				self.h2 = WaS(val['h2'][w], val['h2'][s], val['h2'][sc]) 

				self.ch4 = WaS(val['ch4'][w], val['ch4'][s], val['ch4'][sc])

				self.c2h6 = WaS(val['c2h6'][w], val['c2h6'][s], val['c2h6'][sc])
				
				self.c2h4 = WaS(val['c2h4'][w], val['c2h4'][s], val['c2h4'][sc])

				self.c2h2 = WaS(val['c2h2'][w], val['c2h2'][s], val['c2h2'][sc])

				self.co = WaS(val['co'][w], val['co'][s], val['co'][sc])

				self.coh2 = WaS(val['coh2'][w], val['coh2'][s], val['coh2'][sc])


				self.dga = WaS(self.config["Method 4"][w]["Dissolved_Gases"], val[w]["starts"], val[w]["scores"])
			elif key == "Oil_Quality":
				for k, v in val.items():
					if "voltage" in v:
						rated_volts = list(map(int, list(v["voltage"].keys())))
						rated_volts.sort(reverse = True)
						for volts in rated_volts:
							if transformer_voltage >= volts:
								weight = WaS(v[w], v["voltage"][str(volts)][s], v["voltage"][str(volts)][sc])
								break
					else:
						if k == "weight":
							continue
						weight = WaS(v[w], v[s], v[sc])
					if k == "Dielectric_strength":
						self.breakdown_voltage = weight
					elif k == "Interfacial_tension":
						self.interfacial_tension = weight
					elif k == "Acidity":
						self.acidity = weight
					elif k == "Water_content":
						self.water_content = weight
					elif k == "Color":
						self.color = weight
					elif k == "Dissipation_factor":
						self.dissipation_factor = weight
					else:
						raise Exception

				self.got = WaS(self.config["Method 4"][w]["Oil_Quality"], val[w]["starts"], val[w]["scores"])
			elif key == "Furfural":

				self.fal = WaS(self.config["Method 4"][w]["Furfural"], val[w]["starts"], val[w]["scores"])
			elif key == "weight":
				continue
				 
			else:
				print("Unavailable key type: ", key)
				raise Exception
		
		self._reset_internal_scores()
		

	def _reset_internal_scores(self):
		self._prev_data_dga = []
		self._prev_result_dga, self._prev_score_dga = 0, 0
		self._prev_data_fal = 0 
		self._prev_score_fal = 0
		self._prev_data_got = []
		self._prev_result_got, self._prev_score_got = 0, 0

			
	def _mult_lists(self, lista, listb):
		res = [a*b for a,b in zip(lista, listb)]
		return res

	def _get_result(self, values, weights):
		n = self._mult_lists(values, weights)
		result = sum(n) / sum(weights)

		return result

	def _get_HI(self, values, weights):
		w = [i*4 for i in weights]
		n = self._mult_lists(values, weights)
		result = (sum(n) / sum(w)) * 100

		return result

	def calc_dga(self, data: Dissolved_Gases):
		values = [self.h2.get_score(data.h2), \
					self.ch4.get_score(data.ch4), \
					self.c2h6.get_score(data.c2h6), \
					self.c2h4.get_score(data.c2h4), \
					self.c2h2.get_score(data.c2h2), \
					self.co.get_score(data.co), \
					self.coh2.get_score(data.coh2)	]

		if self._prev_data_dga == values:
			return self._prev_result_dga, self._prev_score_dga

		self._prev_data_dga = values

		w = [self.h2.weight, self.ch4.weight, self.c2h6.weight, self.c2h4.weight, self.c2h2.weight, self.co.weight, self.coh2.weight]

		result = self._get_result(values, w)
		score = self.dga.get_score(result)

		self._prev_result_dga, self._prev_score_dga = result, score

		return result, score
	
	def calc_fal(self, data: Furfural):
		if self._prev_data_fal == data.quantity or isnan(data.quantity):
			return self._prev_score_fal
		
		self._prev_data_fal = data.quantity

		score = self.fal.get_score(data.quantity)
		
		self._prev_score_fal = score

		return score
		
	def calc_got(self, data: Oil_Quality):
		values = [self.breakdown_voltage.get_score(data.breakdown_voltage), \
					self.interfacial_tension.get_score(data.interfacial_tension), \
					self.acidity.get_score(data.acidity), \
					self.water_content.get_score(data.water_content), \
					self.color.get_score(data.color) ]

		if self._prev_data_got == values:
			return self._prev_result_got, self._prev_score_got

		self._prev_data_got = values

		w = [self.breakdown_voltage.weight, self.interfacial_tension.weight, self.acidity.weight, self.water_content.weight, self.color.weight]

		result = self._get_result(values, w)
		score = self.got.get_score(result)
		
		self._prev_result_got, self._prev_score_got = result, score

		return result, score

	def calc_HI(self, data):
		w = [0, 0, 0]
		if data[0] is None:
			dga_score = 0
		else:
			_, dga_score = self.calc_dga(data[0])
			w[0] = self.dga.weight
		
		if data[1] is None:
			fal_score = 0
		else:
			fal_score = self.calc_fal(data[1])
			w[1] = self.fal.weight

		if data[2] is None:
			got_score = 0
		else:
			_, got_score = self.calc_got(data[2])
			w[2] = self.got.weight

		health_index = self._get_HI([dga_score, fal_score, got_score], w)

		return health_index


def calculate_for_transformer(m : Method_4 , tr: Transformer):
	"""
	Returns a list of tupples with the datestamp and the respective result:
		[(datestamp, result), (datestamp, result), ...])
	"""
	queries = fetch_data(tr)
	if tr.nominal_voltage:
		m.update_method_weights(tr.nominal_voltage)
	else:
		return None

	oldest_events_queries, datestamp = get_next_chronological_envents(queries)
	data = [None, None, None]
	results = []
	prev_result = 0
	while oldest_events_queries: 			# Verifica se é uma lista vazia
		for q in oldest_events_queries:
			d = q.get_data()
			if isinstance(d, Dissolved_Gases):
				data[0] = d
			elif isinstance(d, Furfural):
				data[1] = d
			elif isinstance(d, Oil_Quality):
				data[2] = d
			else:
				continue

		result = m.calc_HI(data)
		if prev_result != result:
			results.append((datestamp,result))
			prev_result = result
		
		oldest_events_queries, datestamp = get_next_chronological_envents(queries)
	return results

def calculate_all_transformers(session):
	"""
	Returns a list of tupples with the following structure:
		[(transformer_id, [(datestamp, result), (datestamp, result), ...]),
		(transformer_id, [(datestamp, result), (datestamp, result), ...]),...]
	If a transformer as missing data, it doesn't append to the final result
	"""
	transfomer_list = session.query(Transformer)
	
	m = Method_4()
	results = []
	for tr in transfomer_list:
		result = calculate_for_transformer(m, tr)
		if result:
			results.append((tr.id_transformer, result))

		pass
	return results
