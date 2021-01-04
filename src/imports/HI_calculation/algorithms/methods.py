import json
import os

cwd = os.getcwd()
repo_name = 'SEAI---Equipa-F'
repo_dir = cwd[:cwd.rindex(repo_name) + len(repo_name)] # retira tudo depois de 'SEAI---Equipa-F'
weight_path = os.path.join(repo_dir,"src/imports/HI_calculation/weights.json")
with open(weight_path, "r") as file: 
	config = json.load(file)


class WS: # Weights and Scores
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

class Method:
	def __init__(self, method):
		self.config = config[method]
	
	def _mult_lists(self, lista, listb):
		res = [a*b for a,b in zip(lista, listb)]
		return res

	def calculate_for_transformer(self):
		pass

	def update_method_weights(self):
		pass

	def calc_HI(self):
		pass