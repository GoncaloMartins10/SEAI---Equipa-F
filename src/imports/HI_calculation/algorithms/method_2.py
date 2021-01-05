from datetime import date
from math import isnan

from .methods import  WS, Method
from .fetch_data import fetch_data, get_next_chronological_envents, Queried_data
from ...resources.db_classes import *

class Method_2(Method):
	def __init__(self, transformer : Transformer = None):
		super().__init__("Method 2")

		if transformer:
			if transformer.nominal_voltage:
				self.update_method_weights(transformer.nominal_voltage)


	def update_method_weights(self, transformer_voltage):
		w = "weight"
		s = "starts"
		sc = "scores"

		for key, val in self.config.items():
			if key == "Dissolved_Gases":
				self.h2 = WS(val['h2'][w], val['h2'][s], val['h2'][sc]) 

				self.ch4 = WS(val['ch4'][w], val['ch4'][s], val['ch4'][sc])

				self.c2h6 = WS(val['c2h6'][w], val['c2h6'][s], val['c2h6'][sc])
				
				self.c2h4 = WS(val['c2h4'][w], val['c2h4'][s], val['c2h4'][sc])

				self.c2h2 = WS(val['c2h2'][w], val['c2h2'][s], val['c2h2'][sc])

				self.co = WS(val['co'][w], val['co'][s], val['co'][sc])

				self.coh2 = WS(val['coh2'][w], val['coh2'][s], val['coh2'][sc])


				self.dga = WS(self.config[w]["Dissolved_Gases"], val[w][s], val[w][sc])
			elif key == "Oil_Quality":
				if transformer_voltage is not None:
					for k, v in val.items():
						if "voltage" in v:
							rated_volts = list(map(int, list(v["voltage"].keys())))
							rated_volts.sort(reverse = True)
							for volts in rated_volts:
								if transformer_voltage >= volts:
									weight = WS(v[w], v["voltage"][str(volts)][s], v["voltage"][str(volts)][sc])
									break
						else:
							if k == "weight":
								continue
							weight = WS(v[w], v[s], v[sc])
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

				self.got = WS(self.config[w]["Oil_Quality"], val[w][s], val[w][sc])
			elif key == "Furfural":

				self.fal = WS(self.config[w]["Furfural"], val[w][s], val[w][sc])
			elif key == "Load":
				self.N_scores = WS(self.config[w]["Load"], val[w][s], val[w][sc])
				self.N_scale = val["N"]["scale"]
				continue
			elif key == "Maintenance":
				for k, v in val:
					if k == "Bushings":
						self.bushings = WS(v[w], val[s], v[sc])
					elif k == "Infra-red":
						self.infra_red = WS(v[w], val[s], v[sc])
					elif k == "Main tank":
						self.main_tank = WS(v[w], val[s], v[sc])
					elif k == "Cooling":
						self.cooling = WS(v[w], val[s], v[sc])
					elif k == "Oil Tank":
						self.oil_tank = WS(v[w], val[s], v[sc])
					elif k == "Foundation":
						self.foundation = WS(v[w], val[s], v[sc])
					elif k == "Grounding":
						self.grounding = WS(v[w], val[s], v[sc])
					elif k == "Gaskets":
						self.gaskets = WS(v[w], val[s], v[sc])
					elif k == "Connectors":
						self.connectors = WS(v[w], val[s], v[sc])
					elif k == "Oil leaks":
						self.oil_leaks = WS(v[w], val[s], v[sc])
					elif k == "Oil level":
						self.oil_level = WS(v[w], val[s], v[sc])
			elif key == "Power_Factor":
				self.power_factor = WS(self.config[w]["Power_Factor"], val[s], val[sc])
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
		self._prev_data_maint = []
		self._prev_score_maint = 0
		self._prev_data_load = []
		self._prev_score_load = 0
		self._N_count = [0, 0, 0, 0, 0]

	def _get_result(self, values, weights):
		n = self._mult_lists(values, weights)
		result = sum(n) / sum(values)

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
		if self._prev_data_fal == data.quantity:
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
		w = [0, 0, 0, 0, 0]
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


	def calculate_for_transformer(self, tr: Transformer):
		"""
		Returns a list of tupples with the datestamp and the respective result:
			[(datestamp, result), (datestamp, result), ...])
		"""
		queries = fetch_data(tr)
		

		oldest_events_queries, datestamp = get_next_chronological_envents(queries)
		data = [None, None, None, None, None]
		results = []
		prev_result = 0
		while oldest_events_queries: 			# Verifica se é uma lista vazia
			for q in oldest_events_queries:
				d = q.get_data()
				if isinstance(d, Dissolved_Gases):
					data[0] = d
				elif isinstance(d, Furfural):
					data[1] = d
				elif isinstance(d, Oil_Quality) and tr.nominal_voltage:
					data[2] = d
				elif isinstance(d, Load): # Load e power factor
					data[3] = d
				elif isinstance(d, Maintenance):
					data[4] = d
				else:
					continue

			result = self.calc_HI(data)
			if prev_result != result:
				results.append((datestamp,result))
				prev_result = result

			oldest_events_queries, datestamp = get_next_chronological_envents(queries)
		return results
