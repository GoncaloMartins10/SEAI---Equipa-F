import os
import time
import pandas as pd
import numpy as np

class Excel_extract:
	def __init__(self,file_path):
		self.file_path = file_path

	def __repr__(self):
		return f'Excel to {self.file_path}'

	def filter_DGA(self):
		df = pd.read_excel(self.file_path, sheet_name='DGA')
		df = df.iloc[:10,:]
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
				df_score.drop(df.columns[[j+0,j+1,j+5,j+7]], axis=1, inplace=True)

				if df_score.iloc[0,0] is np.nan: break

				df_DGAF_scores.append(df_score)

				df_rating = df.iloc[i+9,j:j+2] 
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
		df = df.iloc[:7,:]
		df.drop(df.columns[0], axis=1, inplace=True)
		df.drop(df.index[0], axis=0, inplace=True)

		return df

	def filter_Load(self):
		df = pd.read_excel(self.file_path, sheet_name='Load')
		
		LF = df.iloc[2,2]
		Sb = df.iloc[5,2]


		df_load_peak = df.iloc[1:,4:7]
		df_load_peak.dropna(axis=0, inplace=True) # Drops the rest of the nan values
		df_n_intances = df.iloc[2:7,12:14]

		# Tabela com o pico de fator de cargo mensal para todas as sub estações
		df_load_monthly_peak = df.iloc[:,21:33]
		df_load_monthly_peak.dropna(axis=0, how='all', inplace=True) # Drops the rest of the nan values
		df_load_monthly_peak.dropna(axis=1, how='all', inplace=True)
		# Tabela com dados incompletos
		# df = df.iloc[:,37:47]

		return df_load_monthly_peak, Sb, df_n_intances

	def filter_Maintenance(self):
		df = pd.read_excel(self.file_path, sheet_name='Maintenance')

		df_score_table = df.iloc[2:9,:11] 	# Tabela superior esquerda
		df_scores = df.iloc[13:,:12]		# Tabela inferior esquerda
		df_scores.dropna(axis=0, how='all', inplace=True)
		df_scores.dropna(axis=1, how='all', inplace=True)
		df_maintenances = df.iloc[0:,14:]	# Tabela direita
		df_maintenances.dropna(axis=0, how='all', inplace=True)
		df_maintenances.dropna(axis=1, how='all', inplace=True)

		return df_score_table, df_scores, df_maintenances

	def filter_OverallCondition(self):
		df = pd.read_excel(self.file_path, sheet_name='Overall Condition')

		df = df.iloc[10:,[0,2]]
		df.dropna(axis=0, how='all', inplace=True)

		# Deletes rows with incorrect assigned values
		df = df[df["Overall Condition"] != False] 
		return df

	def filter_event_score(self):
		"""
		Returns a dictionay with the event and the corresponding score
		"""
		df = pd.read_excel(self.file_path)
		df = df.iloc[5:,:3]
		df.dropna(axis=0, how='all', inplace=True)
		df.dropna(axis=1, how='all', inplace=True)

		score_dictionary = {}
		for _, key in df.iterrows():
			score_dictionary[key[1]] = key[2]

		return score_dictionary