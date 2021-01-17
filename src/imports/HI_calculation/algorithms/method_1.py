import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression

from .methods import  WS, Method
from .fetch_data import fetch_data, get_next_chronological_envents, Queried_data, get_oldest_date
from ...resources.db_classes import Transformer, Dissolved_Gases, Oil_Quality, Furfural, Load, Health_Index, Maintenance
from .method_2 import Method_2
from .method_4 import Method_4
from datetime import datetime, time
from dateutil.relativedelta import relativedelta



class Method_1(Method):
	def __init__(self):
		super().__init__("method_1")

		self.high = self.config["high"]
		self.med = self.config["med"]
		self.low = self.config["low"]
	
	
	def metodo(self, data):
	# Inputs Normalizados
		weights = [self.high, self.high, self.med, self.low]

		# Calcular HI para cada para (idade, dados)
		measurements = list(zip(data['oqf'], data['dgaf'], data['water_content'], data['impact_index']))
		HI = [sum(self._mult_lists(weights, m)) for m in measurements]

		# Regression
			# List -> array
		ageReg = np.reshape(data['age'], (-1, 1))
		HIReg = np.reshape(HI, (-1, 1))
		# O que acontece a partir daqui?
		reg = LinearRegression(fit_intercept=False).fit(ageReg, HIReg)
		a=reg.predict([[1]]).reshape(-1) 	  	# Declive da Reta
		bupp=a*15                          		  # Limite Superior (+15 anos)
		blow=a*(-10)                            # Limite Inferior  (-10 anos)

		dist= HIReg - reg.predict(ageReg)
		distMax=np.max(dist)
		distMin=np.min(dist)

		# Correcao HI
		nrMeasures = len(data['age'])                #numero de medicoes do transformer (Age pode servir)
		distshrunk=np.zeros(nrMeasures)
		if distMax>bupp or distMin<blow:
			for i, d in np.ndenumerate(dist):
				if d>0 and distMax>bupp:
					distshrunk[sum(i)]=(d/distMax)*bupp
				if d<0 and distMin<blow:
					distshrunk[sum(i)]=(d/-distMin)*-blow

		# Computation HI and Apparent Age        
		HIcorrected=reg.predict(ageReg).reshape(-1)+distshrunk
		appage=HIcorrected/a
		
		return HIcorrected[-1] #Only the most recent measure matters
	

	def norm_data(self, data):
		data['dgaf'] = [(1-i/4) for i in data['dgaf'] ]
		data['oqf'] = [(1-i/4) for i in data['oqf'] ]
		data['water_content'] = [((i-1)/3) for i in data['water_content'] ]
		data['impact_index'] = [((2-i)/4) for i in data['impact_index']]
		return data


	def update_stuffed_data(self, stuffed_data, key, value, current_age):
		if not stuffed_data['age']:
			stuffed_data
		if stuffed_data['age'][-1] == current_age:
			stuffed_data[key][-1] = value
		else:
			stuffed_data[key].append(value)
			stuffed_data['age'].append(current_age)
			for key_i, value_i in stuffed_data:
				if (key_i!=key) and (key_i!='age'):
					value_i.append(value_i[-1])

	def calculate_for_transformer(self, tr: Transformer):
		"""
		Returns a list of tupples with the datestamp and the respective result:
			[(datestamp, result), (datestamp, result), ...])
		"""
		classes_to_query = [Maintenance, Dissolved_Gases, Oil_Quality]
		queries = fetch_data(tr, classes_to_query)

		oldest_events_queries, datestamp = get_next_chronological_envents(queries)
		first_measurement_done = datetime.combine(datestamp, time())
		stuffed_data = {
			'age': [], 
			'dgaf': [],
			'oqf': [],
			'water_content': [],
			'impact_index': []
		}
		results = []
		prev_result = 0
		
		m4 = Method_4()
		m4.update_method_weights(tr.nominal_voltage)
		iter_num = 0
		while oldest_events_queries: 			# Verifica se é uma lista vazia
			# este primeiro ciclo serve para irmos buscar os proximos dados para calcularmos o indice de saude para este algoritmo
			for q in oldest_events_queries:
				d = q.get_data()
				current_date = datetime.combine(q.get_date(), time())				
				current_age = relativedelta(current_date, first_measurement_done).years

				if isinstance(d, Dissolved_Gases):
					new_value = m4.calc_dga(d)[1]
					# Nao termos valores numa das listas
					if [] in list(stuffed_data.values()): 
						stuffed_data['dgaf'] = [new_value]
						stuffed_data['age'] = [current_age]
					# Ultima idade inserida ser a mesma que esta medição
					elif stuffed_data['age'][-1] == current_age:
						stuffed_data['dgaf'][-1] = new_value
					# Ser uma medição cuja idade ainda nao esta considerada
					else:
						stuffed_data['dgaf'].append(new_value)
						stuffed_data['age'].append(current_age)
						for key, list_object in stuffed_data.items():
							if key not in ('dgaf', 'age'):
								list_object.append(list_object[-1])

				elif isinstance(d, Oil_Quality):
					new_value_oqf = m4.calc_got(d)[1]
					new_value_water_content = m4.water_content.get_score(d.water_content)
					# Nao termos valores numa das listas
					if [] in list(stuffed_data.values()): 
						stuffed_data['oqf'] = [new_value_oqf]
						stuffed_data['water_content'] = [new_value_water_content]
						stuffed_data['age'] = [current_age]
					# Ultima idade inserida ser a mesma que esta medição
					elif stuffed_data['age'][-1] == current_age:
						stuffed_data['oqf'][-1] = new_value_oqf
						stuffed_data['water_content'][-1] = new_value_water_content
					# Ser uma medição cuja idade ainda nao esta considerada
					else:
						stuffed_data['oqf'].append(new_value_oqf)
						stuffed_data['water_content'].append(new_value_water_content)
						stuffed_data['age'].append(current_age)
						for key, list_object in stuffed_data.items():
							if key not in ('oqf', 'water_content', 'age'):
								list_object.append(list_object[-1])

				elif isinstance(d, Maintenance):
					new_value = d.impact_index
					# Nao termos valores numa das listas
					if [] in list(stuffed_data.values()): 
						stuffed_data['impact_index'] = [new_value]
						stuffed_data['age'] = [current_age]
					# Ultima idade inserida ser a mesma que esta medição
					elif stuffed_data['age'][-1] == current_age:
						stuffed_data['impact_index'][-1] = new_value
					# Ser uma medição cuja idade ainda nao esta considerada
					else:
						stuffed_data['impact_index'].append(new_value)
						stuffed_data['age'].append(current_age)
						for key, list_object in stuffed_data.items():
							if key not in ('impact_index', 'age'):
								list_object.append(list_object[-1])
				else:
					continue

			# skips calculating HI if any of the lists is empty
			if [] in stuffed_data.values():
				oldest_events_queries, datestamp = get_next_chronological_envents(queries)
				iter_num += 1
				continue

			# normalizing the data between 0 and 1
			stuffed_normalized = self.norm_data(dict(stuffed_data))
			result = self.metodo(stuffed_normalized)

			# este segmento é para normalizar entre 0 a 100 o indice de saude
			result = [0, (result/50)*100, 100][  (result<=0)*0 
											   + (0<result<50)*1 
											   + (result>=50)*2]

			results.append(Health_Index(id_transformer=tr.id_transformer, id_algorithm=1, datestamp=datestamp, hi=result))
			oldest_events_queries, datestamp = get_next_chronological_envents(queries)
			iter_num += 1


		return results


