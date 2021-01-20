import os
from datetime import date
import re

from .template import Report
from .graphics import Graphic

from ..resources.db_classes import *
from ..resources.Mixins import MixinsTables
from ..resources import Session
from ..HI_calculation.algorithms.fetch_data import fetch_data

classes_to_query = [Dissolved_Gases, Furfural, Oil_Quality, Load, Maintenance_Scores, Overall_Condition, Health_Index]

def _get_health_index(hi):
	result = {}
	for item in hi:
		key_name = "Algorithm " + str(item.id_algorithm)
		if key_name not in result:
			result[key_name] = [[],[]]
			
		if item.datestamp not in result[key_name][0]:
			result[key_name][0].append(item.datestamp)
			result[key_name][1].append(item.hi)

	for f in result:
		result[f][0].append(date.today())
		result[f][1].append(result[f][1][-1])

	return result

def generate_report(transformer : Transformer, data : dict):

	cwd = os.getcwd()
	repo_name = 'SEAI---Equipa-F'
	repo_dir = cwd[:cwd.rindex(repo_name) + len(repo_name)] # retira tudo depois de 'SEAI---Equipa-F'
	static_parent_path = os.path.join(repo_dir,"static")
	
	del repo_dir, repo_name

	path_to_images = os.path.join(static_parent_path, "images")
	path_to_docs = os.path.join(static_parent_path, "doc")

	data["Health Index"] = _get_health_index(data["Health Index"])

	r = Report(transformer.id_transformer, path_to_docs)
	r.add_spacer(28)

	r.add_normal(f"Transformer's age: {transformer.age}")
	r.add_spacer(28)

	for chapter, attribute in data.items():
		r.add_subtitle(chapter)
		r.add_spacer(15)
		
		x=[]
		data_for_chapter_graphs = {}
		if chapter == "Health Index":
			limits = (0, 100)
			for d in attribute:
				data_for_chapter_graphs[d] = attribute[d]
		else:
			limits = None
			for d in attribute:
				a = d.__dict__
				for name, prop in a.items():
					if re.search(r"id_|^_", name):
						continue
					elif name == "datestamp":
						x.append(prop)
					else:
						if name in data_for_chapter_graphs:
							data_for_chapter_graphs[name].append(prop)
						else:
							data_for_chapter_graphs[name] = [prop]
		
			for k in data_for_chapter_graphs:
				data_for_chapter_graphs[k] = [x, data_for_chapter_graphs[k]]

		data_for_graph = {}
		removed_keys = []
		i = 0
		count = 0
		
		while len(data_for_chapter_graphs) > 0:
			diff = []
			for k, val in data_for_chapter_graphs.items():
				difference = max(val[1]) - min(val[1])
				if diff and chapter != "Health Index":
					if difference < max(diff) * 0.5 or difference > min(diff) * 2:
						continue
				data_for_graph[k] = val
				removed_keys.append(k)
				
				diff.append(difference)
				i+=1
				if i == 5:
					break
					
			[data_for_chapter_graphs.pop(i, None) for i in removed_keys]
			removed_keys = []
			i=0


			if count == 0: graph_name = chapter
			else: graph_name = chapter + " (" + str(count) + ")"
			
			f = Graphic(path_to_images, graph_name, True, limits, **data_for_graph)
			caption_string = ", ".join(data_for_graph.keys()).replace("_", " ")
			r.add_graph(f, f"Graphic with {caption_string}")
			
			if count%2 or not len(data_for_chapter_graphs):
				r.flush_graphs_to_row()

			data_for_graph = {}
			count += 1
		
		r.add_spacer(25)
		
	return


def _get_data_as_list(query):
		data_list = []
		for i in range(query.count()):
			data_list.append(query[i])
		return data_list

def get_data_for_report(transformer : Transformer):

	data = {}

	queries = fetch_data(transformer, classes_to_query)	
	for q in queries:
		d = q.get_data_as_list()

		if isinstance(d[0], Dissolved_Gases):
			data["Dissolved Gases"] = d
		elif isinstance(d[0], Furfural):
			data["Furfural"] = d
		elif isinstance(d[0], Oil_Quality):
			data["Oil Quality"] = d
		elif isinstance(d[0], Load): # Load e power factor
			data["Load and Power Factor"] = d
		elif isinstance(d[0], Maintenance_Scores):
			data["Maintenance Scores"] = d
		elif isinstance(d[0], Overall_Condition):
			data["Overall Condition"] = d
		elif isinstance(d[0], Health_Index):
			data["Health Index"] = d

	return data


def generate_all_reports():
	session = Session()

	transfomer_list = session.query(Transformer)
	session.close()

	transformer_data = {}
	
	for tr in transfomer_list:
		data = get_data_for_report(tr)
		transformer_data[tr] = data

	
	del transfomer_list, data, session

	for tr, data in transformer_data.items():
		generate_report(tr, data)
