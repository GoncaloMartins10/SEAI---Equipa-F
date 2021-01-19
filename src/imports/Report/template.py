# https://www.blog.pythonlibrary.org/2010/03/08/a-simple-step-by-step-reportlab-tutorial/?fbclid=IwAR3xumnPIKzsc4P5IO-MJXgkJc8JtHlkHuxPicOP1GOJO7vh88BlR3gKKAQ

import os
import time


from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import utils, colors

from .graphics import Graphic

class ImageDetails:
	# https://stackoverflow.com/questions/5327670/image-aspect-ratio-using-reportlab-in-python
	def __init__(self, path, caption):
		self.path = path
		img = utils.ImageReader(path)
		self.width, self.height = img.getSize()
		self.caption = caption
	
	def __repr__(self):
		return f"Image details for {self.path}"

	def get_image(self, width_mult = 1, height_mult = 1):
		return Image(self.path, width = self.width*width_mult, height = self.height*height_mult)

	def get_image_by_ratio(self, ratio = 1):
		return Image(self.path, width = self.width*ratio, height = self.height*ratio)
	
	def get_image_by_width(self, width = 1*cm):
		aspect = self.height / float(self.width)
		return Image(self.path, width = width, height = width*aspect)

	def get_image_by_height(self, height = 1*cm):
		aspect = self.width / float(self.height)
		return Image(self.path, width = (height*aspect), height = height)

class Report:
	def __init__(self, transformer, path_to_save):
		self.name = "Transformer " + transformer
		self.path = os.path.join(path_to_save, self.name.replace(" ", "_"))
		self.doc = SimpleDocTemplate( self.path + ".pdf",pagesize=A4,
						rightMargin=72,leftMargin=72,
						topMargin=72,bottomMargin=18)
		self.catalogue = []

		self._reset_internal_state()
		self._init_styles()
		self._set_graphs_param()

		self.catalogue.append(self.add_title(self.name))

	def __repr__(self):
		return f"Report {self.name}"

	def save_file(self):
		self.doc.build(self.catalogue)

	def _set_graphs_param(self, width = 3 * cm , height = 3 * cm):
		self._max_width =3.3 * inch
		self._max_height = 2.5 * inch
		self._capt_min_height = 0.2 * inch
		self._space_table = 0.3 * cm

	def _reset_internal_state(self):
		self._figures = []
		self.figures_for_table = []
		self._table_width = 0
		self._table_height = 0
		self._colWidths = []
		self._rowHeights = []
		self._figure_count = 1

	def _reset_table(self, all = False):
		if all:
			self.figures_for_table = []
			self._table_width = 0
			self._table_height = 0
		
		self._figures = []
		
	def _init_styles(self):
		self.styles=getSampleStyleSheet()
		self.styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
		self.table_style_image = TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
										('VALIGN', (0, 0), (-1, -1), 'MIDDLE')])
		self.table_style_caption = TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
											('VALIGN',(0, 0), (-1, -1), 'TOP')])

	def __del__(self):
		self.save_file()
		# os.remove("test_graph.png")

	def add_paragraph(self, paragraph):
		self.catalogue.append(paragraph)
	
	def add_with_style(self, text, style):
		p = Paragraph(text, self.styles[style])
		self.add_paragraph(p)

	def add_normal(self, text):
		p = Paragraph(text, self.styles["Normal"])
		self.add_paragraph(p)
	
	def add_title(self, title):
		p = Paragraph(title, self.styles["Title"])
		self.add_paragraph(p)

	def add_subtitle(self, subtitle):
		p = Paragraph(subtitle, self.styles["Heading1"])
		self.add_paragraph(p)

	def get_images_and_capts(self):
		figs = []
		capts = []
		for i in self._figures:
			figs.append(i.get_image_by_width(self._max_width)) # self._graphs_height
			capts.append(i.caption)
		return [figs, capts]

	def add_graph_to_table(self, path, caption):
		"""
		Adiciona o gráfico à lista de gráficos
		"""
		capt = "<b>Figure " + str(self._figure_count) + "</b>: " + caption

		#i = 50
		#while len(capt)-i > 0:
		#	for index, item in enumerate(list(capt[i-50:i])[::-1]):
		#		if item == " ":
		#			i = i - index
		#			break
		#	capt = capt[:i] + "\n" + capt[i:]
		#	i+=51

		p = Paragraph(capt, self.styles["Justify"])
		image = ImageDetails(path, p)
		self._figures.append(image)

		self._figure_count +=1

	def break_table(self):
		imgs = self.get_images_and_capts()

		if self._table_width == 0:
			self._table_width = len(imgs[0])
		elif self._table_width != len(imgs[0]):
			raise Exception("Inconsistent table size")
		
		self._table_height += 2
		self.figures_for_table.extend(imgs)
		self._reset_table()
			
	def get_colWidths(self):
		w = []
		for i in range(self._table_width):
			if i == self._table_width-1:
				w.append(self._max_width)
			else:
				w.append(self._max_width + 0.2 *cm)
		return w

	def get_rowHeights_images(self, images):
		max_h = images[0].drawHeight
		for item in images[1:]:
			if item.drawHeight > max_h:
				max_h = item.drawHeight
		return [max_h]

	def get_rowHeights_captions(self, captions):

		max = int(len(captions[0].text)/51) + int(bool(len(captions[0].text)%51))
		if len(captions) > 1:
			for i in captions[1:]:
				t = int(len(i.text)/51) + int(bool(len(i.text)%51))
				if max < t:
					max = t

		h = [self._capt_min_height * max]
		return h

	def flush_graphs_to_row(self):
		"""
		Imprime a lista de gráficos numa só linha da tabela
		"""
		## Não vai funcionar muito bem porque a largura não é variavel com o tamanho da imagem
		self.break_table()
		for index, item in enumerate(self.figures_for_table):
			is_caption = bool(index % 2)
			needs_spacer = (index < len(self.figures_for_table) - 1)
			if is_caption:
				self.catalogue.append(Table([item],
											colWidths = self.get_colWidths(),
											rowHeights = self.get_rowHeights_captions(item),
											style=self.table_style_caption))
				if needs_spacer:
					self.add_spacer(12)
			else:
				self.catalogue.append(Table([item],
										colWidths = self.get_colWidths(),
										rowHeights = self.get_rowHeights_images(item),
										style=self.table_style_image))		
		self._reset_table(True)

	def add_spacer(self, space=12):
		self.catalogue.append(Spacer(1, space))

	def add_graph(self, graph: Graphic, caption):
		self.add_graph_to_table(graph.get_image_path(), caption)