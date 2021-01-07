import inspect
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

	def __repr__(self):
		return f'Method 2'

	def update_method_weights(self, transformer_voltage):
		w = "weight"
		s = "starts"
		sc = "scores"

		maintenance_parameters = ["Bushings", "Infra-red", "Main tank", "Cooling", "Oil tank", "Foundation", \
									"Grounding", "Gaskets", "Connectors", "Oil leaks", "Oil level"]

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
				self.load = WS(self.config[w]["Load"], val[s], val[sc])
				self.N_scale = val["N"]["scale"]
				continue
			elif key == "Maintenance":

				self.maint = {}
				for k, v in val.items():
					if k in maintenance_parameters:
						l = k.replace(" ", "_").replace("-", "_").lower()
						self.maint[l] = WS(v[w], val[s], v[sc])
					elif k == "starts":
						continue
					else:
						raise Exception(f"Wrong attribute {k}")
					"""
				self.maint = [temp_maint["bushings"], \
								temp_maint["infra_red"], \
								temp_maint["cooling"], \
								temp_maint["main_tank"], \
								temp_maint["oil_tank"], \
								temp_maint["foundation"], \
								temp_maint["grounding"], \
								temp_maint["gaskets"], \
								temp_maint["connectors"], \
								temp_maint["oil_leaks"], \
								temp_maint["oil_level"]]
								"""
			elif key == "Power_Factor":
				self.power_factor = WS(self.config[w]["Power_Factor"], val[w][s], val[w][sc])
			elif key == "weight":
				self.overall_weight = val["Overall_Condition"]
				 
			else:
				print("Unavailable key type: ", key)
				raise Exception
		
		self._reset_internal_scores()

	def _reset_internal_scores(self):
		self._prev_data_dga = None
		self._prev_result_dga, self._prev_score_dga = 0, 0
		self._prev_data_fal = 0 
		self._prev_score_fal = 0
		self._prev_data_got = None
		self._prev_result_got, self._prev_score_got = 0, 0
		self._prev_data_maint = None
		self._prev_score_maint = []
		self._prev_weight_maint = []
		self._prev_data_load = None
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

	def calc_load(self, data: Load):
		for i, n in enumerate(self.N_scale):
			if data.load_factor < n or i == len(self.N_scale) - 1:
				self._N_count[i - 1] += 1
				break
		
		lf = sum([(4-i)*n for i, n in reversed(list(enumerate(self._N_count)))]) / sum(self._N_count)

		res_load = self.load.get_score(lf)

		res_power = self.power_factor.get_score(data.power_factor)

		return res_load, res_power

	def calc_overall(self, data: Overall_Condition):
		return data.score

	def calc_maint(self, data: Maintenance_Scores):
		if self._prev_data_maint == data:
			return self._prev_score_maint, self._prev_weight_maint
		self._prev_data_maint = data
		scores = []
		w = []
		for m in self.maint.keys() & data.__dict__.keys():
			scores.append(data.__dict__[m])
			w.append(self.maint[m].weight)
		
		self._prev_score_maint = scores
		self._prev_weight_maint = w
		return scores, w

	def calc_HI(self, data):
		w = [0, 0, 0, 0, 0, 0]
		values = [0, 0, 0, 0, 0, 0]
		if data[0] is not None:
			_, values[0] = self.calc_dga(data[0])
			w[0] = self.dga.weight
		
		if data[1] is not None:
			values[1] = self.calc_fal(data[1])
			w[1] = self.fal.weight

		if data[2] is not None:
			_, values[2] = self.calc_got(data[2])
			w[2] = self.got.weight
		
		if data[3] is not None:
			values[3], values[4] = self.calc_load(data[3])
			w[3], w[4] = self.load.weight, self.power_factor.weight
		
		if data[4] is not None:
			values[5] = self.calc_overall(data[4])
			w[5] = self.overall_weight 								

		if data[5] is not None:
			scores, maint_w = self.calc_maint(data[5])
			values.extend(scores)
			w.extend(maint_w)

		health_index = self._get_HI(values, w)

		return health_index


	def calculate_for_transformer(self, tr: Transformer):
		"""
		Returns a list of tupples with the datestamp and the respective result:
			[(datestamp, result), (datestamp, result), ...])
		"""
		classes_to_query = [Dissolved_Gases, Furfural, Oil_Quality, Load, Maintenance_Scores, Overall_Condition]
		queries = fetch_data(tr, classes_to_query)
		
		self.update_method_weights(tr.nominal_voltage)

		oldest_events_queries, datestamp = get_next_chronological_envents(queries)
		data = [None, None, None, None, None, None]
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
				elif isinstance(d, Overall_Condition):
					data[4] = d
				elif isinstance(d, Maintenance_Scores):
					data[5] = d

			
			result = self.calc_HI(data)
			if prev_result != result:
				results.append( Health_Index(id_transformer = tr.id_transformer, id_algorithm = 2, datestamp = datestamp, hi = result))
				prev_result = result
			

			oldest_events_queries, datestamp = get_next_chronological_envents(queries)
		return results
