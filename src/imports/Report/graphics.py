import os
from matplotlib import pyplot as plt


class Graphic:
	def __init__(self, path, name, save_graph : bool = False, ylim = None, **kwargs):
		self.name = name
		self.image_path = os.path.join(path, name + ".png")
		self.save_graph = save_graph
		markers = ['o', '^', '*', 'v', '1', 'H', 'p', '|']
		colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', "#ffcccb"]
		fig = plt.figure()
		i=0
		for key, val in kwargs.items():
			plt.plot(val[0], val[1], label = key.replace("_", " "), color = colors[i], marker = markers[i])
			i+=1

		if ylim: 
			axes = plt.gca()
			axes.set_ylim(ylim)

		plt.legend()
		
		path = self.image_path
		plt.savefig(path)
		plt.close(fig)
	
	def __del__(self):
		if not self.save_graph:
			os.remove(self.image_path)
	
	def get_image_path(self):
		return self.image_path