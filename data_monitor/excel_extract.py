import os
import time
import pandas as pd
import numpy as np

class Excel_extract:
	def __init__(self,file_path):
		self.file_path = file_path

	def filter_DGA(self):
		df = pd.read_excel(self.file_path, sheet_name='DGA')
		df.drop(df.columns[[0,1,2]], axis=1, inplace=True)
		df.drop(df.index[0], axis=0, inplace=True)

		return df

	def filter_DGAF(self):
		df = pd.read_excel(self.file_path, sheet_name='DGAF')
		number_of_tables = len(df.index)

		df_DGAF_scores = []
		df_DGAF_ratings = []
		for j in range(0, 12, 11): # Para percorrer as tabelas na horizontal
			for i in range(0, number_of_tables, 15): # Para percorrer as tabelas na vertical
				df_score = df.iloc[i:i+7,j:j+9]
				df_score.drop(df.columns[[j+0,j+1,j+5,j+7]], axis=1, inplace=True) # É possível retirar este conteudo com o método de cima, mas preferi que ficasse explicito que largamos os nomes

				# Apenas para não inserir tabelas sem conteudo, um pouco trolha, só vê o primeiro valor da tabela
				if df_score.iloc[0,0] is np.nan: break

				df_DGAF_scores.append(df_score)

				df_rating = df.iloc[i+9,j:j+2] # Caso se queira usar a tabela com o rating (O naming do dataframe está mal)
				df_DGAF_ratings.append(df_rating)

		return df_DGAF_scores, df_DGAF_ratings

	def filter_FAL(self):
		df = pd.read_excel(self.file_path, sheet_name='2-FAL')
		df.drop(df.columns[4:], axis=1, inplace=True)
		df.drop(df.index[[0,1]], axis=0, inplace=True)

		return df

	def filter_PF(self):
		df = pd.read_excel(self.file_path, sheet_name='PF')
		df.drop(df.columns[2:], axis=1, inplace=True)

		df_rating = df.iloc[2,:2]
		df_samples = df.iloc[5:,:2]

		return df_samples, df_rating

	def filter_GOT(self):
		df = pd.read_excel(self.file_path, sheet_name='GOT')
		df.drop(df.columns[0], axis=1, inplace=True)
		df.drop(df.index[0], axis=0, inplace=True)

		return df

	def filter_OQF(self):
		df = pd.read_excel(self.file_path, sheet_name='OQF')
		number_of_tables = len(df.index)

		df_array = []
		for j in range(0, 12, 11): # Para percorrer as tabelas na horizontal
			for i in range(0, number_of_tables, 9): # Para percorrer as tabelas na vertical
				df_aux = df.iloc[i:i+7,j:j+9]
				df_aux.drop(df.columns[[j+0,j+1,j+5,j+7]], axis=1, inplace=True) # É possível retirar este conteudo com o método de cima, mas preferi que ficasse explicito que largamos os nomes

				# Apenas para não inserir tabelas sem conteudo, um pouco trolha, só vê o primeiro valor da tabela
				if df_aux.iloc[0,0] is np.nan: break

				df_array.append(df_aux)

		raise NotImplementedError
		return df_array

	def filter_Load(self):
		# Falta implementar as outras tabelas, mas não sei o que elas são
		df = pd.read_excel(self.file_path, sheet_name='Load')
		
		LF = df.iloc[2,2]
		Sb = df.iloc[5,2]


		df_load_peak = df.iloc[1:,4:7]
		df_load_peak.dropna(axis=0, inplace=True) # Drops the rest of the nan values
		df_n_intances = df.iloc[2:7,12:14]

		# Tabelas desconhecidas
		df_desconhecida_1 = df.iloc[:,21:33]
		df_desconhecida_1.dropna(axis=0, how='all', inplace=True) # Drops the rest of the nan values
		df_desconhecida_2 = df.iloc[:,37:47]

		return df_load_peak, df_n_intances


	def filter_Maintenance(self):
		df = pd.read_excel(self.file_path, sheet_name='Maintenance')

		df_rating_table = df.iloc[2:9,:11] 	# Tabela superior esquerda
		df_ratings = df.iloc[13:,:12]		# Tabela inferior esquerda
		df_maintenances = df.iloc[7:,17:]	# Tabela direita

		return df_rating_table, df_ratings, df_maintenances

	def filter_OverallCondition(self):
		raise NotImplementedError

	def filter_FinalCalculation(self):
		raise NotImplementedError

if __name__ == "__main__":	
	
	ee = Excel_extract(r'dados/Template SE1.xlsx')
	# df_DGA = filter_DGA()
	# df_DGAF,_ = ee.filter_DGAF() # O _ serve para ignorar o segundo retorno da função
	# df = filter_FAL()
	# df_s, df_r = filter_PF()
	# df = filter_GOT()

	df1, _ = ee.filter_Load()

	print (df1)