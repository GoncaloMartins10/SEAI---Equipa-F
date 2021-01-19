import os
from datetime import date
import re

from .template import Report
from .graphics import Graphic

from ..resources.db_classes import *
from ..resources.Mixins import MixinsTables
from ..resources import Session
from ..HI_calculation.algorithms.fetch_data import fetch_data

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
		# https://stackoverflow.com/questions/47907268/how-do-i-pass-a-string-as-an-argument-name
		while len(data_for_chapter_graphs) > 0:
			for k, val in data_for_chapter_graphs.items():
				data_for_graph[k] = val
				removed_keys.append(k)
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

def generate_all_reports():
	session = Session()

	transfomer_list = session.query(Transformer)
	session.close()

	classes_to_query = [Dissolved_Gases, Furfural, Oil_Quality, Load, Maintenance_Scores, Overall_Condition, Health_Index]

	transformer_data = {}
	data = {}
	queries = []
	for tr in transfomer_list:
	
		queries = fetch_data(tr, classes_to_query)	
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

		transformer_data[tr] = data
		data = {}

	
	del transfomer_list, q, d, data, queries, session, classes_to_query, tr

	for tr, data in transformer_data.items():
		generate_report(tr, data)

if __name__ == "__main__":
	test = True

	logo = "images/color.jpg"
	lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, \
			sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

	if test:
		r = Report("SE1")
		r.add_spacer(28)
		r.add_graph_to_table(logo, "imagem teste hello my name is pedro andthis is a test hello my name is pedro and this is a test hello my name is pedro and this is a test hello my name is pedro and this is a test")
		r.add_graph_to_table(logo, "imagem teste")
		r.break_table()
		r.add_graph_to_table(logo, "imagem teste")
		r.add_graph_to_table(logo, "imagem teste")
		r.flush_graphs_to_row()
		r.add_spacer(28)
		r.add_graph_to_table(logo, "imagem teste")
		r.flush_graphs_to_row()

		f = Graphic("dasd", None, False, a = [[1,2,3,5,7], [3, 5, 6, 6, 3]], b = [[1,5,12,15,18], [3, 5, 6, 6, 3]])
		r.add_graph(f, "yo")
		r.flush_graphs_to_row()

		r.save_file()

	else:
		doc = SimpleDocTemplate( "EE" + ".pdf",pagesize=A4,
								rightMargin=72,leftMargin=72,
								topMargin=72,bottomMargin=18)

		Story=[]
		test_graph = "test.png"



		magName = "Pythonista"
		issueNum = 12
		subPrice = "99.00"
		limitedDate = "03/05/2010"
		freeGift = "tin foil hat"

		formatted_time = time.ctime()
		full_name = "Mike Driscoll"

		styles=getSampleStyleSheet()

		styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

		table_style_image = TableStyle([('ALING', (0, 0), (-1, -1), 'CENTER'),
									('VALID', (0, 0), (-1, -1), 'CENTER')])

		plt.plot([date(1990,1,1), date(1991,1,1), date(1991,2,1), date(1999,1,2)],[1, 2, 3, 1])
		plt.savefig(test_graph)


		im = Image(logo, 2*inch, 2*inch)
		im2 = Image(test_graph, 3*inch, 2*inch)


		Story.append(Paragraph("Titulo", styles["Title"]))
		# Story.append(im)

		p = Paragraph(lorem, styles["Justify"])

		Story.append(Table([[im, im2], [p, p]],
							colWidths=[3.3 * inch, 3.3 * inch],
							rowHeights=[2.5 * inch, 0.5 * inch], style=table_style_image))
		Story.append(Table([[p,im2]],
							colWidths=[3.3 * inch, 3.3 * inch],
							rowHeights=[2.5 * inch], style=table_style_image))

		ptext = '<font size="12">%s</font>' % formatted_time



		Story.append(Paragraph(ptext, styles["Normal"]))
		Story.append(Spacer(1, 12))

		ptext = '<font size="12">Dear %s:</font>' % full_name.split()[0].strip()
		Story.append(Paragraph(ptext, styles["Normal"]))
		Story.append(Spacer(1, 12))
		ptext = '<font size="12">We <b>would</b> like to welcome you to our subscriber base for %s Magazine! \
				You will receive %s issues at the excellent introductory price of $%s. Please respond by\
				%s to start receiving your subscription and get the following free gift: %s.</font>' % (magName, 
																										issueNum,
																										subPrice,
																										limitedDate,
																										freeGift)
		Story.append(Paragraph(ptext, styles["Justify"]))
		Story.append(Spacer(1, 12))
		doc.build(Story)