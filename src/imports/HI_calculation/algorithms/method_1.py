import numpy as np
from sklearn.linear_model import LinearRegression

from .methods import  WS, Method
from .fetch_data import fetch_data, get_next_chronological_envents, Queried_data, get_oldest_date
from ...resources.db_classes import Transformer, Dissolved_Gases, Oil_Quality, Furfural, Load, Health_Index, Maintenance
from .method_2 import Method_2

class Method_1(Method):
	def __init__(self):
		super().__init__("method_1")

		self.high = self.config["high"]
		self.med = self.config["med"]
		self.low = self.config["low"]

	def metodo(self, data):
		'''
			1- Normalizar entre 0 e 1 
				- DGA - [1.2; 3]
				- OQF - Obter Final Rating -> Inverter classficação 0->1 e 5->0
				- Water Content
				- Dados Maintenance (Gasket, Bushings)
			
			2 - Obter idade 
				Current date - oldest date
			
			3 - Aplicar Hidro Quebec 
					HI = weights . param
		'''
		# Inputs (adaptar com a variavel passada ao metodo)
		age = [10, 11, 12, 13]
		param = [1,0.3,0.4,0]  #Dados têm que estar normaliados [0,1]
		weights = [self.high, self.high, self.med, self.low]

		# Calcular HI para cada para (idade, dados)
		HI = self._mult_lists(weights, param)

		# Regression
			# List -> array
		ageReg = np.reshape(age, (-1, 1))
		HIReg = np.reshape(HI, (-1, 1))
		reg = LinearRegression(fit_intercept=False).fit(ageReg, HIReg)
		a=reg.predict([[1]]).reshape(-1)	# Declive da Reta
		bupp=a*15							# Limite Superior (+15 anos)
		blow=a*-10							# Limite Inferior  (-10 anos)

		dist=HI-reg.predict(ageReg).reshape(-1)
		distMax=np.max(dist)
		distMin=np.min(dist)

		# Correcao HI
		nrMeasures = len(age)				#numero de medicoes do transformer (Age pode servir)
		distshrunk=np.zeros(nrMeasures)
		if distMax>bupp or distMin<blow:
			for i, d in np.ndenumerate(dist):
				if d>0 and distMax>bupp:
					distshrunk[i]=(d/distMax)*bupp
				if d<0 and distMin<blow:
					distshrunk[i]=(d/-distMin)*-blow

		# Computation HI and Apparent Age		
		HIcorrected=reg.predict(ageReg).reshape(-1)+distshrunk
		appage=HIcorrected/a
		
		return HIcorrected[-1] #Only the most recent measure matters

	def calculate_for_transformer(self, tr: Transformer):
		"""
		Returns a list of tupples with the datestamp and the respective result:
			[(datestamp, result), (datestamp, result), ...])
		"""
		classes_to_query = [Maintenance, Dissolved_Gases, Furfural, Oil_Quality, Load]
		queries = fetch_data(tr, classes_to_query)

		oldest_events_queries, datestamp = get_next_chronological_envents(queries)
		data = [None, None, None, None, None]
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
				elif isinstance(d, Maintenance):
					data[4] = d
				else:
					continue


			result = self.metodo(data)


			if prev_result != result:
				results.append( Health_Index(id_transformer = tr.id_transformer, id_algorithm = 3, datestamp = datestamp, hi = result))
				prev_result = result
			
			oldest_events_queries, datestamp = get_next_chronological_envents(queries)
		return results


