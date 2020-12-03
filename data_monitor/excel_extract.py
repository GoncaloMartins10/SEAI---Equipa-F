import os
import time
import pandas as pd
import numpy as np

def filter_DGA(file_path):
	df = pd.read_excel(file_path, sheet_name='DGA')
	df.drop(df.columns[[0,1,2]], axis=1, inplace=True)
	df.drop(df.index[0], axis=0, inplace=True)
	
	return df


def filter_DGAF(file_path):
	df = pd.read_excel(file_path, sheet_name='DGAF')
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

if __name__ == "__main__":	
	df_DGA = filter_DGA(r'dados/Template SE1.xlsx')
	df_DGAF,_ = filter_DGAF(r'dados/Template SE1.xlsx') # O _ serve para ignorar o segundo retorno da função