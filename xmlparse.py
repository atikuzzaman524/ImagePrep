import xml.etree.ElementTree as ET
import glob
from bs4 import BeautifulSoup


for paths in glob.iglob('*.xml'):


   	tree = ET.parse(paths)
   	root = tree.getroot()
   	for country in root.findall('filename'):
   		extension = paths.replace('.xml','.jpg')
   		country.text = str(extension)
   		print country.text

   	tree.write(paths)