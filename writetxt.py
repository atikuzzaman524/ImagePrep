import xml.etree.ElementTree as ET
import glob
from bs4 import BeautifulSoup


for paths in glob.iglob('*.jpg'):
	print paths

	# filename = paths.replace('.xml', '.txt')
	# f = open(filename, "w+")

 #   	tree = ET.parse(paths)
 #   	root = tree.getroot()

 #   	for child in root:
 #   		if child.tag == "object":
 #   			for subchild in child:
 #   				if subchild.tag == "name":
 #   					object_class = subchild.text
 #   					#print objectid
 #   				if subchild.tag == "bndbox":
 #   					for subsubchild in subchild:
 #   						if subsubchild.tag == "xmin":
 #   							x_min = int(subsubchild.text)
 #   						if subsubchild.tag == "ymin":
 #   							y_min = int(subsubchild.text)
 #   						if subsubchild.tag == "xmax":
 #   							x_max = int(subsubchild.text)
 #   						if subsubchild.tag == "ymax":
 #   							y_max = int(subsubchild.text)
   							
 #   					width = x_max - x_min
 #   					height = y_max - y_min
 #   					line = object_class + ' ' + str(x_min) + ' ' + str(y_min) + ' ' + str(width) + ' ' + str(height)
 #   					f.write(line + "\n")
   		#print child.tag
   		#for child2 in child:
   			#print child2.tag

#   	for country in root.iter('name'):
 #  		print country.text

  