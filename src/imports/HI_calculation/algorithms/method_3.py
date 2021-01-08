import numpy as np
import math
import json
import os

from .methods import  WS, Method
from .fetch_data import fetch_data, get_next_chronological_envents, Queried_data, get_oldest_date
from ...resources.db_classes import Transformer, Dissolved_Gases, Oil_Quality, Furfural, Load, Health_Index


class MultiFeatureIndex(Method):
	def __init__(self):
		super().__init__("method_3")

		self.pesos_main = self.config["main"]
		self.pesos_iso= self.config["pesos_iso"]
		self.pesos_dga = self.config["pesos_DGA"]
		self.pesos_oil = self.config["pesos_oil"]
		self.pesos_combinado = self.config["pesos_combinado"]

		#self.caluculate_indexes()
	

	def caluculate_indexes(self, data, oldest_date):
		
		if data[3] is None:
			self.hi_main = 0
		else:
			self.hi_main= self.get_main(data[3], oldest_date)

		if data[0] is None or data[1] is None:
			self.hi_iso = 0
		else:
			self.hi_iso = self.get_iso(data[0], data[1])
		
		if data[0] is None:
			self.hi_dga = 0
		else:
			self.hi_dga = self.get_dga(data[0])

		if data[2] is None:
			self.hi_oil = 0
		else:
			self.hi_oil = self.get_oil(data[2])

		HI_combinado = self.get_combinado(self.hi_main, self.hi_iso, self.hi_dga, self.hi_oil)

		return HI_combinado 

	def get_combinado(self, hi_main, hi_iso, hi_dga, hi_oil):
		w=[self.pesos_combinado["HI_m"], self.pesos_combinado["HI_iso"], self.pesos_combinado["HI_CH"], self.pesos_combinado["HI_oil"]]

		HI=[            # Funções dos índices
			hi_main,
			hi_iso,
			hi_dga,
			hi_oil
		]
		# Calcular somatório
		HI_com = self._mult_lists(w, HI)
		return sum(HI_com)
	
	
	def get_main(self, data: Load, oldest_date):
		HI0 = self.pesos_main["HI0"]
		t_exp = self.pesos_main["t_exp"]
		f_L = data.load_factor    

		#T1 ano da primeira instância
		T1 = oldest_date.year
		#T2 ano da instância atual
		T2 = data.datestamp.year

		B = f_L * (np.log(6.5/0.5) / t_exp)     # Coeficiente de envelhecimento
		HI_m = HI0 * math.exp(B * (T2 - T1))
		return HI_m

	def get_iso(self, data_dg: Dissolved_Gases, data_f: Furfural ): 
		w_F_CO = self.pesos_iso['CO']

		
		x_CO = data_dg.co

		# Inicializar Fator Oxigénio-Carbono
		a = [0.0067, 0.0017, 0.02, 0.0125, 0]		
		b = [0, 1.5, -14.97, -7.5, 0]

		#cond = [x_CO range(0,300), x_CO range(300,900), x_CO range(900, 1000), x_CO range(1000, 1400), x_CO 1400]

		if 0 < x_CO <= 300 :
			F_CO = a[0] * x_CO + b[0]
		elif 300 < x_CO <= 900 :
			F_CO = a[1] * x_CO + b[1]
		elif 900 < x_CO <= 1000 :
			F_CO = a[2] * x_CO + b[2]
		elif 1000 < x_CO <= 1400 :
			F_CO = a[3] * x_CO + b[3]
		elif x_CO > 1400 :
			F_CO = 10


		HI_CO = F_CO

		
		C_fur = data_f.quantity
		# Calcular o indíce HI_C,O
		
		HI_fur = 3.344 * C_fur**0.413   # Calcular HI_fur

		w1 = 0.3
		w2 = 0.7
		HI_iso = w1 * HI_CO + w2 * HI_fur
		return HI_iso

	def get_dga(self, data: Dissolved_Gases):
	  
		w_CH = [self.pesos_dga["H2"], self.pesos_dga["CH4"], self.pesos_dga["C2H6"], self.pesos_dga["C2H4"], self.pesos_dga["C2H2"]]
		x_CH = [data.h2, data.ch4, data.c2h6, data.c2h4, data.c2h2]
		F_CH = [None, None, None, None, None]

		# Calcular F_C,H dos diferentes gases consoante o seu conteúdo (uL/L)
		# H2
		if x_CH[0] <= 30:               
			F_CH[0] = 0
		elif 30 < x_CH[0] <= 50:
			F_CH[0] = 0.1*x_CH[0] - 3 
		elif 50 < x_CH[0] <= 100:
			F_CH[0] = 0.06*x_CH[0] + 1
		elif 100 < x_CH[0] <= 500:
			F_CH[0] = 0.0125*x_CH[0] + 3.75
		else:
			F_CH[0] = 10
		
		# CH4
		if x_CH[1] <= 10:               
			F_CH[1] = 0
		elif 10 < x_CH[1] <= 15:
			F_CH[1] = 0.4*x_CH[1] - 2 
		elif 15 < x_CH[1] <= 115:
			F_CH[1] = 0.0727*x_CH[1] + 0.9
		else:
			F_CH[1] = 10

		# C2H6
		if x_CH[2] <= 5:               
			F_CH[2] = 0
		elif 5 < x_CH[2] <= 20:
			F_CH[2] = 0.1333*x_CH[2] - 0.6667 
		elif 20 < x_CH[2] <= 35:
			F_CH[2] = 0.2*x_CH[2] - 2
		elif 35 < x_CH[2] <= 70:
			F_CH[2] = 0.125*x_CH[2] + 0.625
		else:
			F_CH[2] = 10
		
		# C2H4
		if x_CH[3] <= 10:               
			F_CH[3] = 0
		elif 10 < x_CH[3] <= 30:
			F_CH[3] = 0.1*x_CH[3] - 1
		elif 30 < x_CH[3] <= 50:
			F_CH[3] = 0.15*x_CH[3] - 2.5
		elif 50 < x_CH[3] <= 175:
			F_CH[3] = 0.04*x_CH[3] + 3
		else:
			F_CH[3] = 10

		# C2H2
		if x_CH[4] <= 0.5:               
			F_CH[4] = 0
		elif 0.5 < x_CH[4] <= 3:
			F_CH[4] = 0.8*x_CH[4] - 0.4
		elif 3 < x_CH[4] <= 5:
			F_CH[4] = 1.5*x_CH[4] - 2.5
		elif 5 < x_CH[4] <= 35:
			F_CH[4] = 0.1667*x_CH[4] + 4.167
		else:
			F_CH[4] = 10

		HI_CH = self._mult_lists(F_CH, w_CH)

		return sum(HI_CH)

	def get_oil(self, data: Oil_Quality):
		w_oil = [self.pesos_oil["mw"], self.pesos_oil["av"], self.pesos_oil["bv"]]
		F_oil = [None, None, None]

		# Fatores que influenciam a qualidade do óleo | VALORES ALTERÁVEIS
		mw = data.water_content             	 # Micro-Water (mg/L)
		av = data.acidity            			 # Acid Value (mgKOH/g)
		# dl = data.            					 # Dielectric Loss (25ºC)  Não temos este valor 
		bv = data.breakdown_voltage             # Breakdown Voltage (kV)

		# Calcular fatores de qualidade
		# Micro-Water
		if mw <= 20:
			F_oil[0] = 0
		elif 20 < mw <= 30:
			F_oil[0] = 0.2*mw - 4
		elif 30 < mw <= 45:
			F_oil[0] = 0.4*mw - 10
		else:
			F_oil[0] = 10

		# Acid Value
		if av <= 0.015:
			F_oil[1] = 0
		elif 0.015 < av <= 0.1:
			F_oil[1] = 23.53*av - 0.353
		elif 0.1 < av <= 0.2:
			F_oil[1] = 20*av 
		elif 0.2 < av <= 0.3:
			F_oil[1] = 40*av - 4
		else:
			F_oil[1] = 10

		 # Dielectric Loss
		# if dl <= 0.005:
		#     F_oil[2] = 0
		# elif 0.005 < dl <= 0.015:
		#     F_oil[2] = 20*dl - 1
		# elif 0.015 < dl <= 0.5:
		#     F_oil[2] = 5.714*dl + 1.143
		# elif 0.5 < dl <= 1.5:
		#     F_oil[2] = 4*dl + 2
		# else:
		#     F_oil[2] = 10
		
		# Breakdown Voltage
		if bv <= 30:
			F_oil[2] = 10
		elif 30 < bv <= 40:
			F_oil[2] = -0.4*bv + 20
		elif 40 < bv <= 43:
			F_oil[2] = -0.664*bv + 30.68
		elif 43 < bv <= 45:
			F_oil[2] = -1*bv + 45
		else:
			F_oil[2] = 0
		
		# Calcular índice
		HI_oil = self._mult_lists(w_oil, F_oil)

		return sum(HI_oil)




	def calculate_for_transformer(self, tr: Transformer):
		"""
		Returns a list of tupples with the datestamp and the respective result:
			[(datestamp, result), (datestamp, result), ...])
		"""
		classes_to_query = [Dissolved_Gases, Furfural, Oil_Quality, Load]
		queries = fetch_data(tr, classes_to_query)

		oldest_date = get_oldest_date(queries)

		oldest_events_queries, datestamp = get_next_chronological_envents(queries)
		data = [None, None, None, None]
		results = []
		prev_result = 0
		
		while oldest_events_queries: 			# Verifica se é uma lista vazia
			for q in oldest_events_queries:
				d = q.get_data()
				print(type(d),isinstance(d, Load))
				if isinstance(d, Dissolved_Gases):
					data[0] = d
				elif isinstance(d, Furfural):
					data[1] = d
				elif isinstance(d, Oil_Quality):
					data[2] = d     
				elif isinstance(d, Load):
					data[3] = d
				else:
					continue

			
			result = self.caluculate_indexes(data, oldest_date)


			if prev_result != result:
				results.append( Health_Index(id_transformer = tr.id_transformer, id_algorithm = 3, datestamp = datestamp, hi = result))
				prev_result = result
			
			oldest_events_queries, datestamp = get_next_chronological_envents(queries)
		return results


	




